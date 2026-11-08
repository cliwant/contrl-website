#!/usr/bin/env python3
"""EP11 (Competitive Price to Win) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep11.py
Writes images/blog/competitive-price-to-win/contrl-ptw-edge.svg (en) and .<lang>.svg (ko/ja/zh).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'competitive-price-to-win', 'contrl-ptw-edge'

T = {
    'en': dict(
        title='Your team’s Price to Win findings about each rival and the target position go into Contrl’s strategy interview; of the proposed win themes, one whose edge needs more than the target price allows is set aside, and the one that fits the target position is chosen',
        z1='Your Price to Win analysis', z1_sub='done by your analysts, outside Contrl',
        rivals=[('Rival A', 'Lowest price, thin transition team'),
                ('Rival B · incumbent', 'Safe, but priced highest')],
        target='Target position', target_v='B’s low risk at near A’s price',
        z2='In Contrl',
        interview='Strategy interview', interview_sub='asks about the competition',
        themes='Proposed win themes',
        t_bad='Edge: the largest senior team', bad_note='Too costly for the target price',
        t_good='Edge: low-risk transition on a lean team', good_note='Fits the target position',
        pick='Your pick',
        foot='Contrl doesn’t set the price. Your Price to Win result decides which edge the win theme can promise.'),
    'ko': dict(
        title='경쟁사별 Price to Win 분석 결과와 목표 포지션을 Contrl 전략 인터뷰에 가져가면, 제안된 윈 테마 가운데 목표 가격으로 감당할 수 없는 강점은 제외하고 목표 포지션에 맞는 강점을 고른다',
        z1='우리 팀의 Price to Win 분석', z1_sub='분석 담당이 Contrl 밖에서 수행',
        rivals=[('경쟁사 A', '최저가, 전환 인력은 최소'),
                ('경쟁사 B · 현 수행사', '안정적이지만 가격은 최고')],
        target='목표 포지션', target_v='B 수준의 낮은 위험을\nA에 가까운 가격으로',
        z2='Contrl에서',
        interview='전략 인터뷰', interview_sub='경쟁사 질문에 답하며',
        themes='제안된 윈 테마',
        t_bad='강점: 최대 규모의 고급 인력', bad_note='목표 가격으로는 감당할 수 없음',
        t_good='강점: 소수 정예의 안정적 전환', good_note='목표 포지션에 맞음',
        pick='선택',
        foot='가격은 Contrl이 정하지 않습니다. Price to Win 결과가 윈 테마가 약속할 강점을 정합니다.'),
    'ja': dict(
        title='競合ごとのPrice to Win分析の結果と目標ポジションをContrlの戦略インタビューに持ち込むと、提案されたウィンテーマのうち目標価格では支えられない強みは外し、目標ポジションに合う強みを選べる',
        z1='自社のPrice to Win分析', z1_sub='分析担当がContrlの外で実施',
        rivals=[('競合A', '最安値、移行要員は最小限'),
                ('競合B · 現行業者', '安心感はあるが価格は最高')],
        target='目標ポジション', target_v='B並みの低リスクを\nAに近い価格で',
        z2='Contrlで',
        interview='戦略インタビュー', interview_sub='競合についての質問に答える',
        themes='提案されたウィンテーマ',
        t_bad='強み：最大規模の上級チーム', bad_note='目標価格では支えられない',
        t_good='強み：少数精鋭で\n低リスクな移行', good_note='目標ポジションに合う',
        pick='選択',
        foot='価格はContrlが決めるのではありません。Price to Winの結果が、ウィンテーマで約束できる強みを決めます。'),
    'zh': dict(
        title='把针对各竞争对手的制胜价格分析结论和目标定位带进 Contrl 的策略访谈；在提出的制胜主题中，放下目标价格撑不起的优势，选择符合目标定位的那一个',
        z1='我方的制胜价格分析', z1_sub='由分析人员在 Contrl 之外完成',
        rivals=[('对手 A', '价格最低，交接团队单薄'),
                ('对手 B · 现任承包商', '稳妥，但报价最高')],
        target='目标定位', target_v='B 一样的低风险，\n接近 A 的价格',
        z2='在 Contrl 中',
        interview='策略访谈', interview_sub='回答关于竞争对手的问题',
        themes='提出的制胜主题',
        t_bad='优势：规模最大的资深团队', bad_note='目标价格撑不起',
        t_good='优势：精干团队，低风险交接', good_note='符合目标定位',
        pick='选择',
        foot='价格不由 Contrl 决定。制胜价格分析的结论决定制胜主题能承诺哪种优势。'),
}


def ptw(lang):
    t = T[lang]
    s = Svg(lang, 560)
    # zone 1: your cPTW analysis (outside Contrl)
    s.rect(30, 30, 420, 470, CREAM, LINE, r=20)
    s.text(56, 72, t['z1'], fs=21, weight=700, maxw=370)
    s.text(56, 102, t['z1_sub'], fs=16, fill=MUTED, maxw=370)
    y = 126
    for who, what in t['rivals']:
        s.rect(56, y, 368, 92, '#fff', LINE, r=12)
        s.text(78, y + 34, who, fs=16, weight=700, fill=MUTED)
        s.text(78, y + 66, what, fs=18, maxw=330)
        y += 106
    # target position
    s.rect(56, 346, 368, 128, PEACH, ACCENT, r=12, sw=2)
    s.text(78, 382, t['target'], fs=17, weight=700, fill=ACCENT_INK)
    s.text(78, 418, t['target_v'], fs=20, weight=700, maxw=330)
    # arrow into Contrl
    s.arrow(452, 280, 506, 280)
    # zone 2: in Contrl
    s.rect(510, 30, 660, 470, PEACH, ACCENT, r=20, sw=2)
    s.text(536, 72, t['z2'], fs=20, weight=700, fill=ACCENT_INK)
    s.rect(536, 100, 250, 360, '#fff', LINE, r=14)
    hi = s.block_h(t['interview'], 21, 210)
    hs = s.block_h(t['interview_sub'], 16, 210)
    top = 280 - (hi + 10 + hs) / 2 + 21
    yy = s.text(661, top, t['interview'], fs=21, weight=700, anchor='middle', maxw=210)
    s.text(661, yy + 6, t['interview_sub'], fs=16, fill=MUTED, anchor='middle', maxw=210)
    # themes
    s.text(822, 120, t['themes'], fs=17, weight=700, fill=MUTED)
    # bad theme (set aside)
    s.path('M788 220 C800 220 806 196 818 196', color=GRAY_TXT, sw=2.5)
    s.rect(822, 140, 324, 130, GRAY_BOX, GRAY_TXT, r=12, dash='6 6')
    ye = s.text(844, 176, t['t_bad'], fs=18, weight=600, fill='#71717a', maxw=284, lh=1.3)
    s.text(844, ye + 8, '✕ ' + t['bad_note'], fs=15, fill='#71717a', maxw=284, lh=1.3)
    # good theme (picked)
    s.path('M788 340 C800 340 806 364 818 364')
    s.rect(822, 296, 324, 150, INK, r=12)
    yg = s.text(844, 334, t['t_good'], fs=19, weight=700, fill='#fff', maxw=284, lh=1.3)
    s.text(844, yg + 8, '✓ ' + t['good_note'], fs=16, fill='#fde3d2', weight=600, maxw=284, lh=1.3)
    pw = tw(t['pick'], 14) + 28
    s.pill(1146 - pw - 12, 296 - 14, t['pick'], fs=14)
    s.text(W / 2, 538, t['foot'], fs=18, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(ptw(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
