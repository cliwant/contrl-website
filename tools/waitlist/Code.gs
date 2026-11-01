/**
 * contrl.ai waitlist backend — Google Apps Script web app.
 *
 * POST (signup):  appends a row to "Sheet1" of TARGET_SHEET_ID, computes the queue position
 *                 (POSITION_OFFSET + regular signups; invited signups form a front queue from #1),
 *                 posts to Slack #7-alert, emails an HTML confirmation, returns {ok, position, invited, duplicate}.
 * GET ?invite=X:  checks an invite code → {ok, valid}.
 *
 * Deploy: Deploy → New deployment → Web app → Execute as Me · Who has access: Anyone → copy /exec URL
 * into WAITLIST_ENDPOINT in index.html. After editing: Deploy → Manage deployments → ✎ → New version.
 *
 * Invite codes: tab "Invites", column A = codes. A used code gets the email in column B (one-time).
 */

const TARGET_SHEET_ID = '1x_jzKkbUk3MwhJi8aVEQeqvML97MgclHBlCqJ2LRwGY';
const SHEET_WAITLIST = 'Sheet1';
const SHEET_INVITES = 'Invites';
const HEADERS = ['Date/Time', 'Region', 'Email', 'invite_code', 'invited', 'source', 'user_agent', 'position'];
const POSITION_OFFSET = 100;   // first regular signup is #101
const SEND_EMAIL = true;
const SITE = 'https://contrl.ai';

const T = {
  en: { subject: (n) => `You're #${n} on the Contrl waitlist`, hi: "You're in line.", spot: 'Your spot', front: 'Front queue · invited',
        body: 'Access opens in order of signup, 25 teams a week. We\'ll email you when your seat opens — nothing else.',
        cta: 'Back to contrl.ai', tag: 'You decide. AI writes the rest.' },
  ko: { subject: (n) => `Contrl 대기 명단 ${n}번째로 등록됐습니다`, hi: '대기 명단에 등록됐습니다.', spot: '내 순번', front: '앞줄 대기열 · 초대',
        body: '신청 순서대로 매주 25팀씩 열립니다. 자리가 열리면 이 메일 주소로 알려 드리고, 그 외 메일은 보내지 않습니다.',
        cta: 'contrl.ai로 돌아가기', tag: '사람이 정하고, AI가 씁니다.' },
  ja: { subject: (n) => `Contrl ウェイトリストに${n}番目で登録されました`, hi: 'ウェイトリストに登録されました。', spot: 'あなたの順番', front: '優先列・招待',
        body: '登録順に毎週25チームずつ開放します。席が空き次第、このメールアドレスにご連絡します。それ以外のメールは送りません。',
        cta: 'contrl.aiへ戻る', tag: 'あなたが決め、AIが書く。' },
  zh: { subject: (n) => `你已排在 Contrl 等候名单第 ${n} 位`, hi: '你已加入等候名单。', spot: '你的排位', front: '优先队列 · 邀请',
        body: '按报名顺序每周开放 25 个团队。名额开放时我们会发邮件到这个地址，除此之外不会打扰你。',
        cta: '返回 contrl.ai', tag: '你来决定，AI来写。' },
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
    ensureHeaders_(sh);

    const rows = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, HEADERS.length).getValues() : [];
    const existing = rows.find(r => String(r[2]).toLowerCase() === email);
    if (existing) return json_({ ok: true, duplicate: true, position: Number(existing[7]), invited: existing[4] === true });

    const code = String(body.invite || '').trim().toUpperCase();
    const invited = code ? redeemInvite_(ss, code, email) : false;
    const position = invited
      ? rows.filter(r => r[4] === true).length + 1
      : POSITION_OFFSET + rows.filter(r => r[4] !== true).length + 1;

    sh.appendRow([new Date(), lang, email, code, invited, body.source || '', body.ua || '', position]);
    const rowUrl = `${ss.getUrl()}#gid=${sh.getSheetId()}&range=A${sh.getLastRow()}`;
    notifySlack_({ email, position, invited, code, lang, source: body.source || '', total: rows.length + 1, rowUrl });
    if (SEND_EMAIL) sendConfirmation_(email, position, invited, lang);
    return json_({ ok: true, position, invited, invalidCode: !!(code && !invited) });
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  const code = String((e && e.parameter && e.parameter.invite) || '').trim().toUpperCase();
  if (code) {
    const ss = SpreadsheetApp.openById(TARGET_SHEET_ID);
    return json_({ ok: true, valid: inviteStatus_(ss, code) === 'unused' });
  }
  return json_({ ok: true, service: 'contrl waitlist' });
}

function ensureHeaders_(sh) {
  if (sh.getLastRow() === 0) { sh.appendRow(HEADERS); return; }
  const row = sh.getRange(1, 1, 1, HEADERS.length).getValues()[0];
  const fixed = HEADERS.map((h, i) => (row[i] === '' || row[i] === null) ? h : row[i]);
  if (fixed.some((v, i) => v !== row[i])) sh.getRange(1, 1, 1, HEADERS.length).setValues([fixed]);
}

/** 'unused' | 'used' | 'none' */
function inviteStatus_(ss, code) {
  const sh = ss.getSheetByName(SHEET_INVITES);
  if (!sh || sh.getLastRow() === 0) return 'none';
  const codes = sh.getRange(1, 1, sh.getLastRow(), 2).getValues();
  for (const r of codes) if (String(r[0]).trim().toUpperCase() === code) return r[1] ? 'used' : 'unused';
  return 'none';
}

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
      { type: 'context', elements: [{ type: 'mrkdwn', text: `${flag} ${d.lang} · signups ${d.total}${d.code ? ` · code \`${d.code}\`${d.invited ? '' : ' (invalid)'}` : ''} · ${d.source} · <${d.rowUrl}|Open row in Sheet>` }] },
    ],
  };
  try { UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', payload: JSON.stringify(payload), muteHttpExceptions: true }); } catch (err) {}
}

function sendConfirmation_(email, position, invited, lang) {
  const t = T[lang] || T.en;
  const plain = `${t.hi}\n${t.spot}: #${position}${invited ? ` (${t.front})` : ''}\n\n${t.body}\n\nContrl — ${t.tag}\n${SITE}`;
  const html = `
<!doctype html><html><body style="margin:0;padding:0;background:#f6f3ee;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f6f3ee;padding:32px 16px;">
  <tr><td align="center">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;background:#ffffff;border-radius:16px;border:1px solid #ebe5de;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Apple SD Gothic Neo','Noto Sans KR','Hiragino Sans','PingFang SC',sans-serif;color:#18181b;">
      <tr><td style="padding:28px 32px 0;font-size:22px;font-weight:800;letter-spacing:-0.02em;">contrl<span style="color:#F27A2E;">.</span></td></tr>
      <tr><td style="padding:24px 32px 0;font-size:18px;font-weight:700;">${t.hi}</td></tr>
      <tr><td style="padding:18px 32px 0;">
        <table role="presentation" cellspacing="0" cellpadding="0" style="background:#fff6ef;border:1px solid #f3d9c4;border-radius:12px;width:100%;">
          <tr><td style="padding:16px 20px;">
            <div style="font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#b7551b;">${t.spot}${invited ? ` · ${t.front}` : ''}</div>
            <div style="font-size:44px;font-weight:800;letter-spacing:-0.03em;color:#F27A2E;line-height:1.1;margin-top:4px;">#${position}</div>
          </td></tr>
        </table>
      </td></tr>
      <tr><td style="padding:18px 32px 0;font-size:15px;line-height:1.6;color:#52525b;">${t.body}</td></tr>
      <tr><td style="padding:22px 32px 0;">
        <a href="${SITE}" style="display:inline-block;background:#F27A2E;color:#ffffff;text-decoration:none;font-weight:700;font-size:14px;padding:12px 20px;border-radius:999px;">${t.cta}</a>
      </td></tr>
      <tr><td style="padding:28px 32px 28px;font-size:12px;color:#a1a1aa;border-top:1px solid #f0ebe4;margin-top:24px;">Contrl — ${t.tag}<br>Cliwant Inc. · 12130 Millennium Dr #300, Los Angeles, CA 90094</td></tr>
    </table>
  </td></tr>
</table>
</body></html>`;
  try { MailApp.sendEmail({ to: email, subject: t.subject(position), body: plain, htmlBody: html, name: 'Contrl' }); } catch (err) {}
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
