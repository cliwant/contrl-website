/**
 * contrl.ai sign-up backend — Google Apps Script web app.
 *
 * POST (signup):  the page signs the user in with Firebase Auth (Google or email + password) and sends
 *                 the Firebase ID token. We verify it with the Identity Toolkit API, take the email from it,
 *                 append a row to "Sheet1" of TARGET_SHEET_ID, compute the onboarding position
 *                 (POSITION_OFFSET + regular signups; invited signups form a front queue from #1),
 *                 post to Slack #7-alert, send the welcome email (first sign-up only), return {ok, position, invited, duplicate, schedule_url}.
 * Script Properties: SLACK_WEBHOOK, SCHEDULE_URL (Google Calendar booking page; optional).
 * Location: estimated from the browser's time zone + locale the page sends (no IP lookup).
 * UTM: utm_* / ref query params from the landing URL, stored as 'utm_source=…&utm_campaign=…'.
 * GET ?invite=X:  checks an invite code → {ok, valid}.
 *
 * Deploy: Deploy → New deployment → Web app → Execute as Me · Who has access: Anyone → copy /exec URL
 * into WAITLIST_ENDPOINT in index.html. After editing: Deploy → Manage deployments → ✎ → New version.
 *
 * POST {action: 'support_reply', secret, to, subject, html, text}: the web app server mails a support-chat
 *                 reply to a customer who has left (server/support.mjs). Needs Script Property SUPPORT_SECRET
 *                 (the same value as on the server); anything else is refused. At most 300 a day.
 *
 * Invite codes: tab "Invites", column A = codes. A used code gets the email in column B (one-time).
 */

const TARGET_SHEET_ID = '1x_jzKkbUk3MwhJi8aVEQeqvML97MgclHBlCqJ2LRwGY';
const SHEET_WAITLIST = 'Sheet1';
const SHEET_INVITES = 'Invites';
const HEADERS = ['Date/Time', 'Region', 'Email', 'invite_code', 'invited', 'source', 'user_agent', 'position', 'provider', 'location', 'utm'];
const FIREBASE_API_KEY = 'AIzaSyAEAbx0ZAlvNMWDAxloVg8JevO7GDls7I8';   // public web key of the contrl-ai Firebase project
const POSITION_OFFSET = 100;   // first regular signup is #101
const SEND_EMAIL = true;
const SITE = 'https://contrl.ai';

// Welcome email (sent once, on the first sign-up), in the language of the page the user signed up on.
// The web app is open: the email takes them straight to it. zh signups get the app in English.
const APP = 'https://app.contrl.ai/';
const T = {
  en: { subject: 'Welcome to Contrl — your account is ready', hi: 'Welcome to Contrl.',
        body: 'Your account is ready. Upload an RFP and Contrl works through it with you — from the analysis and strategy to the slides. You make the calls; AI does the writing.',
        steps: ['Upload your RFP, or start with a sample RFP', 'Answer a short strategy interview and pick your Win Theme', 'Get the slides section by section'],
        trial: 'Start your first proposal free.', cta: 'Start your first proposal',
        help: 'Questions? Just reply to this email.', tag: 'You make the decisions. AI writes on your behalf.' },
  ko: { subject: 'Contrl 가입을 환영합니다 — 지금 바로 첫 제안서를 시작해 보세요', hi: 'Contrl에 오신 것을 환영합니다.',
        body: '계정이 준비됐습니다. RFP를 올리면 Contrl이 분석부터 전략, 슬라이드까지 함께 만들어 갑니다. 방향은 직접 정하고, 쓰는 일은 AI가 맡습니다.',
        steps: ['RFP를 올리거나 샘플 RFP로 시작하기', '짧은 전략 인터뷰에 답하고 Win Theme 고르기', '섹션별로 슬라이드 받아 보기'],
        trial: '첫 제안서를 무료로 시작해 보세요.', cta: '첫 제안서 시작하기',
        help: '궁금한 점은 이 메일에 바로 답장해 주세요.', tag: '사람이 정하고, AI가 씁니다.' },
  ja: { subject: 'Contrlへようこそ — さっそく最初の提案書を始めましょう', hi: 'Contrlへようこそ。',
        body: 'アカウントの準備ができました。RFPをアップロードすると、Contrlが分析から戦略、スライドまで一緒に作り上げます。方針はあなたが決め、作成はAIが担います。',
        steps: ['RFPをアップロード、またはサンプルRFPで始める', '短い戦略インタビューに答えてWin Themeを選ぶ', 'セクションごとにスライドを受け取る'],
        trial: '最初の提案書を無料で始められます。', cta: '最初の提案書を始める',
        help: 'ご不明な点は、このメールにそのまま返信してください。', tag: '方針は人が決め、作成はAIが担う。' },
  zh: { subject: '欢迎加入 Contrl — 你的账号已开通', hi: '欢迎加入 Contrl。',
        body: '你的账号已经开通。上传 RFP 后，Contrl 会和你一起完成从分析、策略到幻灯片的全过程。方向由你决定，撰写交给 AI。',
        steps: ['上传 RFP，或用示例 RFP 开始', '回答简短的策略访谈，选定 Win Theme', '按章节获取幻灯片'],
        trial: '第一份提案可免费开始制作。', cta: '开始第一份提案',
        help: '有任何问题，直接回复这封邮件即可。', tag: '你来决定，AI来写。' },
};

function doPost(e) {
  let body = {};
  try { body = JSON.parse((e.postData && e.postData.contents) || '{}'); } catch (err) {}
  if (body.action === 'support_reply') return supportReply_(body);
  let email = '', provider = 'email-only';
  if (body.idToken) {
    const who = verifyIdToken_(body.idToken);
    if (!who) return json_({ ok: false, error: 'invalid_token' });
    email = who.email; provider = who.provider;
    reportToApp_(body);
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
    const utm = String(body.utm || '').slice(0, 300);
    sh.appendRow([new Date(), lang, email, code, invited, body.source || '', body.ua || '', position, provider, loc.text, utm]);
    const rowUrl = `${ss.getUrl()}#gid=${sh.getSheetId()}&range=A${sh.getLastRow()}`;
    notifySlack_({ email, position, invited, code, lang, provider, loc, utm, source: body.source || '', total: rows.length + 1, rowUrl });
    if (SEND_EMAIL) sendConfirmation_(email, position, invited, lang, schedule);
    return json_({ ok: true, position, invited, invalidCode: !!(code && !invited), schedule_url: schedule });
  } finally {
    lock.releaseLock();
  }
}

/** Tells the web app's server about the sign-up (its admin page lists every sign-up). The server checks the
 *  user's own ID token, so nothing else is needed; a failure here never blocks the sign-up. */
function reportToApp_(body) {
  try {
    UrlFetchApp.fetch(APP + 'api/signup-record', { method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ idToken: body.idToken, lang: body.lang || '', source: body.source || '', utm: String(body.utm || '').slice(0, 300), tz: body.tz || '', locale: body.locale || '' }) });
  } catch (err) {}
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

/** 'utm_source=email&utm_campaign=reengage' → 'email / reengage' for Slack. */
function utmLabel_(utm) {
  const q = {}; String(utm).split('&').forEach(p => { const i = p.indexOf('='); if (i > 0) q[p.slice(0, i)] = p.slice(i + 1); });
  return [q.utm_source, q.utm_medium, q.utm_campaign, q.ref].filter(Boolean).join(' / ') || utm;
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
      { type: 'context', elements: [{ type: 'mrkdwn', text: `${d.loc ? d.loc.slack + ' · ' : ''}page ${flag} ${d.lang} · signups ${d.total}${d.code ? ` · code \`${d.code}\`${d.invited ? '' : ' (invalid)'}` : ''} · ${d.source}${d.utm ? ` · 🔗 ${utmLabel_(d.utm)}` : ''} · <${d.rowUrl}|Open row in Sheet>` }] },
    ],
  };
  try { UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', payload: JSON.stringify(payload), muteHttpExceptions: true }); } catch (err) {}
}

function sendConfirmation_(email, position, invited, lang, schedule) {
  const t = T[lang] || T.en;
  const link = APP + '?lang=' + (['ko', 'en', 'ja'].includes(lang) ? lang : 'en');
  const plain = `${t.hi}\n\n${t.body}\n\n${t.steps.map((x, i) => `${i + 1}. ${x}`).join('\n')}\n\n${t.trial}\n\n${t.cta}: ${link}\n\n${t.help}\n\nContrl — ${t.tag}\n${SITE}`;
  const steps = t.steps.map((x, i) => `<tr><td valign="top" style="padding:6px 10px 6px 0;"><span style="display:inline-block;width:22px;height:22px;line-height:22px;border-radius:999px;background:#fff6ef;color:#b7551b;font-size:12px;font-weight:800;text-align:center;">${i + 1}</span></td><td style="padding:6px 0;font-size:15px;line-height:1.5;color:#3f3f46;">${x}</td></tr>`).join('');
  const html = `
<!doctype html><html><body style="margin:0;padding:0;background:#f6f3ee;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f6f3ee;padding:32px 16px;">
  <tr><td align="center">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;background:#ffffff;border-radius:16px;border:1px solid #ebe5de;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Apple SD Gothic Neo','Noto Sans KR','Hiragino Sans','PingFang SC',sans-serif;color:#18181b;">
      <tr><td style="padding:28px 32px 0;font-size:22px;font-weight:800;letter-spacing:-0.02em;">contrl<span style="color:#F27A2E;">.</span></td></tr>
      <tr><td style="padding:24px 32px 0;font-size:19px;font-weight:800;">${t.hi}</td></tr>
      <tr><td style="padding:12px 32px 0;font-size:15px;line-height:1.65;color:#52525b;">${t.body}</td></tr>
      <tr><td style="padding:16px 32px 0;"><table role="presentation" cellspacing="0" cellpadding="0">${steps}</table></td></tr>
      <tr><td style="padding:22px 32px 0;"><a href="${link}" style="display:inline-block;background:#F27A2E;color:#ffffff;text-decoration:none;font-weight:700;font-size:15px;padding:14px 24px;border-radius:999px;">${t.cta} →</a></td></tr>
      <tr><td style="padding:14px 32px 0;font-size:13px;color:#71717a;">${t.trial}</td></tr>
      <tr><td style="padding:18px 32px 0;font-size:13px;color:#71717a;">${t.help}</td></tr>
      <tr><td style="padding:28px 32px 28px;font-size:12px;color:#a1a1aa;border-top:1px solid #f0ebe4;margin-top:24px;">Contrl — ${t.tag}<br><a href="${SITE}" style="color:#a1a1aa;">contrl.ai</a> · Cliwant Inc. · 12130 Millennium Dr #300, Los Angeles, CA 90094</td></tr>
    </table>
  </td></tr>
</table>
</body></html>`;
  try { MailApp.sendEmail({ to: email, subject: t.subject, body: plain, htmlBody: html, name: 'Contrl' }); } catch (err) {}
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}


/** A support-chat reply by email, asked by the web app's server (server/support.mjs). Only with the shared
 *  secret (Script Property SUPPORT_SECRET); one recipient, size-capped, at most 300 a day. */
function supportReply_(body) {
  const secret = PropertiesService.getScriptProperties().getProperty('SUPPORT_SECRET') || '';
  if (secret.length < 16 || String(body.secret || '') !== secret) return json_({ ok: false, error: 'forbidden' });
  const to = String(body.to || '').trim();
  if (!/^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]{2,}$/.test(to)) return json_({ ok: false, error: 'bad_to' });
  const subject = String(body.subject || '').slice(0, 200), html = String(body.html || '').slice(0, 60000), text = String(body.text || '').slice(0, 20000);
  if (!subject || !text) return json_({ ok: false, error: 'empty' });
  const cache = CacheService.getScriptCache(), key = 'support-mail-' + Utilities.formatDate(new Date(), 'UTC', 'yyyyMMdd');
  const n = Number(cache.get(key) || 0);
  if (n >= 300) return json_({ ok: false, error: 'daily_limit' });
  cache.put(key, String(n + 1), 21600);
  MailApp.sendEmail({ to: to, subject: subject, body: text, htmlBody: html || undefined, name: 'Contrl' });
  return json_({ ok: true });
}
