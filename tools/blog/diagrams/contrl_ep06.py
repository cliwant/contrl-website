#!/usr/bin/env python3
"""EP06 · Executive summaries: the win theme feeds the customer-first boxes of the five-box summary.

Run:  python3 tools/blog/diagrams/contrl_ep06.py
Writes images/blog/executive-summaries/contrl-summary-boxes(.<lang>).svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'executive-summaries', 'contrl-summary-boxes'
LANGS = ['en', 'ko', 'ja', 'zh']

T = {
    'en': dict(
        title='The win theme you pick in Contrl already holds the client need, your edge and the benefit: boxes 1, 2 and 5 of a five-box executive summary. Price and next steps come from your team.',
        left='Picked in Contrl', right='Five-box executive summary',
        theme='Win theme', rows=['Client need', 'Benefit', 'Our edge'],
        boxes=['The customer’s goals and challenges', 'Your solution and its benefits', 'Investment and terms',
               'Next steps after award', 'Why choose us'],
        team='Your team adds',
        foot='One argument, stated in the customer’s order: their need first, your name last.'),
    'ko': dict(
        title='Contrl에서 고른 윈 테마에는 고객 니즈, 우리의 강점, 효과가 이미 담겨 있어 5-Box 요약문의 1·2·5번이 된다. 가격과 다음 단계는 팀이 채운다.',
        left='Contrl에서 고른 것', right='5-Box 요약문',
        theme='윈 테마', rows=['고객 니즈', '효과', '우리의 강점'],
        boxes=['고객의 목표와 과제', '솔루션과 혜택', '투자·비용·조건', '수주 후 다음 단계', '우리를 선택할 이유'],
        team='팀이 채울 것',
        foot='하나의 논리를 고객의 순서로: 고객의 니즈가 먼저, 우리 이름은 마지막.'),
    'ja': dict(
        title='Contrlで選んだウィンテーマには顧客ニーズ、自社の強み、効果がすでに入っており、5ボックス型サマリーの1・2・5番になる。価格と次のステップはチームが加える。',
        left='Contrlで選んだもの', right='5ボックス型エグゼクティブサマリー',
        theme='ウィンテーマ', rows=['顧客ニーズ', '効果', '自社の強み'],
        boxes=['顧客の目標と課題', 'ソリューションと効果', '投資・費用・条件', '受注後の次のステップ', '自社を選ぶ理由'],
        team='チームが加える',
        foot='一つの論理を顧客の順番で。顧客のニーズが先、自社の名前は最後。'),
    'zh': dict(
        title='在 Contrl 中选定的制胜主题已包含客户需求、我方优势和收益，正对应五框式执行摘要的第 1、2、5 框；价格和后续步骤由团队补充。',
        left='在 Contrl 中选定', right='五框式执行摘要',
        theme='制胜主题', rows=['客户需求', '收益', '我方优势'],
        boxes=['客户的目标与挑战', '解决方案与收益', '投资、费用与条件', '中标后的下一步', '选择我们的理由'],
        team='由团队补充',
        foot='同一个论点，按客户的顺序讲：客户需求在前，我方名字在最后。'),
}


def summary_boxes(lang):
    t = T[lang]
    s = Svg(lang, 620)
    s.text(40, 52, t['left'], fs=18, weight=700, fill=ACCENT_INK)
    s.text(560, 52, t['right'], fs=18, weight=700, fill=MUTED)

    # five boxes on the right
    bx, bw, bh, gap, y0 = 560, 600, 82, 16, 74
    ys = [y0 + i * (bh + gap) for i in range(5)]
    from_theme = {0: 0, 1: 1, 4: 2}  # box index -> theme row
    for i, y in enumerate(ys):
        hot = i in from_theme
        if hot:
            s.rect(bx, y, bw, bh, PEACH, ACCENT, r=14, sw=2)
        else:
            s.rect(bx, y, bw, bh, GRAY_BOX, GRAY_TXT, r=14, sw=1.5, dash='6 6')
        # number badge
        s.out.append(f'<circle cx="{bx + 40}" cy="{y + bh / 2}" r="20" fill="{ACCENT if hot else GRAY_TXT}"/>')
        s.text(bx + 40, y + bh / 2 + 7, str(i + 1), fs=20, weight=700, fill='#fff', anchor='middle')
        s.text(bx + 76, y + bh / 2 + 7, t['boxes'][i], fs=20, weight=700 if hot else 600,
               fill=INK if hot else '#52525b')
        if not hot:
            pw = tw(t['team'], 14) + 28
            s.pill(bx + bw - pw - 18, y + bh / 2 - 15, t['team'], fs=14, fill='#fff', color=MUTED)

    # win theme card on the left
    cx, cy, cw_, ch = 40, 150, 380, 330
    s.rect(cx, cy, cw_, ch, INK, r=18)
    s.text(cx + 30, cy + 54, t['theme'], fs=26, weight=700, fill='#fff')
    row_y = [cy + 110 + k * 72 for k in range(3)]
    for k, ry in enumerate(row_y):
        s.rect(cx + 24, ry, cw_ - 48, 54, '#2a2a2e', r=10)
        s.out.append(f'<circle cx="{cx + 48}" cy="{ry + 27}" r="6" fill="{ACCENT}"/>')
        s.text(cx + 66, ry + 34, t['rows'][k], fs=19, weight=600, fill='#fff')

    # arrows from theme rows to boxes 1, 2, 5
    for box_i, row_k in from_theme.items():
        sx, sy = cx + cw_ - 24, row_y[row_k] + 27
        ex, ey = bx - 4, ys[box_i] + bh / 2
        s.path(f'M{sx + 4} {sy} C{sx + 70} {sy} {ex - 70} {ey} {ex} {ey}')

    s.text(W / 2, 600, t['foot'], fs=18, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in LANGS:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(summary_boxes(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
