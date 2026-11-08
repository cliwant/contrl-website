#!/usr/bin/env python3
"""EP13 (Cost and Pricing Data) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep13.py
Writes images/blog/cost-and-pricing-data/contrl-price-narrative.svg (en) and .<lang>.svg (ko/ja/zh).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'cost-and-pricing-data', 'contrl-price-narrative'

T = {
    'en': dict(
        title='One win theme feeds both the technical section and the price narrative; each page cites the RFP requirements it answers, while the figures come from your pricing team',
        wt='Selected win theme', wt_body='No service downtime during transition, through a staged cutover',
        l_lab='Technical section', l_key='Staged cutover keeps every service running',
        l_req='Answers RFP req. 2.1',
        r_lab='Price narrative', r_key='The staged plan avoids the cost of downtime',
        r_fig='Figures', r_req='Answers RFP req. 5.3',
        team='Your pricing team', team_sub='Supplies the numbers.\nContrl doesn’t set\nthe price.',
        foot='Same theme in both volumes. The story comes from Contrl; the numbers come from you.'),
    'ko': dict(
        title='하나의 윈 테마가 기술 섹션과 가격 설명 페이지를 함께 이끌고, 각 페이지는 대응하는 제안요청서 요구사항을 표시하며, 숫자는 가격 담당 팀이 채운다',
        wt='선택한 윈 테마', wt_body='단계적 전환으로 전환 기간에도 서비스 중단 없음',
        l_lab='기술 섹션', l_key='단계적 전환으로 모든 서비스가 멈추지 않습니다',
        l_req='제안요청서 요구사항 2.1 대응',
        r_lab='가격 설명 페이지', r_key='단계적 계획이 서비스 중단 비용을 막습니다',
        r_fig='숫자', r_req='제안요청서 요구사항 5.3 대응',
        team='가격 담당 팀', team_sub='숫자를 채웁니다.\nContrl은 가격을\n정하지 않습니다.',
        foot='두 권에 같은 테마. 이야기는 Contrl이, 숫자는 우리 팀이 만듭니다.'),
    'ja': dict(
        title='一つのウィンテーマが技術セクションと価格説明ページの両方を貫き、各ページは対応するRFP要件を示し、数字は価格担当チームが入れる',
        wt='選んだウィンテーマ', wt_body='段階的移行で、移行期間中もサービスを止めない',
        l_lab='技術セクション', l_key='段階的移行で、すべての\nサービスを止めません',
        l_req='RFP要件2.1に対応',
        r_lab='価格説明ページ', r_key='段階的な計画が、停止に\nよるコストを防ぎます',
        r_fig='数字', r_req='RFP要件5.3に対応',
        team='価格担当チーム', team_sub='数字を入れる。\nContrlは価格を\n決めません。',
        foot='両方の巻に同じテーマ。ストーリーはContrlが、数字は自社が用意します。'),
    'zh': dict(
        title='同一个制胜主题贯穿技术章节和价格说明页，每页标注所回应的招标需求，数字由你的定价团队提供',
        wt='选定的制胜主题', wt_body='分阶段切换，过渡期间服务不中断',
        l_lab='技术章节', l_key='分阶段切换，所有服务\n持续运行',
        l_req='回应招标需求 2.1',
        r_lab='价格说明页', r_key='分阶段方案避免了\n停机带来的成本',
        r_fig='数字', r_req='回应招标需求 5.3',
        team='你的定价团队', team_sub='提供数字。\nContrl 不负责定价。',
        foot='两部分讲同一个主题。故事由 Contrl 组织，数字由你提供。'),
}


def lines(s, x, y, n, w, color=LINE):
    for i in range(n):
        ww = w if i < n - 1 else w * 0.6
        s.rect(x, y + i * 20, ww, 8, color, r=4)


def page(s, x, y, w, h, lab, key, req):
    s.text(x, y - 12, lab, fs=18, weight=700, fill=ACCENT_INK)
    s.rect(x, y, w, h, '#fff', ACCENT, r=14, sw=2)
    yy = s.text(x + 24, y + 44, key, fs=21, weight=700, maxw=w - 48)
    s.pill(x + 24, y + h - 54, req, fs=15, fill=INK)
    return yy


def diagram(lang):
    t = T[lang]
    s = Svg(lang, 550)
    # win theme banner
    s.rect(300, 26, 600, 122, PEACH, ACCENT, r=14, sw=2)
    s.pill(324, 42, t['wt'], fs=15)
    s.text(324, 100, t['wt_body'], fs=19, weight=600, maxw=552, lh=1.35)

    # branches
    s.path('M 520 148 C 520 176, 280 168, 280 200')
    s.path('M 680 148 C 680 176, 720 168, 720 200')

    # left: technical section page
    yy = page(s, 60, 222, 440, 250, t['l_lab'], t['l_key'], t['l_req'])
    lines(s, 84, yy + 4, 3, 340)

    # right: price narrative page
    yy = page(s, 540, 222, 360, 250, t['r_lab'], t['r_key'], t['r_req'])
    fy = yy + 4
    s.rect(564, fy, 312, 66, CREAM, ACCENT, r=10, dash='6 5')
    s.text(584, fy + 26, t['r_fig'], fs=15, weight=700, fill=ACCENT_INK)
    for i, hgt in enumerate((18, 30, 24, 40)):
        s.rect(700 + i * 36, fy + 56 - hgt, 22, hgt, ACCENT if i == 3 else '#d4d4d8', r=3)

    # pricing team
    s.rect(940, 248, 220, 160, GRAY_BOX, GRAY_TXT, r=14)
    s.text(960, 286, t['team'], fs=18, weight=700, fill='#3f3f46', maxw=184)
    s.text(960, 324, t['team_sub'], fs=16, fill='#52525b', maxw=184, lh=1.45)
    s.arrow(936, fy + 33, 882, fy + 33, color=GRAY_TXT)

    s.text(W / 2, 524, t['foot'], fs=19, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in T:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
