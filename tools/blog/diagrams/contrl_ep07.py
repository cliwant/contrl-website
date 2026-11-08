#!/usr/bin/env python3
"""EP07 concept diagram: scattered section messages vs one win theme on every section.

Run:  python3 tools/blog/diagrams/contrl_ep07.py
Writes images/blog/strategy-and-win-themes/contrl-one-thread(.<lang>).svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402

SLUG = 'strategy-and-win-themes'
NAME = 'contrl-one-thread'
LANGS = ['en', 'ko', 'ja', 'zh']

T = {
    'en': dict(
        title='When each section tells its own story the evaluator falls back to price; when one chosen win theme runs through every section, the evaluator remembers a reason beyond price',
        a_tag='Each section tells its own story', b_tag='One win theme on every section · Contrl',
        sec='Section', a_msgs=['“Innovative platform”', '“Lowest cost”', '“Stable operations”'],
        a_out='“They all look alike.”\nCompare the prices.',
        theme='Chosen win theme', theme_rows=['Client need', 'Your edge', 'Benefit'],
        key='Key sentence', b_out='“Zero billing disruption.”\nA reason beyond price.'),
    'ko': dict(
        title='섹션마다 다른 이야기를 하면 평가위원은 가격으로 돌아가고, 고른 윈 테마 하나가 모든 섹션을 관통하면 가격 말고 선택할 이유가 남는다',
        a_tag='섹션마다 다른 이야기', b_tag='모든 섹션에 하나의 윈 테마 · Contrl',
        sec='섹션', a_msgs=['“혁신적인 플랫폼”', '“최저 비용”', '“안정적 운영”'],
        a_out='“다 고만고만하네.”\n가격을 비교한다.',
        theme='선택한 윈 테마', theme_rows=['고객 니즈', '우리의 강점', '효과'],
        key='핵심 문장', b_out='“정산 중단 제로.”\n가격 말고 선택할 이유.'),
    'ja': dict(
        title='セクションごとに違う話をすると評価者は価格に戻り、選んだ一つのウィンテーマがすべてのセクションを貫くと価格以外の選ぶ理由が残る',
        a_tag='セクションごとに違う話', b_tag='すべてのセクションに一つのウィンテーマ · Contrl',
        sec='セクション', a_msgs=['「革新的な\nプラットフォーム」', '「最低コスト」', '「安定運用」'],
        a_out='「どこも同じに見える」\n価格を比べる。',
        theme='選んだウィンテーマ', theme_rows=['顧客ニーズ', '自社の強み', '効果'],
        key='キーセンテンス', b_out='「請求の中断ゼロ」\n価格以外の選ぶ理由。'),
    'zh': dict(
        title='每个章节各说各话，评审只能回到比价格；选定的一个制胜主题贯穿每个章节，评审就记住了价格之外的理由',
        a_tag='每个章节各说各话', b_tag='每个章节同一个制胜主题 · Contrl',
        sec='章节', a_msgs=['“创新平台”', '“最低成本”', '“稳定运营”'],
        a_out='“看起来都差不多。”\n那就比价格。',
        theme='选定的制胜主题', theme_rows=['客户需求', '我方优势', '收益'],
        key='核心句', b_out='“计费零中断。”\n价格之外的理由。'),
}


def one_thread(lang):
    t = T[lang]
    s = Svg(lang, 620)
    # ---- row A: scattered
    s.text(40, 52, t['a_tag'], fs=18, weight=700, fill=MUTED)
    xs = [40, 250, 460]
    for i, x in enumerate(xs):
        s.rect(x, 72, 190, 112, GRAY_BOX, r=14)
        s.text(x + 18, 104, f"{t['sec']} {i + 1}", fs=15, weight=700, fill=GRAY_TXT)
        s.text(x + 18, 138, t['a_msgs'][i], fs=16, fill='#52525b', weight=600, maxw=160, lh=1.3)
    s.arrow(654, 128, 742, 128, color=GRAY_TXT)
    s.rect(746, 72, 414, 112, GRAY_BOX, r=14, dash='6 6', stroke=GRAY_TXT, sw=1.5)
    s.text(953, 118, t['a_out'], fs=19, fill='#52525b', weight=600, anchor='middle')
    # divider
    s.out.append(f'<line x1="40" y1="224" x2="1160" y2="224" stroke="{LINE}" stroke-width="2"/>')
    # ---- row B: one thread
    s.text(40, 270, t['b_tag'], fs=18, weight=700, fill=ACCENT_INK)
    s.rect(40, 292, 250, 290, INK, r=16)
    s.text(64, 334, t['theme'], fs=19, weight=700, fill='#fff', maxw=210)
    y = 392
    for r in t['theme_rows']:
        s.rect(64, y - 26, 202, 44, '#2a2a2e', r=10)
        s.out.append(f'<circle cx="84" cy="{y - 4}" r="5" fill="{ACCENT}"/>')
        s.text(100, y + 2, r, fs=16, fill='#fff', weight=600)
        y += 60
    # thread line through sections
    cards = [(340, 300), (530, 300), (720, 300)]
    s.out.append(f'<line x1="290" y1="437" x2="904" y2="437" stroke="{ACCENT}" stroke-width="4"/>')
    for i, (cx, cy) in enumerate(cards):
        s.rect(cx, cy, 170, 270, '#fff', LINE, r=14)
        s.text(cx + 18, cy + 34, f"{t['sec']} {i + 1}", fs=15, weight=700, fill=MUTED)
        s.rect(cx + 14, cy + 112, 142, 50, PEACH, ACCENT, r=10, sw=2)
        s.text(cx + 85, cy + 143, t['key'], fs=16 if tw(t['key'], 16) < 130 else 14, weight=700, fill=ACCENT_INK, anchor='middle')
        for k in range(3):
            s.rect(cx + 18, cy + 186 + k * 22, 134 - k * 24, 10, GRAY_BOX, r=5)
    s.arrow(906, 437, 942, 437)
    s.rect(946, 362, 214, 150, PEACH, ACCENT, r=16, sw=2)
    l0, l1 = t['b_out'].split('\n')
    h0, h1 = s.block_h(l0, 18, 186, 1.3), 16 * 1.3
    y = 437 - (h0 + 10 + h1) / 2 + 17
    y = s.text(1053, y, l0, fs=18, weight=700, fill=ACCENT_INK, anchor='middle', maxw=186, lh=1.3) + 10
    s.text(1053, y, l1, fs=16, weight=600, fill=INK, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in LANGS:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(one_thread(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
