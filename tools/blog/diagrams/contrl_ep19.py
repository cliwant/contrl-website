#!/usr/bin/env python3
"""EP19 (Graphics) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep19.py
Writes images/blog/graphics/contrl-sentence-to-page.svg (en) and .<lang>.svg (ko/ja/zh).

Three frames of rising fidelity: the key sentence you pick, the plan you pick (a dashed
wireframe of page blocks), and the finished slide drawn in your design system.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'graphics', 'contrl-sentence-to-page'
H = 560

T = {
    'en': dict(
        title='One section taking shape in Contrl, from rough to finished: first you pick one of three key sentences, then one of three plans for the section, and only then does Contrl draw the slide in your design system, citing the RFP requirement it answers',
        steps=[('The sentence', 'You pick 1 of 3 key sentences'),
               ('The plan', 'You pick 1 of 3 plans'),
               ('The page', 'Contrl draws the slides')],
        key='Riders keep paying the old way until the new system runs clean',
        key2='Riders keep paying the old way\nuntil the new system runs clean',
        plans='Plan', pages=['p. 1', 'p. 2–3', 'p. 4'],
        old='Old fares', new='New fares', mark='30 clean days',
        chip='Answers RFP req. 4.2',
        ds='Your design system', foot='The message is settled before anything is drawn; the template keeps every page consistent.'),
    'ko': dict(
        title='Contrl에서 한 섹션이 거친 단계에서 완성으로 가는 과정: 먼저 핵심 문장 후보 셋 중 하나를 고르고, 섹션 전개안 셋 중 하나를 고른 뒤에야 Contrl이 회사 디자인 시스템으로 슬라이드를 그리며, 페이지마다 대응하는 제안요청서 요구사항을 밝힌다',
        steps=[('문장', '핵심 문장 후보 3개 중 선택'),
               ('전개', '전개안 3개 중 선택'),
               ('페이지', 'Contrl이 슬라이드 작성')],
        key='새 시스템이 안정될 때까지 승객은 지금 방식 그대로 요금을 냅니다',
        key2='새 시스템이 안정될 때까지\n승객은 지금 방식 그대로',
        plans='전개안', pages=['1쪽', '2–3쪽', '4쪽'],
        old='기존 요금 시스템', new='새 요금 시스템', mark='오류 없는 30일',
        chip='제안요청서 요구사항 4.2 대응',
        ds='회사 디자인 시스템', foot='무엇을 말할지 먼저 정하고 그립니다. 템플릿이 모든 페이지의 모양을 맞춥니다.'),
    'ja': dict(
        title='Contrlで1つのセクションが粗い段階から完成へ進む流れ：まずキーセンテンス候補3つから1つを選び、次にセクションの展開案3つから1つを選ぶ。その後でContrlが自社のデザインシステムでスライドを描き、各ページが対応するRFP要件を示す',
        steps=[('一文', 'キーセンテンス候補3つから選ぶ'),
               ('展開', '展開案3つから選ぶ'),
               ('ページ', 'Contrlがスライドを作成')],
        key='新システムが安定するまで、\n乗客は今までどおり\n運賃を払えます',
        key2='新システムが安定するまで、\n乗客は今までどおり',
        plans='展開案', pages=['1ページ', '2–3ページ', '4ページ'],
        old='旧運賃システム', new='新運賃システム', mark='エラーなしの30日',
        chip='RFP要件4.2に対応',
        ds='自社のデザイン\nシステム', foot='何を伝えるかを決めてから描きます。テンプレートが全ページの見た目をそろえます。'),
    'zh': dict(
        title='一个章节在 Contrl 中从草稿到成品的过程：先从三个核心句候选中选一个，再从三个章节展开方案中选一个，之后 Contrl 才用贵公司的设计体系绘制幻灯片，并在每页注明所回应的招标需求',
        steps=[('一句话', '从3个核心句候选中选择'),
               ('展开方案', '从3个展开方案中选择'),
               ('页面', 'Contrl 绘制幻灯片')],
        key='新系统稳定运行之前，\n乘客照旧方式付费',
        key2='新系统稳定运行之前，\n乘客照旧方式付费',
        plans='方案', pages=['第1页', '第2–3页', '第4页'],
        old='旧票务系统', new='新票务系统', mark='零差错30天',
        chip='回应招标需求 4.2',
        ds='贵公司的设计体系', foot='先定下要说什么，再动手画；模板让每一页保持一致。'),
}

FX = [40, 435, 830]
FW, FY, FH = 330, 112, 318


def badge(s, x, y, n):
    s.out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{ACCENT}"/>')
    s.text(x, y + 6, str(n), fs=16, weight=700, fill='#fff', anchor='middle')


def arrow(s, x1, x2, y):
    s.out.append(f'<line x1="{x1}" y1="{y}" x2="{x2 - 10}" y2="{y}" stroke="{ACCENT}" stroke-width="2.5"/>')
    s.out.append(f'<path d="M{x2 - 12} {y - 8} L{x2} {y} L{x2 - 12} {y + 8} Z" fill="{ACCENT}"/>')


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)

    # step headers
    for i, (lab, sub) in enumerate(t['steps']):
        x = FX[i]
        badge(s, x + 15, 42, i + 1)
        s.text(x + 42, 49, lab, fs=21, weight=800, fill=ACCENT_INK if i == 2 else INK)
        s.text(x, 86, sub, fs=15, fill=MUTED)

    for i in range(2):
        arrow(s, FX[i] + FW + 14, FX[i + 1] - 14, FY + FH / 2)

    # ---- frame 1: three candidates, one picked (text only, lowest fidelity)
    x = FX[0]
    s.rect(x, FY, FW, FH, '#fff', LINE, r=14)
    hk = s.block_h(t['key'], 16, FW - 84, lh=1.35) + 30
    cy = FY + (FH - (62 * 2 + hk + 28)) / 2
    for k in range(3):
        if k == 1:
            hh = s.block_h(t['key'], 16, FW - 84, lh=1.35) + 30
            s.rect(x + 18, cy, FW - 36, hh, PEACH, ACCENT, r=10, sw=2)
            s.out.append(f'<circle cx="{x + 38}" cy="{cy + 24}" r="10" fill="{ACCENT}"/>')
            s.out.append(f'<path d="M{x + 33} {cy + 24} l4 4 l7 -8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
            s.text(x + 58, cy + 29, t['key'], fs=16, weight=700, maxw=FW - 84, lh=1.35)
            cy += hh + 14
        else:
            s.rect(x + 18, cy, FW - 36, 62, CREAM, LINE, r=10, sw=1, dash='5 5')
            s.rect(x + 36, cy + 20, (FW - 72) * 0.85, 8, GRAY_BOX, r=4)
            s.rect(x + 36, cy + 36, (FW - 72) * 0.55, 8, GRAY_BOX, r=4)
            cy += 62 + 14

    # ---- frame 2: plan tabs + dashed wireframe of page blocks
    x = FX[1]
    s.rect(x, FY, FW, FH, '#fff', LINE, r=14)
    tabw = (FW - 36 - 16) / 3
    for k, L in enumerate('ABC'):
        tx = x + 18 + k * (tabw + 8)
        on = k == 1
        s.rect(tx, FY + 20, tabw, 34, PEACH if on else CREAM, ACCENT if on else LINE, r=8, sw=2 if on else 1)
        s.text(tx + tabw / 2, FY + 43, f"{t['plans']} {L}", fs=14, weight=700 if on else 400,
               fill=ACCENT_INK if on else GRAY_TXT, anchor='middle')
    s.rect(x + 18, FY + 72, FW - 36, 10, INK, r=5)  # the key sentence, now a line on top
    by = FY + 98
    hs = [50, 74, 50]
    for k, (pg, hh) in enumerate(zip(t['pages'], hs)):
        s.rect(x + 18, by, FW - 36, hh, '#fff', GRAY_TXT, r=8, sw=1.5, dash='6 5')
        s.text(x + 34, by + 24, pg, fs=13, weight=700, fill=MUTED)
        s.rect(x + 34, by + 36, (FW - 120) * (0.7 if k != 1 else 0.85), 7, GRAY_BOX, r=3)
        by += hh + 10

    # ---- frame 3: the finished slide, in colour
    x = FX[2]
    s.rect(x, FY, FW, FH, '#fff', ACCENT, r=14, sw=2)
    s.rect(x, FY, FW, 10, ACCENT, r=0)
    s.rect(x + 20, FY + 30, 5, 56, ACCENT, r=2)
    s.text(x + 36, FY + 52, t['key2'], fs=17, weight=800, lh=1.3)
    # timeline: old and new running side by side until the clean-run marker
    ty = FY + 132
    bx, bw = x + 24, FW - 48
    s.text(bx, ty - 8, t['old'], fs=12, weight=700, fill=MUTED)
    s.rect(bx, ty, bw * 0.78, 18, GRAY_BOX, GRAY_TXT, r=9, sw=1)
    s.text(bx + bw * 0.22, ty + 48, t['new'], fs=12, weight=700, fill=ACCENT_INK)
    s.rect(bx + bw * 0.22, ty + 56, bw * 0.78, 18, ACCENT, r=9)
    mx = bx + bw * 0.78
    s.out.append(f'<line x1="{mx}" y1="{ty - 22}" x2="{mx}" y2="{ty + 94}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 4"/>')
    s.text(mx - 6, ty + 112, t['mark'], fs=13, weight=700, anchor='end')
    # requirement chip
    cw_ = tw(t['chip'], 13) + 26
    s.rect(x + 24, FY + FH - 50, cw_, 30, PEACH, ACCENT, r=15, sw=1.5)
    s.text(x + 24 + cw_ / 2, FY + FH - 30, t['chip'], fs=13, weight=700, fill=ACCENT_INK, anchor='middle')

    # ---- design-system strip feeding frame 3
    sy = FY + FH + 40
    s.rect(x, sy, FW, 60, CREAM, LINE, r=12)
    for k, c in enumerate([ACCENT, INK, '#fff', GRAY_BOX]):
        s.out.append(f'<rect x="{x + 18 + k * 30}" y="{sy + 18}" width="24" height="24" rx="6" fill="{c}" stroke="{LINE}" stroke-width="1"/>')
    s.text(x + 146, sy + 39, 'Aa', fs=22, weight=800)
    s.text(x + 190, sy + 36, t['ds'], fs=14, weight=700, fill=MUTED, maxw=FW - 200, lh=1.25)
    ax = x + FW / 2 + 60
    s.out.append(f'<line x1="{ax}" y1="{sy - 4}" x2="{ax}" y2="{FY + FH + 12}" stroke="{ACCENT}" stroke-width="2.5"/>')
    s.out.append(f'<path d="M{ax - 8} {FY + FH + 14} L{ax} {FY + FH + 2} L{ax + 8} {FY + FH + 14} Z" fill="{ACCENT}"/>')

    s.text(40, 492, t['foot'], fs=17, fill=MUTED, maxw=740, lh=1.45)
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
