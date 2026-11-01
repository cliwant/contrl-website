# Demo videos

The two landing-page videos are not screen recordings. They are self-playing HTML pages recorded headlessly:

- `problem.html` — hero video ("hand it everything" → 100 slides → page 12 → the night before)
- `replay.html` — "How Contrl works" video (Win Theme → key sentence → plan → 17 pages → one-note rewrite)

Captions, title cards and chat lines live in the `CAPS` dict inside each file (en/ko/ja/zh). The product UI (deck tool, Finder, slide, Contrl panel) is localized for ko/ja through the `UI` map (exact-text replacement at load); zh keeps the English UI with zh captions. `ui_i18n.py` is the script that generated the `UI` maps — edit the HTML `UI` JSON directly for small fixes.

```bash
npm install && npm run install-browser   # once
./record_all.sh                          # records 4 languages × 2 videos at 3200×2000 → images/hero/*.{lang}.mp4 + poster .jpg
```

`stills.js` renders the three "Why it fails" images (`images/why/*.jpg`) from `problem.html#still`.
Requires ffmpeg on PATH. Output paths are hard-coded in `record_all.sh`.
