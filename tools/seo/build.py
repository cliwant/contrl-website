#!/usr/bin/env python3
"""SEO / GEO build for contrl.ai. Standard library only; run from anywhere:

    python3 tools/seo/build.py

What it writes (all generated files say so at the top; edit the sources, not them):

1. Landing pages per language
   /index.html stays the hand-edited source (English). Its translations live in the page's own
   I18N / META objects and are applied by JS, which crawlers that don't run JS (Naver, most AI
   crawlers) never see. So this script prerenders /ko/, /ja/, /zh/ as static copies with the
   translated text, title, description, canonical and hreflang already in the HTML.
   It also fills the <!-- seo:start --> … <!-- seo:end --> block in the <head> of every landing
   page: hreflang links and JSON-LD (Organization, WebSite, SoftwareApplication with the
   pricing, FAQPage).

2. Blog
   Post sources live in tools/blog/posts/<slug>.html (tools/ is not deployed). Each starts with
   a JSON front-matter comment and continues with the article body HTML; see
   tools/blog/README.md. Files whose name starts with "_" are skipped (drafts, the example).
   Output: /blog/<slug>/index.html and /blog/index.html (only when at least one post exists).

3. sitemap.xml and rss.xml from the pages above.

The deploy workflows run this before deploying, so a forgotten run never ships stale pages;
still commit the output so the repository matches what is live.
"""
import html
import json
import re
import sys
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = 'https://contrl.ai'
APP = 'https://app.contrl.ai/'
LANGS = ['en', 'ko', 'ja', 'zh']
LOCALE = {'en': 'en_US', 'ko': 'ko_KR', 'ja': 'ja_JP', 'zh': 'zh_CN'}
NOTO = {'ja': 'Noto+Sans+JP', 'zh': 'Noto+Sans+SC'}
POSTS_DIR = ROOT / 'tools' / 'blog' / 'posts'
TODAY = date.today().isoformat()
BLOG_LANG = 'en'  # language of /blog/ (the index page) and rss.xml; posts carry their own "lang"


def landing_url(lang):
    return f'{SITE}/' if lang == 'en' else f'{SITE}/{lang}/'


def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def esc(s):
    return html.escape(s, quote=True)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding='utf-8') if path.exists() else None
    if old != text:
        path.write_text(text, encoding='utf-8')
        print('wrote', path.relative_to(ROOT))


def jsonld(obj):
    # "</" can't appear inside a <script> block
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


ORG = {
    '@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'Contrl', 'alternateName': ['contrl', 'CONTRL', '컨트롤'],
    'legalName': 'Cliwant', 'url': f'{SITE}/', 'logo': f'{SITE}/favicon.svg',
}


# --------------------------------------------------------------------------------------------
# Landing page
# --------------------------------------------------------------------------------------------
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


class I18nFinder(HTMLParser):
    """Finds the inner range of every element carrying data-i18n, and the start tags carrying
    data-i18n-<attr>, as character offsets into the source."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.line_starts = [0] + [m.end() for m in re.finditer('\n', src)]
        self.stack = []      # [tag, key or None, inner_start]
        self.ranges = []     # (inner_start, inner_end, key)
        self.attr_tags = []  # (tag_start, tag_end, {attr: key})

    def src_pos(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self.src_pos()
        end = start + len(self.get_starttag_text())
        a = dict(attrs)
        extra = {k[len('data-i18n-'):]: v for k, v in a.items() if k.startswith('data-i18n-')}
        if extra:
            self.attr_tags.append((start, end, extra))
        if tag not in VOID:
            self.stack.append([tag, a.get('data-i18n'), end])

    def handle_startendtag(self, tag, attrs):
        start = self.src_pos()
        a = dict(attrs)
        extra = {k[len('data-i18n-'):]: v for k, v in a.items() if k.startswith('data-i18n-')}
        if extra:
            self.attr_tags.append((start, start + len(self.get_starttag_text()), extra))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        pos = self.src_pos()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, key, inner = self.stack[i]
                if key:
                    self.ranges.append((inner, pos, key))
                del self.stack[i:]
                return


def set_attr(tag_text, name, value):
    v = esc(value)
    pat = re.compile(r'(\s' + re.escape(name) + r'=)"[^"]*"')
    if pat.search(tag_text):
        return pat.sub(lambda m: m.group(1) + '"' + v + '"', tag_text, count=1)
    return re.sub(r'\s*/?>$', lambda m: f' {name}="{v}"' + m.group(0), tag_text, count=1)


def load_landing():
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    i18n = json.loads(re.search(r'const I18N = (\{.*?\});\n', src).group(1))
    meta = json.loads(re.search(r'const META = (\{.*?\});\n', src).group(1))
    return src, i18n, meta


def tr(i18n, key, lang):
    v = i18n.get(key)
    if not v:
        return None
    return v[lang] if v.get(lang) is not None else v['en']


def landing_seo_block(lang, i18n, meta):
    lines = [f'<link rel="alternate" hreflang="{l}" href="{landing_url(l)}">' for l in LANGS]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{landing_url("en")}">')
    if (ROOT / 'blog' / 'index.html').exists() or list_posts():
        lines.append(f'<link rel="alternate" type="application/rss+xml" title="Contrl Blog" href="{SITE}/rss.xml">')
    t = lambda k: strip_tags(tr(i18n, k, lang) or '')
    url = landing_url(lang)
    offers = []
    for plan, price, slides in (('prf', '0', 'prf_slides'), ('prb', '20', 'prb_slides'), ('prp', '50', 'prp_slides')):
        o = {'@type': 'Offer', 'name': f'{t(plan + "_name")} — {t(slides)}', 'price': price, 'priceCurrency': 'USD',
             'url': f'{url}#pricing', 'availability': 'https://schema.org/InStock'}
        if price != '0':
            o['priceSpecification'] = {'@type': 'UnitPriceSpecification', 'price': price, 'priceCurrency': 'USD',
                                       'billingDuration': 'P1M', 'unitCode': 'MON'}
        offers.append(o)
    faqs = [{'@type': 'Question', 'name': t(f'faq{i}_q'),
             'acceptedAnswer': {'@type': 'Answer', 'text': t(f'faq{i}_a')}}
            for i in range(1, 20) if f'faq{i}_q' in i18n]
    graph = {'@context': 'https://schema.org', '@graph': [
        ORG,
        {'@type': 'WebSite', '@id': f'{SITE}/#website', 'url': f'{SITE}/', 'name': 'Contrl', 'publisher': {'@id': f'{SITE}/#org'},
         'inLanguage': LANGS},
        {'@type': 'WebPage', '@id': f'{url}#webpage', 'url': url, 'name': meta[lang]['title'], 'description': meta[lang]['desc'],
         'inLanguage': lang, 'isPartOf': {'@id': f'{SITE}/#website'}, 'about': {'@id': f'{SITE}/#app'},
         'primaryImageOfPage': f'{SITE}/og-image.png'},
        {'@type': 'SoftwareApplication', '@id': f'{SITE}/#app', 'name': 'Contrl', 'url': url,
         'applicationCategory': 'BusinessApplication', 'applicationSubCategory': 'Proposal writing software',
         'operatingSystem': 'Web', 'description': meta[lang]['desc'], 'image': f'{SITE}/og-image.png',
         'publisher': {'@id': f'{SITE}/#org'}, 'offers': offers,
         'featureList': [t(k) for k in ('prb_f1', 'prf_f2', 'prb_f3', 'prp_f2', 'chk1', 'chk2', 'chk3') if k in i18n]},
        {'@type': 'FAQPage', '@id': f'{url}#faq', 'inLanguage': lang, 'mainEntity': faqs},
    ]}
    lines.append(jsonld(graph))
    return '\n'.join('    ' + l for l in lines)


def fill_seo_block(src, block):
    return re.sub(r'(<!-- seo:start[^>]*-->\n).*?(\s*<!-- seo:end -->)', lambda m: m.group(1) + block + m.group(2), src, count=1, flags=re.S)


def render_landing(src, i18n, meta, lang):
    out = src
    if lang != 'en':
        f = I18nFinder(src)
        f.feed(src)
        edits = []  # (start, end, replacement)
        chosen = []
        for s, e, key in sorted(f.ranges):
            if any(cs <= s and e <= ce for cs, ce in chosen):
                continue  # inside an element that is itself replaced (JS does the same: outer wins)
            v = tr(i18n, key, lang)
            if v is None:
                continue
            chosen.append((s, e))
            edits.append((s, e, v))
        for s, e, attrs in f.attr_tags:
            tag = src[s:e]
            new = tag
            for attr, key in attrs.items():
                v = tr(i18n, key, lang)
                if v is not None:
                    new = set_attr(new, attr, re.sub(r'<[^>]+>', '', v))
            if new != tag:
                edits.append((s, e, new))
        for s, e, v in sorted(edits, reverse=True):
            out = out[:s] + v + out[e:]

        m = meta[lang]
        url = landing_url(lang)
        out = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', out, count=1)
        out = re.sub(r'<title>.*?</title>', f'<title>{esc(m["title"])}</title>', out, count=1, flags=re.S)
        for sel, val in ((r'name="description"', m['desc']), (r'property="og:title"', m['title']), (r'name="twitter:title"', m['title']),
                         (r'property="og:description"', m['desc']), (r'name="twitter:description"', m['desc']),
                         (r'property="og:url"', url), (r'property="og:locale"', LOCALE[lang])):
            out = re.sub(r'(<meta ' + sel + r' content=)"[^"]*"', lambda mm: mm.group(1) + '"' + esc(val) + '"', out, count=1)
        out = re.sub(r'(<link rel="canonical" href=)"[^"]*"', lambda mm: mm.group(1) + f'"{url}"', out, count=1)
        out = out.replace('href="/en/" class="text-xl font-bold', f'href="/{lang}/" class="text-xl font-bold')
        still = lang if lang in ('ko', 'ja') else 'en'
        out = re.sub(r'(/images/why/still-[a-z-]+)\.en\.jpg', lambda mm: f'{mm.group(1)}.{still}.jpg', out)
        out = re.sub(r'(/images/hero/[a-z-]+)\.en\.jpg', lambda mm: f'{mm.group(1)}.{lang}.jpg', out)
        out = re.sub(r'(<button[^>]*data-lang="' + lang + r'")', r'\1 class="on"', out)
        if lang in NOTO:
            font = (f'    <link id="noto-{lang}" rel="stylesheet" href="https://fonts.googleapis.com/css2?family={NOTO[lang]}'
                    ':wght@400;500;600;700;800;900&display=swap">\n')
            out = out.replace('    <!-- seo:end -->', '    <!-- seo:end -->\n' + font.rstrip('\n'), 1)
        out = out.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n<!-- GENERATED by tools/seo/build.py from /index.html — edit /index.html, then run the script. -->\n', 1)
    return fill_seo_block(out, landing_seo_block(lang, i18n, meta))


def build_landing(blog_index_langs=()):
    src, i18n, meta = load_landing()
    if '<!-- seo:start' not in src:
        sys.exit('index.html has no <!-- seo:start --> block in <head>')
    write(ROOT / 'index.html', render_landing(src, i18n, meta, 'en'))
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    for lang in LANGS[1:]:
        page = render_landing(src, i18n, meta, lang)
        if lang in blog_index_langs:
            page = page.replace('href="/blog/"', f'href="{blog_base(lang)}"')
        write(ROOT / lang / 'index.html', page)


# --------------------------------------------------------------------------------------------
# Blog
# --------------------------------------------------------------------------------------------
BLOG_UI = {
    'ko': {'blog': '블로그', 'blog_title': 'Contrl 블로그 — 제안서·입찰 실무 가이드',
           'blog_desc': '공공입찰 제안서, RFP 분석, Win Theme, 평가표 대응까지. 제안서를 쓰는 사람을 위한 실무 가이드.',
           'cta_t': '제안서, 사람이 정하고 AI가 쓰게 하세요', 'cta_p': 'RFP를 올리면 Contrl이 분석부터 전략, 슬라이드까지 함께 만듭니다. 첫 제안서는 무료예요.',
           'cta_b': '무료로 시작하기', 'start': '무료로 시작하기', 'updated': '업데이트', 'published': '작성', 'toc': '목차',
           'summary': '핵심 요약', 'faq': '자주 묻는 질문', 'min': '분 읽기', 'all': '모든 글', 'empty': '아직 글이 없습니다.'},
    'en': {'blog': 'Blog', 'blog_title': 'Contrl Blog — Practical guides for proposals and bids',
           'blog_desc': 'RFP analysis, win themes, scoring tables and more: practical guides for people who write proposals.',
           'cta_t': 'You make the call. AI writes the proposal.', 'cta_p': 'Upload an RFP and Contrl works through it with you, from analysis and strategy to the slides. Your first proposal is free.',
           'cta_b': 'Get started free', 'start': 'Get started free', 'updated': 'Updated', 'published': 'Published', 'toc': 'Contents',
           'summary': 'Key takeaways', 'faq': 'FAQ', 'min': 'min read', 'all': 'All posts', 'empty': 'No posts yet.'},
}
BLOG_UI['ja'] = {'blog': 'ブログ', 'blog_title': 'Contrl ブログ — 提案書・入札の実務ガイド',
                 'blog_desc': 'RFP分析、ウィンテーマ、評価基準への対応まで。提案書を書く人のための実務ガイド。',
                 'cta_t': '判断は人が、作成はAIが。', 'cta_p': 'RFPをアップロードすると、Contrlが分析・戦略からスライド作成まで一緒に進めます。最初の提案書は無料です。',
                 'cta_b': '無料で始める', 'start': '無料で始める', 'updated': '更新', 'published': '公開', 'toc': '目次',
                 'summary': '要点', 'faq': 'よくある質問', 'min': '分で読めます', 'all': 'すべての記事', 'empty': 'まだ記事がありません。'}
BLOG_UI['zh'] = {'blog': '博客', 'blog_title': 'Contrl 博客 — 投标与提案书实务指南',
                 'blog_desc': '从RFP分析、制胜主题到评分标准应对：写给提案书撰写者的实务指南。',
                 'cta_t': '由你决策，由AI撰写。', 'cta_p': '上传RFP，Contrl会与你一起完成从分析、策略到幻灯片的全过程。第一份提案书免费。',
                 'cta_b': '免费开始', 'start': '免费开始', 'updated': '更新于', 'published': '发布于', 'toc': '目录',
                 'summary': '要点', 'faq': '常见问题', 'min': '分钟阅读', 'all': '全部文章', 'empty': '暂无文章。'}
LANG_NAME = {'en': 'English', 'ko': '한국어', 'ja': '日本語', 'zh': '中文'}


def blog_base(lang):
    """Path of a language's blog: /blog/ for English, /<lang>/blog/ for the others (next to /<lang>/)."""
    return '/blog/' if lang == 'en' else f'/{lang}/blog/'


def list_posts():
    if not POSTS_DIR.exists():
        return []
    posts = []
    for f in sorted(POSTS_DIR.glob('*.html')):
        if f.name.startswith('_'):
            continue
        posts.append(parse_post(f))
    posts.sort(key=lambda p: p['published'], reverse=True)
    return posts


def parse_post(f):
    text = f.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--(.*?)-->\s*', text, re.S)
    if not m:
        sys.exit(f'{f}: missing the JSON front-matter comment at the top')
    try:
        fm = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f'{f}: front matter is not valid JSON: {e}')
    for k in ('title', 'description', 'published'):
        if not fm.get(k):
            sys.exit(f'{f}: front matter needs "{k}"')
    # <slug>.html is the English post; <slug>.<lang>.html its translation (same slug, linked by hreflang)
    stem, _, suffix = f.stem.partition('.')
    fm.setdefault('slug', stem)
    fm.setdefault('lang', suffix or 'en')
    fm['file'] = f'tools/blog/posts/{f.name}'
    if fm['lang'] not in LANGS:
        sys.exit(f'{f}: lang must be one of {LANGS}')
    fm.setdefault('updated', fm['published'])
    fm.setdefault('tags', [])
    fm.setdefault('faq', [])
    fm.setdefault('summary', [])
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', fm['slug']):
        sys.exit(f'{f}: slug must be lowercase letters, digits and hyphens')
    fm['body'] = text[m.end():]
    fm['path'] = f'{blog_base(fm["lang"])}{fm["slug"]}/'
    fm['url'] = SITE + fm['path']
    chars = len(strip_tags(fm['body']))
    fm['minutes'] = max(1, round(chars / (500 if fm['lang'] in ('ko', 'ja', 'zh') else 1200)))
    return fm


BLOG_HEAD = '''<!DOCTYPE html>
<!-- GENERATED by tools/seo/build.py — edit {source}, then run the script. -->
<html lang="{lang}">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-RP629LFPHJ"></script>
    <script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', 'G-RP629LFPHJ');</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="alternate" type="application/rss+xml" title="Contrl Blog" href="{site}/rss.xml">
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Contrl">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{image}">
    <meta property="og:locale" content="{locale}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{image}">
{extra_meta}    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css">
    <style>{css}</style>
    {ld}
</head>
<body>
    <header class="b-nav"><div class="b-wrap b-nav-in">
        <a class="b-logo" href="{home}">contrl<span>.</span></a>
        <nav><a href="{blog_home}">{ui_blog}</a><a class="b-btn" href="{home}#join">{ui_start}</a></nav>
    </div></header>
'''

def blog_css():
    # Inlined, not linked: contrl.ai sits behind CloudFront, which caches /assets/* for an hour and
    # ignores query strings, so a changed stylesheet would reach visitors up to an hour after the
    # HTML (which is no-cache). Inlining ships the CSS with the page. The source is tools/blog/blog.css.
    css = (ROOT / 'tools' / 'blog' / 'blog.css').read_text(encoding='utf-8')
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return re.sub(r'\s*\n\s*', '', css).replace('</', '<\\/')


BLOG_FOOT = '''    <footer class="b-foot"><div class="b-wrap">
        <a class="b-logo" href="{home}">contrl<span>.</span></a>
        <p>&copy; {year} Contrl by Cliwant. All rights reserved.</p>
    </div></footer>
</body>
</html>
'''


def slugify_heading(text, used):
    base = re.sub(r'[^\w가-힣ぁ-んァ-ン一-龥-]+', '-', strip_tags(text).lower()).strip('-') or 'section'
    s, n = base, 2
    while s in used:
        s, n = f'{base}-{n}', n + 1
    used.add(s)
    return s


def add_heading_ids(body):
    used, toc = set(), []

    def fix(m):
        level, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'\sid="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify_heading(inner, used)
        if level == '2':
            toc.append((hid, strip_tags(inner)))
        if not idm:
            attrs += f' id="{hid}"'
        return f'<h{level}{attrs}>{inner}</h{level}>'
    body = re.sub(r'<h([23])([^>]*)>(.*?)</h\1>', fix, body, flags=re.S)
    return body, toc


def fmt_date(d, lang):
    y, m, dd = d.split('-')
    return f'{y}. {int(m)}. {int(dd)}.' if lang == 'ko' else d


def hreflang_links(alts):
    """alts: {lang: absolute url}. Returns <link> lines for the head (empty when there is one language)."""
    if len(alts) < 2:
        return ''
    lines = [f'    <link rel="alternate" hreflang="{l}" href="{u}">\n' for l, u in sorted(alts.items())]
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="{alts.get("en") or next(iter(alts.values()))}">\n')
    return ''.join(lines)


def cjk_font(lang):
    """Pretendard covers Latin and Hangul only; ja/zh pages also load Noto Sans JP/SC."""
    if lang not in NOTO:
        return ''
    return (f'    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={NOTO[lang]}:wght@400;600;700;800&display=swap">\n'
            f'    <style>body{{font-family:\'Pretendard\',\'{NOTO[lang].replace("+", " ")}\',sans-serif}}</style>\n')


def lang_switch(alts, current):
    if len(alts) < 2:
        return ''
    links = [f'<a href="{u.replace(SITE, "")}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == current else ""}>{LANG_NAME[l]}</a>'
             for l, u in sorted(alts.items(), key=lambda kv: LANGS.index(kv[0]))]
    return '<span class="b-langs">' + ''.join(links) + '</span>'


def render_post(p, alts):
    lang = p['lang']
    ui = BLOG_UI.get(lang, BLOG_UI['en'])
    home = landing_url(lang).replace(SITE, '')
    image = p.get('image') or f'{SITE}/og-image.png'
    if image.startswith('/'):
        image = SITE + image
    body, toc = add_heading_ids(p['body'])
    author = p.get('author')
    author_ld = ({'@type': 'Person', 'name': author['name'], **({'url': author['url']} if author.get('url') else {}),
                  **({'jobTitle': author['title']} if author.get('title') else {}), 'worksFor': {'@id': f'{SITE}/#org'}}
                 if author else {'@id': f'{SITE}/#org'})
    graph = [
        ORG,
        {'@type': 'BlogPosting', '@id': f'{p["url"]}#article', 'headline': p['title'], 'description': p['description'],
         'url': p['url'], 'mainEntityOfPage': p['url'], 'inLanguage': lang, 'datePublished': p['published'],
         'dateModified': p['updated'], 'image': image, 'author': author_ld, 'publisher': {'@id': f'{SITE}/#org'},
         'keywords': p['tags'], 'wordCount': len(strip_tags(p['body']).split()),
         'isPartOf': {'@type': 'Blog', '@id': f'{SITE}{blog_base(lang)}#blog', 'name': 'Contrl Blog', 'url': f'{SITE}{blog_base(lang)}'},
         **({'translationOfWork': {'@id': alts['en'] + '#article'}} if lang != 'en' and 'en' in alts else {}),
         'about': {'@type': 'SoftwareApplication', '@id': f'{SITE}/#app', 'name': 'Contrl'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Contrl', 'item': landing_url(lang)},
            {'@type': 'ListItem', 'position': 2, 'name': ui['blog'], 'item': f'{SITE}{blog_base(lang)}'},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': p['url']}]},
    ]
    if p['faq']:
        graph.append({'@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': [
            {'@type': 'Question', 'name': strip_tags(q['q']), 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(q['a'])}}
            for q in p['faq']]})
    extra = (f'    <meta property="article:published_time" content="{p["published"]}">\n'
             f'    <meta property="article:modified_time" content="{p["updated"]}">\n'
             + ''.join(f'    <meta property="article:tag" content="{esc(t)}">\n' for t in p['tags'])
             + hreflang_links(alts) + cjk_font(lang))
    head = BLOG_HEAD.format(source=p['file'], lang=lang, title=esc(p['title']), desc=esc(p['description']),
                            url=p['url'], site=SITE, og_type='article', image=image, locale=LOCALE.get(lang, 'ko_KR'),
                            extra_meta=extra, ld=jsonld({'@context': 'https://schema.org', '@graph': graph}), css=blog_css(),
                            home=home, ui_blog=ui['blog'], ui_start=ui['start'], blog_home=blog_base(lang))
    parts = [head, '    <main class="b-wrap b-post">\n']
    parts.append(f'        <div class="b-crumb"><nav><a href="{blog_base(lang)}">{ui["blog"]}</a>'
                 + (f' · <span>{esc(p.get("series") or p["tags"][0])}</span>' if p.get('series') or p['tags'] else '') + '</nav>'
                 + lang_switch(alts, lang) + '</div>\n')
    parts.append(f'        <h1>{esc(p["title"])}</h1>\n')
    by = f'{esc(author["name"])} · ' if author else ''
    dates = f'<time datetime="{p["published"]}">{fmt_date(p["published"], lang)}</time>'
    if p['updated'] != p['published']:
        dates += f' · {ui["updated"]} <time datetime="{p["updated"]}">{fmt_date(p["updated"], lang)}</time>'
    parts.append(f'        <p class="b-meta">{by}{dates} · {p["minutes"]}{ui["min"] if lang != "en" else " " + ui["min"]}</p>\n')
    if p['summary']:
        parts.append(f'        <aside class="b-summary"><p class="b-label">{ui["summary"]}</p><ul>'
                     + ''.join(f'<li>{s}</li>' for s in p['summary']) + '</ul></aside>\n')
    if len(toc) >= 3:
        parts.append(f'        <nav class="b-toc"><p class="b-label">{ui["toc"]}</p><ol>'
                     + ''.join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc) + '</ol></nav>\n')
    parts.append('        <article class="b-body">\n' + body.strip() + '\n        </article>\n')
    if p['faq']:
        parts.append(f'        <section class="b-faq"><h2 id="faq">{ui["faq"]}</h2>'
                     + ''.join(f'<details><summary>{q["q"]}</summary><div>{q["a"]}</div></details>' for q in p['faq'])
                     + '</section>\n')
    parts.append(f'        <section class="b-cta"><h2>{ui["cta_t"]}</h2><p>{ui["cta_p"]}</p>'
                 f'<a class="b-btn" href="{home}#join">{ui["cta_b"]} →</a></section>\n')
    parts.append('    </main>\n')
    parts.append(BLOG_FOOT.format(home=home, year=p['published'][:4]))
    return ''.join(parts)


def render_blog_index(posts, lang, index_langs):
    ui = BLOG_UI[lang]
    url = f'{SITE}{blog_base(lang)}'
    alts = {l: f'{SITE}{blog_base(l)}' for l in index_langs}
    graph = [ORG, {'@type': 'Blog', '@id': f'{url}#blog', 'name': 'Contrl Blog', 'url': url, 'description': ui['blog_desc'],
                   'inLanguage': sorted({p['lang'] for p in posts}) or [lang], 'publisher': {'@id': f'{SITE}/#org'},
                   'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': p['url'], 'datePublished': p['published']}
                                for p in posts]}]
    head = BLOG_HEAD.format(source='tools/blog/posts/', lang=lang, title=esc(ui['blog_title']), desc=esc(ui['blog_desc']),
                            url=url, site=SITE, og_type='website', image=f'{SITE}/og-image.png', locale=LOCALE[lang],
                            extra_meta=hreflang_links(alts) + cjk_font(lang), ld=jsonld({'@context': 'https://schema.org', '@graph': graph}), css=blog_css(),
                            home=landing_url(lang).replace(SITE, ''), ui_blog=ui['blog'], ui_start=ui['start'], blog_home=blog_base(lang))
    items = []
    for p in posts:
        thumb = (f'<div class="b-thumb"><img src="{esc(p["image"])}" alt="" width="1344" height="752" loading="lazy" decoding="async"></div>'
                 if p.get('image', '').startswith('/') else '')
        kicker = esc(p.get('series') or (p['tags'][0] if p['tags'] else ''))
        read = f'{p["minutes"]} {ui["min"]}' if lang == 'en' else f'{p["minutes"]}{ui["min"]}'
        items.append(f'''        <li><a class="b-card{" has-thumb" if thumb else ""}" href="{p["path"]}">
            {thumb}<div class="b-card-body">
                {f'<p class="b-kicker">{kicker}</p>' if kicker else ''}
                <h2>{esc(p["title"])}</h2>
                <p class="b-desc">{esc(p["description"])}</p>
                <p class="b-meta"><time datetime="{p["published"]}">{fmt_date(p["published"], p["lang"])}</time> · {read}</p>
            </div>
        </a></li>''')
    body = (f'    <main class="b-wrap b-index">\n        <div class="b-crumb">{lang_switch(alts, lang)}</div>\n        <h1>{ui["blog"]}</h1>\n        <p class="b-lede">{ui["blog_desc"]}</p>\n'
            f'        <ul class="b-list">\n' + '\n'.join(items) + '\n        </ul>\n    </main>\n')
    return head + body + BLOG_FOOT.format(home=landing_url(lang).replace(SITE, ''), year=TODAY[:4])


def translations(posts):
    groups = {}
    for p in posts:
        groups.setdefault(p['slug'], {})[p['lang']] = p['url']
    return groups


def blog_langs(posts):
    return [l for l in LANGS if any(p['lang'] == l for p in posts)]


def build_blog(posts):
    groups = translations(posts)
    index_langs = blog_langs(posts)
    for p in posts:
        write(ROOT / p['path'].strip('/') / 'index.html', render_post(p, groups[p['slug']]))
    for lang in LANGS:
        blog = ROOT / blog_base(lang).strip('/')
        live = {p['slug'] for p in posts if p['lang'] == lang}
        if not blog.exists():
            continue
        generated = lambda f: f.exists() and 'GENERATED by tools/seo/build.py' in f.read_text(encoding='utf-8')[:300]
        for d in blog.iterdir():
            if d.is_dir() and d.name not in live and generated(d / 'index.html'):
                (d / 'index.html').unlink()
                d.rmdir()
                print('removed', d.relative_to(ROOT))
        if lang in index_langs:
            write(blog / 'index.html', render_blog_index([p for p in posts if p['lang'] == lang], lang, index_langs))
        elif generated(blog / 'index.html'):
            (blog / 'index.html').unlink()
            print('removed', (blog / 'index.html').relative_to(ROOT))


# --------------------------------------------------------------------------------------------
# sitemap.xml / rss.xml
# --------------------------------------------------------------------------------------------
def git_lastmod(path):
    import subprocess
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(path)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return out or TODAY
    except OSError:
        return TODAY


def build_sitemap(posts):
    lastmod = git_lastmod(ROOT / 'index.html')
    alts = ''.join(f'\n        <xhtml:link rel="alternate" hreflang="{l}" href="{landing_url(l)}"/>' for l in LANGS) \
        + f'\n        <xhtml:link rel="alternate" hreflang="x-default" href="{landing_url("en")}"/>'
    urls = []
    for l in LANGS:
        urls.append(f'''    <url>
        <loc>{landing_url(l)}</loc>
        <lastmod>{lastmod}</lastmod>{alts}
        <image:image><image:loc>{SITE}/og-image.png</image:loc></image:image>
    </url>''')
    def xalts(alts):
        if len(alts) < 2:
            return ''
        return ''.join(f'\n        <xhtml:link rel="alternate" hreflang="{l}" href="{u}"/>' for l, u in sorted(alts.items())) \
            + f'\n        <xhtml:link rel="alternate" hreflang="x-default" href="{alts.get("en") or next(iter(alts.values()))}"/>'
    index_langs = blog_langs(posts)
    index_alts = {l: f'{SITE}{blog_base(l)}' for l in index_langs}
    for l in index_langs:
        urls.append(f'''    <url>
        <loc>{SITE}{blog_base(l)}</loc>
        <lastmod>{max(p["updated"] for p in posts if p["lang"] == l)}</lastmod>{xalts(index_alts)}
    </url>''')
    groups = translations(posts)
    for p in posts:
        img = f'\n        <image:image><image:loc>{SITE}{p["image"]}</image:loc></image:image>' if p.get('image', '').startswith('/') else ''
        urls.append(f'''    <url>
        <loc>{p["url"]}</loc>
        <lastmod>{p["updated"]}</lastmod>{xalts(groups[p["slug"]])}{img}
    </url>''')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- GENERATED by tools/seo/build.py -->\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml"\n'
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           + '\n'.join(urls) + '\n</urlset>\n')
    write(ROOT / 'sitemap.xml', xml)


def rfc822(d):
    return datetime.fromisoformat(d).replace(hour=9, tzinfo=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')


def build_rss(posts):
    posts = [p for p in posts if p['lang'] == BLOG_LANG]
    items = []
    for p in posts[:50]:
        cats = ''.join(f'\n            <category>{esc(t)}</category>' for t in p['tags'])
        items.append(f'''        <item>
            <title>{esc(p["title"])}</title>
            <link>{p["url"]}</link>
            <guid isPermaLink="true">{p["url"]}</guid>
            <description>{esc(p["description"])}</description>
            <pubDate>{rfc822(p["published"])}</pubDate>
            <dc:creator>{esc(p["author"]["name"]) if p.get("author") else "Contrl"}</dc:creator>{cats}
        </item>''')
    built = rfc822(max([p['updated'] for p in posts], default=git_lastmod(ROOT / 'index.html')))
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- GENERATED by tools/seo/build.py -->
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <channel>
        <title>Contrl Blog</title>
        <link>{SITE}/blog/</link>
        <description>{esc(BLOG_UI[BLOG_LANG]["blog_desc"])}</description>
        <language>{BLOG_LANG}</language>
        <lastBuildDate>{built}</lastBuildDate>
        <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>
''' + '\n'.join(items) + ('\n' if items else '') + '''    </channel>
</rss>
'''
    write(ROOT / 'rss.xml', xml)


def main():
    posts = list_posts()
    keys = [(p['slug'], p['lang']) for p in posts]
    if len(keys) != len(set(keys)):
        sys.exit('two posts share a slug and language')
    build_blog(posts)
    build_landing(blog_langs(posts))
    build_sitemap(posts)
    build_rss(posts)


if __name__ == '__main__':
    main()
