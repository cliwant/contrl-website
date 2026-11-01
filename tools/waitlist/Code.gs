/**
 * contrl.ai waitlist backend — Google Apps Script web app.
 *
 * On each signup (POST from the landing page):
 *   1. appends a row to the "Waitlist" tab of TARGET_SHEET_ID (row order = queue order)
 *   2. computes the queue position: POSITION_OFFSET + number of regular signups
 *      (invited signups form a separate front queue numbered from 1)
 *   3. posts to Slack #7-alert (Script Property SLACK_WEBHOOK) with the position
 *   4. emails the signup a confirmation with their position (sent from the deploying account)
 *   5. returns {ok, position, invited} as JSON — the page shows a toast "You're #N in line."
 *
 * Deploy: Deploy → New deployment → Web app → Execute as Me · Who has access: Anyone → copy /exec URL
 * into WAITLIST_ENDPOINT in index.html. After editing: Deploy → Manage deployments → ✎ → New version.
 *
 * Invite codes: tab "Invites", column A = codes. A used code gets the email in column B (one-time).
 */

const TARGET_SHEET_ID = '1x_jzKkbUk3MwhJi8aVEQeqvML97MgclHBlCqJ2LRwGY';
const SHEET_WAITLIST = 'Waitlist';
const SHEET_INVITES = 'Invites';
const POSITION_OFFSET = 100;   // first regular signup is #101
const SEND_EMAIL = true;

const EMAIL = {
  en: { subject: (n) => `You're #${n} on the Contrl waitlist`,
        body: (n, inv) => `You're in line for Contrl — spot #${n}${inv ? ' (front queue, via invite)' : ''}.\n\nAccess opens in order of signup, 25 teams a week. We'll email you when your seat opens.\n\nContrl — You decide. AI writes the rest.\nhttps://contrl.ai` },
  ko: { subject: (n) => `Contrl 대기 명단 ${n}번째로 등록됐습니다`,
        body: (n, inv) => `Contrl 대기 명단에 등록됐습니다. 순번은 ${n}번${inv ? ' (초대 · 앞줄 대기열)' : ''}입니다.\n\n신청 순서대로 매주 25팀씩 열립니다. 자리가 열리면 이 메일 주소로 알려 드리겠습니다.\n\nContrl — 사람이 정하고, AI가 씁니다.\nhttps://contrl.ai` },
  ja: { subject: (n) => `Contrl ウェイトリストに${n}番目で登録されました`,
        body: (n, inv) => `Contrlのウェイトリストに登録されました。順番は${n}番${inv ? '（招待・優先列）' : ''}です。\n\n登録順に毎週25チームずつ開放します。席が空き次第、このメールアドレスにご連絡します。\n\nContrl — あなたが決め、AIが書く。\nhttps://contrl.ai` },
  zh: { subject: (n) => `你已排在 Contrl 等候名单第 ${n} 位`,
        body: (n, inv) => `你已加入 Contrl 等候名单，排位第 ${n}${inv ? '（邀请 · 优先队列）' : ''}。\n\n按报名顺序每周开放 25 个团队。名额开放时我们会发邮件到这个地址。\n\nContrl — 你来决定，AI来写。\nhttps://contrl.ai` },
};

function doPost(e) {
  let body = {};
  try { body = JSON.parse((e.postData && e.postData.contents) || '{}'); } catch (err) {}
  const email = String(body.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json_({ ok: false, error: 'invalid_email' });
  const lang = ['en', 'ko', 'ja', 'zh'].includes(body.lang) ? body.lang : 'en';

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.openById(TARGET_SHEET_ID);
    const sh = ss.getSheetByName(SHEET_WAITLIST) || ss.insertSheet(SHEET_WAITLIST);
    if (sh.getLastRow() === 0) sh.appendRow(['timestamp', 'email', 'lang', 'invite_code', 'invited', 'source', 'user_agent', 'position']);

    const rows = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, 8).getValues() : [];
    const existing = rows.find(r => String(r[1]).toLowerCase() === email);
    if (existing) return json_({ ok: true, position: Number(existing[7]), invited: existing[4] === true, duplicate: true });

    const code = String(body.invite || '').trim().toUpperCase();
    const invited = code ? redeemInvite_(ss, code, email) : false;
    const position = invited
      ? rows.filter(r => r[4] === true).length + 1
      : POSITION_OFFSET + rows.filter(r => r[4] !== true).length + 1;

    sh.appendRow([new Date(), email, lang, code, invited, body.source || '', body.ua || '', position]);
    notifySlack_({ email, position, invited, code, lang, source: body.source || '', total: rows.length + 1 });
    if (SEND_EMAIL) sendConfirmation_(email, position, invited, lang);
    return json_({ ok: true, position, invited });
  } finally {
    lock.releaseLock();
  }
}

function doGet() { return json_({ ok: true, service: 'contrl waitlist' }); }

function redeemInvite_(ss, code, email) {
  const sh = ss.getSheetByName(SHEET_INVITES);
  if (!sh || sh.getLastRow() === 0) return false;
  const codes = sh.getRange(1, 1, sh.getLastRow(), 2).getValues();
  for (let i = 0; i < codes.length; i++) {
    if (String(codes[i][0]).trim().toUpperCase() === code) {
      if (codes[i][1]) return false;
      sh.getRange(i + 1, 2).setValue(email);
      return true;
    }
  }
  return false;
}

function notifySlack_(d) {
  const url = PropertiesService.getScriptProperties().getProperty('SLACK_WEBHOOK');
  if (!url) return;
  const flag = { en: '🇺🇸', ko: '🇰🇷', ja: '🇯🇵', zh: '🇨🇳' }[d.lang] || '🌐';
  const text = `${d.invited ? '🎟️' : '🆕'} Waitlist #${d.position}${d.invited ? ' (invite · front queue)' : ''} — ${d.email}`;
  const payload = {
    text,
    blocks: [
      { type: 'section', text: { type: 'mrkdwn', text: `*${text}*` } },
      { type: 'context', elements: [{ type: 'mrkdwn', text: `${flag} ${d.lang} · signups ${d.total}${d.code ? ` · code \`${d.code}\`${d.invited ? '' : ' (invalid)'}` : ''} · ${d.source}` }] },
    ],
  };
  try { UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', payload: JSON.stringify(payload), muteHttpExceptions: true }); } catch (err) {}
}

function sendConfirmation_(email, position, invited, lang) {
  const t = EMAIL[lang] || EMAIL.en;
  try { MailApp.sendEmail({ to: email, subject: t.subject(position), body: t.body(position, invited), name: 'Contrl' }); } catch (err) {}
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
