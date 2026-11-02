/**
 * contrl.ai sign-up backend — Google Apps Script web app.
 *
 * POST (signup):  the page signs the user in with Firebase Auth (Google or email + password) and sends
 *                 the Firebase ID token. We verify it with the Identity Toolkit API, take the email from it,
 *                 append a row to "Sheet1" of TARGET_SHEET_ID, compute the onboarding position
 *                 (POSITION_OFFSET + regular signups; invited signups form a front queue from #1),
 *                 post to Slack #7-alert, email the setup schedule, return {ok, position, invited, duplicate, schedule_url}.
 * Script Properties: SLACK_WEBHOOK, SCHEDULE_URL (Google Calendar booking page; optional).
 * Location: estimated from the browser's time zone + locale the page sends (no IP lookup).
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
const HEADERS = ['Date/Time', 'Region', 'Email', 'invite_code', 'invited', 'source', 'user_agent', 'position', 'provider', 'location'];
const FIREBASE_API_KEY = 'AIzaSyAEAbx0ZAlvNMWDAxloVg8JevO7GDls7I8';   // public web key of the contrl-ai Firebase project
const POSITION_OFFSET = 100;   // first regular signup is #101
const SEND_EMAIL = true;
const SITE = 'https://contrl.ai';

const T = {
  en: { subject: () => 'Welcome to Contrl — pick a time for your team setup', hi: 'Thanks for signing up.', spot: 'Your place in line', front: 'Front of the line · invited',
        body: 'Every team gets a hands-on setup: we connect your design system and past proposals to Contrl with you. We open accounts in signup order, so pick a time that works from the schedule below.',
        nolink: "We'll email you a setup schedule shortly.", cta: 'Pick a setup time', tag: 'You make the decisions. AI writes on your behalf.' },
  ko: { subject: () => 'Contrl 가입을 환영합니다 — 세팅 일정을 골라 주세요', hi: '가입해 주셔서 감사합니다.', spot: '내 순서', front: '초대 · 우선 세팅',
        body: 'Contrl은 팀마다 디자인 시스템과 과거 제안서를 연결하는 세팅이 필요해서, 저희가 직접 도와드리며 가입 순서대로 계정을 열고 있습니다. 아래 스케줄표에서 편한 시간을 골라 주세요.',
        nolink: '세팅 일정을 고를 수 있는 스케줄표를 곧 메일로 보내 드리겠습니다.', cta: '세팅 일정 고르기', tag: '사람이 정하고, AI가 씁니다.' },
  ja: { subject: () => 'Contrlへようこそ — 初期設定の日程をお選びください', hi: 'ご登録ありがとうございます。', spot: 'あなたの順番', front: '招待・優先セットアップ',
        body: 'Contrlはチームごとにデザインシステムと過去の提案書をつなぐ初期設定が必要なため、私たちが直接サポートしながら登録順にアカウントを開放しています。下の日程表からご都合のよい時間をお選びください。',
        nolink: '設定の日程を選べる日程表を、まもなくメールでお送りします。', cta: '設定の日程を選ぶ', tag: '方針は人が決め、作成はAIが担う。' },
  zh: { subject: () => '欢迎加入 Contrl — 请选择团队设置时间', hi: '感谢注册。', spot: '你的排位', front: '邀请 · 优先设置',
        body: 'Contrl 需要为每个团队连接设计系统和过往提案，因此我们会亲自协助设置，并按注册顺序开通账号。请在下方排期表中选择方便的时间。',
        nolink: '我们很快会把设置排期表发到你的邮箱。', cta: '选择设置时间', tag: '你来决定，AI来写。' },
};

function doPost(e) {
  let body = {};
  try { body = JSON.parse((e.postData && e.postData.contents) || '{}'); } catch (err) {}
  let email = '', provider = 'email-only';
  if (body.idToken) {
    const who = verifyIdToken_(body.idToken);
    if (!who) return json_({ ok: false, error: 'invalid_token' });
    email = who.email; provider = who.provider;
  } else {
    email = String(body.email || '').trim().toLowerCase();   // older cached pages
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json_({ ok: false, error: 'invalid_email' });
  const lang = ['en', 'ko', 'ja', 'zh'].includes(body.lang) ? body.lang : 'en';
  const schedule = scheduleUrl_();

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.openById(TARGET_SHEET_ID);
    const sh = ss.getSheetByName(SHEET_WAITLIST) || ss.insertSheet(SHEET_WAITLIST);
    ensureHeaders_(sh);

    const rows = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, HEADERS.length).getValues() : [];
    const existing = rows.find(r => String(r[2]).toLowerCase() === email);
    if (existing) return json_({ ok: true, duplicate: true, position: Number(existing[7]), invited: existing[4] === true, schedule_url: schedule });

    const code = String(body.invite || '').trim().toUpperCase();
    const invited = code ? redeemInvite_(ss, code, email) : false;
    const position = invited
      ? rows.filter(r => r[4] === true).length + 1
      : POSITION_OFFSET + rows.filter(r => r[4] !== true).length + 1;

    const loc = location_(body.tz, body.locale);
    sh.appendRow([new Date(), lang, email, code, invited, body.source || '', body.ua || '', position, provider, loc.text]);
    const rowUrl = `${ss.getUrl()}#gid=${sh.getSheetId()}&range=A${sh.getLastRow()}`;
    notifySlack_({ email, position, invited, code, lang, provider, loc, source: body.source || '', total: rows.length + 1, rowUrl });
    if (SEND_EMAIL) sendConfirmation_(email, position, invited, lang, schedule);
    return json_({ ok: true, position, invited, invalidCode: !!(code && !invited), schedule_url: schedule });
  } finally {
    lock.releaseLock();
  }
}

/** Verifies a Firebase ID token with the Identity Toolkit API → {email, provider} or null. */
function verifyIdToken_(idToken) {
  try {
    const r = UrlFetchApp.fetch('https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=' + FIREBASE_API_KEY, {
      method: 'post', contentType: 'application/json', payload: JSON.stringify({ idToken }), muteHttpExceptions: true });
    if (r.getResponseCode() !== 200) return null;
    const u = (JSON.parse(r.getContentText()).users || [])[0];
    if (!u || !u.email) return null;
    const ids = (u.providerUserInfo || []).map(p => p.providerId);
    return { email: String(u.email).toLowerCase(), provider: ids.includes('google.com') ? 'google' : (ids.includes('password') ? 'password' : (ids[0] || 'firebase')) };
  } catch (err) { return null; }
}

// Time zone → [country code, city]. Covers the target markets; anything else falls back to the zone's city.
const TZ_PLACE = {
  'Asia/Seoul': ['KR', 'Seoul'], 'Asia/Tokyo': ['JP', 'Tokyo'], 'Asia/Shanghai': ['CN', 'Shanghai'], 'Asia/Hong_Kong': ['HK', 'Hong Kong'],
  'Asia/Taipei': ['TW', 'Taipei'], 'Asia/Singapore': ['SG', 'Singapore'], 'Asia/Ho_Chi_Minh': ['VN', 'Ho Chi Minh City'], 'Asia/Saigon': ['VN', 'Ho Chi Minh City'],
  'Asia/Bangkok': ['TH', 'Bangkok'], 'Asia/Jakarta': ['ID', 'Jakarta'], 'Asia/Kuala_Lumpur': ['MY', 'Kuala Lumpur'], 'Asia/Manila': ['PH', 'Manila'],
  'Asia/Kolkata': ['IN', 'India'], 'Asia/Calcutta': ['IN', 'India'], 'Asia/Dubai': ['AE', 'Dubai'],
  'America/New_York': ['US', 'US Eastern'], 'America/Chicago': ['US', 'US Central'], 'America/Denver': ['US', 'US Mountain'], 'America/Phoenix': ['US', 'Arizona'],
  'America/Los_Angeles': ['US', 'US Pacific'], 'America/Anchorage': ['US', 'Alaska'], 'Pacific/Honolulu': ['US', 'Hawaii'],
  'America/Toronto': ['CA', 'Toronto'], 'America/Vancouver': ['CA', 'Vancouver'], 'America/Mexico_City': ['MX', 'Mexico City'], 'America/Sao_Paulo': ['BR', 'São Paulo'],
  'Europe/London': ['GB', 'London'], 'Europe/Berlin': ['DE', 'Berlin'], 'Europe/Paris': ['FR', 'Paris'], 'Europe/Amsterdam': ['NL', 'Amsterdam'],
  'Australia/Sydney': ['AU', 'Sydney'], 'Australia/Melbourne': ['AU', 'Melbourne'], 'Pacific/Auckland': ['NZ', 'Auckland'],
};
const flag_ = cc => /^[A-Z]{2}$/.test(cc || '') ? String.fromCodePoint(...[...cc].map(c => 0x1F1E6 + c.charCodeAt(0) - 65)) : '🌐';

/** Best-effort location from the browser time zone (+ locale region as a fallback) → {text, slack}. */
function location_(tz, locale) {
  tz = String(tz || '').slice(0, 64); locale = String(locale || '').slice(0, 32);
  const localeCC = (locale.match(/[-_]([A-Za-z]{2})\b/) || [])[1];
  const hit = TZ_PLACE[tz];
  const cc = hit ? hit[0] : (localeCC ? localeCC.toUpperCase() : '');
  const city = hit ? hit[1] : (tz.includes('/') ? tz.split('/').pop().replace(/_/g, ' ') : '');
  if (!cc && !city) return { text: '', slack: '📍 unknown' };
  const text = [city, cc].filter(Boolean).join(', ') + (tz ? ` (${tz})` : '');
  return { text, slack: `📍 ${flag_(cc)} ${[city, cc].filter(Boolean).join(', ')}${locale ? ` · ${locale}` : ''}` };
}

function scheduleUrl_() { return PropertiesService.getScriptProperties().getProperty('SCHEDULE_URL') || ''; }

function doGet(e) {
  const code = String((e && e.parameter && e.parameter.invite) || '').trim().toUpperCase();
  if (code) {
    const ss = SpreadsheetApp.openById(TARGET_SHEET_ID);
    return json_({ ok: true, valid: inviteStatus_(ss, code) === 'unused' });
  }
  return json_({ ok: true, service: 'contrl signup' });
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
  const via = { google: 'Google', password: 'email + password' }[d.provider] || d.provider;
  const text = `${d.invited ? '🎟️' : '🆕'} Signup #${d.position}${d.invited ? ' (invite · front of line)' : ''} — ${d.email} · ${via}`;
  const payload = {
    text,
    blocks: [
      { type: 'section', text: { type: 'mrkdwn', text: `*${text}*` } },
      { type: 'context', elements: [{ type: 'mrkdwn', text: `${d.loc ? d.loc.slack + ' · ' : ''}page ${flag} ${d.lang} · signups ${d.total}${d.code ? ` · code \`${d.code}\`${d.invited ? '' : ' (invalid)'}` : ''} · ${d.source} · <${d.rowUrl}|Open row in Sheet>` }] },
    ],
  };
  try { UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', payload: JSON.stringify(payload), muteHttpExceptions: true }); } catch (err) {}
}

function sendConfirmation_(email, position, invited, lang, schedule) {
  const t = T[lang] || T.en;
  const plain = `${t.hi}\n${t.spot}: #${position}${invited ? ` (${t.front})` : ''}\n\n${t.body}\n\n${schedule ? `${t.cta}: ${schedule}` : t.nolink}\n\nContrl — ${t.tag}\n${SITE}`;
  const action = schedule
    ? `<a href="${schedule}" style="display:inline-block;background:#F27A2E;color:#ffffff;text-decoration:none;font-weight:700;font-size:15px;padding:14px 24px;border-radius:999px;">${t.cta} →</a>`
    : `<div style="font-size:14px;color:#52525b;background:#faf7f2;border-radius:10px;padding:12px 16px;">${t.nolink}</div>`;
  const html = `
<!doctype html><html><body style="margin:0;padding:0;background:#f6f3ee;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f6f3ee;padding:32px 16px;">
  <tr><td align="center">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;background:#ffffff;border-radius:16px;border:1px solid #ebe5de;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Apple SD Gothic Neo','Noto Sans KR','Hiragino Sans','PingFang SC',sans-serif;color:#18181b;">
      <tr><td style="padding:28px 32px 0;font-size:22px;font-weight:800;letter-spacing:-0.02em;">contrl<span style="color:#F27A2E;">.</span></td></tr>
      <tr><td style="padding:24px 32px 0;font-size:19px;font-weight:800;">${t.hi}</td></tr>
      <tr><td style="padding:12px 32px 0;font-size:15px;line-height:1.65;color:#52525b;">${t.body}</td></tr>
      <tr><td style="padding:22px 32px 0;">${action}</td></tr>
      <tr><td style="padding:22px 32px 0;">
        <table role="presentation" cellspacing="0" cellpadding="0" style="background:#fff6ef;border:1px solid #f3d9c4;border-radius:12px;">
          <tr><td style="padding:10px 16px;font-size:13px;font-weight:700;color:#b7551b;">${t.spot}${invited ? ` · ${t.front}` : ''} &nbsp;<span style="font-size:18px;color:#F27A2E;">#${position}</span></td></tr>
        </table>
      </td></tr>
      <tr><td style="padding:28px 32px 28px;font-size:12px;color:#a1a1aa;border-top:1px solid #f0ebe4;">Contrl — ${t.tag}<br><a href="${SITE}" style="color:#a1a1aa;">contrl.ai</a> · Cliwant Inc. · 12130 Millennium Dr #300, Los Angeles, CA 90094</td></tr>
    </table>
  </td></tr>
</table>
</body></html>`;
  try { MailApp.sendEmail({ to: email, subject: t.subject(position), body: plain, htmlBody: html, name: 'Contrl' }); } catch (err) {}
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
