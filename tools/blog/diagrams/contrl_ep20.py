#!/usr/bin/env python3
"""EP20 (Page and Document Design) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep20.py
Writes images/blog/page-and-document-design/contrl-one-template.svg (en) and .<lang>.svg (ko/ja/zh).

One design-system card feeds a wall of slides from four sections finished on different days.
The content of each slide differs; dashed guides run straight across every slide in a row to
show that header, margins and footer line up everywhere.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'page-and-document-design', 'contrl-one-template'
H = 560

T = {
    'en': dict(
        title='Four proposal sections finished on different days, eight slides with different content, all drawn in one company design system: the header bar, margins and footer line up across every slide, and each slide cites the RFP requirement it answers',
        card='Your company’s design system', items=['Colors', 'Fonts', 'Layout'],
        top='Each section has its own key sentence and plan',
        days=['Section 1 · day 3', 'Section 2 · day 6', 'Section 3 · day 8', 'Section 4 · last day'],
        req='Req.', guide='Same header, margins and footer on every slide',
        foot='Written at different times, one template on every page. Nothing to reformat at the end.'),
    'ko': dict(
        title='서로 다른 날 완성된 네 섹션의 슬라이드 여덟 장. 내용은 모두 다르지만 하나의 회사 디자인 시스템으로 그려져 머리 띠, 여백, 바닥글이 모든 슬라이드에서 나란히 맞고, 슬라이드마다 대응하는 제안요청서 요구사항을 밝힌다',
        card='회사 디자인 시스템', items=['색', '글꼴', '레이아웃'],
        top='섹션마다 핵심 문장과 전개는 따로',
        days=['섹션 1 · 3일째', '섹션 2 · 6일째', '섹션 3 · 8일째', '섹션 4 · 마지막 날'],
        req='요구사항', guide='모든 슬라이드에서 같은 머리 띠, 여백, 바닥글',
        foot='쓴 날은 달라도 모든 페이지가 같은 템플릿입니다. 마지막에 서식을 맞출 일이 없습니다.'),
    'ja': dict(
        title='別々の日に仕上がった4つのセクションのスライド8枚。内容はすべて違うが、一つの自社デザインシステムで描かれているため、ヘッダーの帯、余白、フッターがすべてのスライドでそろい、各スライドが対応するRFP要件を示す',
        card='自社のデザイン\nシステム', items=['色', 'フォント', 'レイアウト'],
        top='キーセンテンスと展開はセクションごと',
        days=['セクション1・3日目', 'セクション2・6日目', 'セクション3・8日目', 'セクション4・最終日'],
        req='要件', guide='どのスライドも同じヘッダー、余白、フッター',
        foot='書いた日は違っても、全ページが同じテンプレートです。最後に体裁をそろえる作業はありません。'),
    'zh': dict(
        title='四个章节在不同日期完成，八页幻灯片内容各不相同，但都用同一套公司设计体系绘制：页眉色条、页边距和页脚在每一页上对齐，每页注明所回应的招标需求',
        card='贵公司的设计体系', items=['颜色', '字体', '版式'],
        top='每个章节各有核心句和展开方案',
        days=['第1节 · 第3天', '第2节 · 第6天', '第3节 · 第8天', '第4节 · 最后一天'],
        req='需求', guide='每页相同的页眉、页边距和页脚',
        foot='写作时间不同，每一页却是同一个模板，最后无需再统一格式。'),
}

CX, CY, CWD, CH = 40, 150, 250, 270          # design-system card
SX = [390, 584, 778, 972]                     # slide columns
SW_, SH = 172, 112
RY = [150, 308]                               # slide rows
REQS = [['2.1', '3.4', '4.2', '5.1'], ['2.3', '3.6', '4.5', '5.3']]


def slide(s, x, y, kind, req, lang):
    s.rect(x, y, SW_, SH, '#fff', LINE, r=6, sw=1.2)
    s.rect(x, y, SW_, 8, ACCENT, r=0)                       # header band
    s.rect(x + 12, y + 18, SW_ * 0.62, 7, INK, r=3)          # headline
    bx, by = x + 12, y + 34
    if kind == 0:   # bar chart
        for k, hh in enumerate([14, 22, 18, 32]):
            s.rect(bx + 4 + k * 18, by + 38 - hh, 12, hh, ACCENT if k == 3 else GRAY_BOX, r=2)
        for k in range(3):
            s.rect(bx + 86, by + 6 + k * 12, 60, 5, GRAY_BOX, r=2)
    elif kind == 1:  # table
        s.rect(bx, by, SW_ - 24, 40, '#fff', GRAY_TXT, r=2, sw=1)
        s.rect(bx, by, SW_ - 24, 10, GRAY_BOX, r=0)
        for k in (1, 2):
            xx = bx + (SW_ - 24) * k / 3
            s.out.append(f'<line x1="{xx:.1f}" y1="{by}" x2="{xx:.1f}" y2="{by + 40}" stroke="{GRAY_TXT}" stroke-width="1"/>')
        for k in (1, 2):
            yy = by + 10 + 10 * k
            s.out.append(f'<line x1="{bx}" y1="{yy}" x2="{bx + SW_ - 24}" y2="{yy}" stroke="{GRAY_TXT}" stroke-width="1"/>')
    elif kind == 2:  # timeline
        yy = by + 18
        s.out.append(f'<line x1="{bx}" y1="{yy}" x2="{bx + SW_ - 24}" y2="{yy}" stroke="{GRAY_TXT}" stroke-width="2"/>')
        for k in range(4):
            cx = bx + 10 + k * (SW_ - 44) / 3
            s.out.append(f'<circle cx="{cx:.1f}" cy="{yy}" r="6" fill="{ACCENT if k == 2 else GRAY_BOX}"/>')
            s.rect(cx - 12, yy + 12, 24, 4, GRAY_BOX, r=2)
    else:            # text + callout
        for k, f in enumerate([0.55, 0.5, 0.45]):
            s.rect(bx, by + 4 + k * 12, (SW_ - 24) * f, 5, GRAY_BOX, r=2)
        s.rect(bx + (SW_ - 24) * 0.62, by, (SW_ - 24) * 0.38, 38, PEACH, ACCENT, r=4, sw=1)
    # footer: rule + requirement chip
    fy = y + SH - 16
    s.out.append(f'<line x1="{x + 12}" y1="{fy - 6}" x2="{x + SW_ - 12}" y2="{fy - 6}" stroke="{LINE}" stroke-width="1"/>')
    lab = f'{req}'
    s.text(x + 12, fy + 7, lab, fs=10, weight=700, fill=ACCENT_INK)


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)

    # header line over the slide wall
    s.text(SX[0], 52, t['top'], fs=18, weight=800)
    for i, d in enumerate(t['days']):
        s.text(SX[i], 96, d, fs=13, weight=700, fill=MUTED)
        s.out.append(f'<line x1="{SX[i]}" y1="{106}" x2="{SX[i] + SW_}" y2="{106}" stroke="{LINE}" stroke-width="2"/>')

    # design-system card
    s.rect(CX, CY, CWD, CH, CREAM, ACCENT, r=14, sw=2)
    ty = s.text(CX + 22, CY + 40, t['card'], fs=19, weight=800, maxw=CWD - 44, lh=1.3)
    rows_y = max(ty + 10, CY + 96)
    # colors
    for k, c in enumerate([ACCENT, INK, GRAY_BOX, '#fff']):
        s.out.append(f'<rect x="{CX + 22 + k * 30}" y="{rows_y}" width="24" height="24" rx="6" fill="{c}" stroke="{LINE}" stroke-width="1"/>')
    s.text(CX + 150, rows_y + 18, t['items'][0], fs=14, weight=700, fill=MUTED)
    # fonts
    s.text(CX + 22, rows_y + 74, 'Aa', fs=30, weight=800)
    s.text(CX + 150, rows_y + 66, t['items'][1], fs=14, weight=700, fill=MUTED)
    # layout: mini master page with dashed margins
    ly = rows_y + 100
    s.rect(CX + 22, ly, 108, 62, '#fff', GRAY_TXT, r=4, sw=1.2)
    s.rect(CX + 22, ly, 108, 7, ACCENT, r=0)
    s.rect(CX + 30, ly + 13, 92, 40, 'none', ACCENT, r=0, sw=1, dash='3 3')
    s.text(CX + 150, ly + 36, t['items'][2], fs=14, weight=700, fill=MUTED)

    # feed: card -> bus -> each row
    bus = 352
    mid = CY + CH / 2
    s.out.append(f'<line x1="{CX + CWD}" y1="{mid}" x2="{bus}" y2="{mid}" stroke="{ACCENT}" stroke-width="3"/>')
    s.out.append(f'<line x1="{bus}" y1="{RY[0] + SH / 2}" x2="{bus}" y2="{RY[1] + SH / 2}" stroke="{ACCENT}" stroke-width="3"/>')
    for ry in RY:
        s.arrow(bus, ry + SH / 2, SX[0] - 8, ry + SH / 2)

    # slides
    for r, ry in enumerate(RY):
        for c, sx in enumerate(SX):
            kind = (c + 2 * r) % 4
            slide(s, sx, ry, kind, f"{t['req']} {REQS[r][c]}", lang)
        # alignment guides running across the whole row
        for gy in (ry + 8, ry + 30, ry + SH - 22):
            s.out.append(f'<line x1="{SX[0] - 4}" y1="{gy}" x2="{SX[-1] + SW_ + 14}" y2="{gy}" stroke="{ACCENT}" stroke-width="1.2" stroke-dasharray="5 4" opacity="0.85"/>')

    # guide legend
    ly = RY[1] + SH + 34
    s.out.append(f'<line x1="{SX[0]}" y1="{ly - 5}" x2="{SX[0] + 40}" y2="{ly - 5}" stroke="{ACCENT}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    s.text(SX[0] + 52, ly, t['guide'], fs=14, weight=700, fill=ACCENT_INK)

    s.text(40, 512, t['foot'], fs=17, fill=MUTED, maxw=1100, lh=1.45)
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
