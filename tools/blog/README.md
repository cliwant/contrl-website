# Blog posts

Each post is one file here: `tools/blog/posts/<slug>.html`. `tools/` is not deployed; run

    python3 tools/seo/build.py

to generate `blog/<slug>/index.html`, `blog/index.html`, `sitemap.xml` and `rss.xml` (the deploy
workflows run it too, but commit the output). Files starting with `_` are skipped (drafts).

The file starts with a JSON comment, then the article body as HTML (no `<h1>`; the title is the h1):

```html
<!--
{
  "slug": "compliance-vs-responsiveness",      // URL: /blog/<slug>/ (defaults to the file name)
  "lang": "en",                                  // en | ko | ja | zh
  "title": "…",                                  // <title>, h1, og:title — keep under ~65 characters if you can
  "description": "…",                            // meta description, ~150 characters
  "published": "2026-11-08",
  "updated": "2026-11-20",                       // optional; shown and used as dateModified
  "tags": ["APMP Foundation"],
  "series": "APMP Foundation, explained — EP01", // optional; shown above the title
  "author": {"name": "…", "title": "…", "url": "…"}, // optional; Person in JSON-LD (better E-E-A-T)
  "image": "/images/blog/…png",                  // optional; og:image, defaults to /og-image.png
  "summary": ["…", "…"],                         // key takeaways box at the top (HTML allowed)
  "faq": [{"q": "…", "a": "…"}]                  // FAQ section + FAQPage JSON-LD
}
-->
<p>Body…</p>
<h2>Section</h2>   <!-- h2s get ids and make the table of contents (3 or more) -->
```

Body helpers from `tools/blog/blog.css` (inlined into every blog page): `<div class="b-table"><table>…</table></div>` (scrolls on
phones), `<div class="b-compare"><div>…</div><div class="good">…</div></div>` (side-by-side),
`<div class="b-note">`, `<p class="b-source">` (sources / disclaimer line), `<blockquote>`.

GEO habits that help AI answers quote the post: answer the question in the first paragraph and
the summary, use real definitions, tables and numbered steps, keep FAQ answers self-contained,
and say where facts come from.
