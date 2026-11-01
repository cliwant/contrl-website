# Waitlist backend (Google Sheet + Apps Script → Slack #7-alert)

The landing page POSTs each signup to `WAITLIST_ENDPOINT` (in `index.html`). `Code.gs` is the whole backend:
it stores the signup in a Google Sheet, computes the queue position, posts to Slack, and returns the position
so the page can show "You're #N in line." It also emails an HTML confirmation and answers the page's invite-code Check button (`GET ?invite=`).

## One-time setup (≈10 minutes, needs your Google + Slack accounts)

1. **Slack webhook** — api.slack.com/apps → *Create New App* (from scratch, workspace Cliwant) →
   *Incoming Webhooks* → Activate → *Add New Webhook to Workspace* → channel **#7-alert** → copy the
   `https://hooks.slack.com/services/…` URL.
2. **Sheet + script** — create a Google Sheet named e.g. `contrl waitlist` → *Extensions → Apps Script* →
   replace the default code with `Code.gs` → save.
3. **Secret** — in Apps Script: *Project Settings → Script Properties → Add property*:
   `SLACK_WEBHOOK` = the URL from step 1.
4. **Deploy** — *Deploy → New deployment → type: Web app* → *Execute as: Me* · *Who has access: Anyone* →
   Deploy → authorize → copy the **Web app URL** (ends in `/exec`).
5. **Wire the page** — paste that URL into `WAITLIST_ENDPOINT` in `index.html`, remove `FALLBACK_MAILTO`'s
   mailto branch if you like, commit, merge.

Re-deploying after editing `Code.gs`: *Deploy → Manage deployments → ✎ → Version: New* (the URL stays the same).

## Sheets

- `Sheet1` (headers auto-filled): Date/Time · Region · Email · invite_code · invited · source · user_agent · position
  Positions start at #101 (`POSITION_OFFSET`). A duplicate email is not re-added; the API returns `duplicate:true` with the existing position.
- `Invites` (optional, create it yourself): column A = codes you hand out (e.g. `NV-7F3K`). When a signup uses a
  code, column B is filled with the email, and that signup is counted in the **front queue** (its own #1, #2…).

## Slack message

`🆕 Waitlist #42 — someone@company.com` with a context line `🇰🇷 ko · total 57 · contrl.ai`.
Invited signups show `🎟️ Waitlist #3 (invite · front queue)`.

## Testing

```bash
curl -sL "$ENDPOINT" -H 'Content-Type: text/plain' \
  --data '{"email":"test@example.com","lang":"en","source":"curl"}'   # no -X POST: the 302 must become a GET
# → {"ok":true,"position":101,"invited":false,"invalidCode":false}
curl -sL "$ENDPOINT?invite=ABC123"   # → {"ok":true,"valid":false}  (invite-code Check button)
```
Delete the test row from the sheet afterwards (positions are computed from rows).
