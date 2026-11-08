#!/usr/bin/env python3
"""EP09 · Features, Benefits and Discriminators — "Where Contrl fits" diagram, one SVG per language.

Run:  python3 tools/blog/diagrams/contrl_ep09.py
Writes images/blog/features-benefits-discriminators/contrl-fbd.<lang>.svg (en has no lang suffix).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402

SLUG, NAME = 'features-benefits-discriminators', 'contrl-fbd'

T = {
    'en': dict(
        title='A feature you mention in the Contrl strategy interview, with what you know about the client and competitors, becomes a win theme stating the client need, your edge (why us) and the benefit (so what)',
        left='What you tell the interview',
        cards=[('Feature · what we have', '24/7 monitoring center'),
               ('Client', 'Outages found late last year'),
               ('Competitors', 'Rival B: office hours only')],
        mid='Contrl strategy interview',
        theme='Win theme',
        rows=[('Client need', 'Catch problems before users do', None),
              ('Our edge', 'The only round-the-clock coverage', 'Why us?'),
              ('Benefit', 'Shorter service interruptions', 'So what?')],
        foot='The feature goes in; the win theme states the need, the edge and the benefit.'),
    'ko': dict(
        title='Contrl 전략 인터뷰에서 말한 기능이 고객·경쟁사 정보와 함께 고객 니즈, 우리의 강점(왜 우리인가), 효과(그래서 뭐가 좋은가)를 담은 윈 테마가 된다',
        left='인터뷰에서 우리가 말하는 것',
        cards=[('기능 · 우리가 가진 것', '24시간 관제 센터'),
               ('고객', '작년에 장애를 늦게 발견했다'),
               ('경쟁사', 'B사는 업무 시간에만 관제한다')],
        mid='Contrl 전략 인터뷰',
        theme='윈 테마',
        rows=[('고객 니즈', '사용자보다 먼저 문제를 발견', None),
              ('우리의 강점', '유일한 24시간 관제', '왜 우리인가?'),
              ('효과', '서비스 중단 시간 단축', '그래서?')],
        foot='기능을 넣으면, 윈 테마는 니즈와 강점과 효과로 말합니다.'),
    'ja': dict(
        title='Contrlの戦略インタビューで伝えた機能が、顧客と競合の情報とともに、顧客ニーズ、自社の強み（なぜ自社か）、効果（だから何か）を述べるウィンテーマになる',
        left='インタビューで伝えること',
        cards=[('機能 · 自社が持つもの', '24時間監視センター'),
               ('顧客', '昨年、障害の発見が遅れた'),
               ('競合', 'B社の監視は業務時間のみ')],
        mid='Contrl\n戦略インタビュー',
        theme='ウィンテーマ',
        rows=[('顧客ニーズ', '利用者より先に問題を見つける', None),
              ('自社の強み', '唯一の24時間監視', 'なぜ自社か？'),
              ('効果', 'サービス停止時間の短縮', 'だから何？')],
        foot='機能を入れると、ウィンテーマはニーズ・強み・効果で語ります。'),
    'zh': dict(
        title='在 Contrl 策略访谈中提到的功能，加上对客户和竞争对手的了解，会变成写明客户需求、我方优势（为什么是我们）和收益（那又怎样）的制胜主题',
        left='你在访谈中提供的信息',
        cards=[('功能 · 我们拥有的', '7×24 小时监控中心'),
               ('客户', '去年故障发现得太晚'),
               ('竞争对手', 'B 公司只在工作时间监控')],
        mid='Contrl\n策略访谈',
        theme='制胜主题',
        rows=[('客户需求', '在用户察觉之前发现问题', None),
              ('我方优势', '唯一的全天候监控', '为什么是我们？'),
              ('收益', '缩短服务中断时间', '那又怎样？')],
        foot='输入的是功能，制胜主题说出的是需求、优势和收益。'),
}


def fbd(lang):
    t = T[lang]
    s = Svg(lang, 560)
    # left zone: inputs
    s.rect(30, 30, 410, 450, CREAM, LINE)
    s.text(56, 70, t['left'], fs=19, weight=700, fill=MUTED, maxw=360)
    y = 96
    for i, (tag, body) in enumerate(t['cards']):
        feat = i == 0
        s.rect(56, y, 358, 112, '#fff', ACCENT if feat else LINE, r=12, sw=2 if feat else 1.5)
        s.text(78, y + 34, tag, fs=15, weight=700, fill=ACCENT_INK if feat else MUTED)
        s.text(78, y + 70, body, fs=19, weight=600 if feat else 400, maxw=320, lh=1.3)
        y += 126
    # middle: interview
    s.path('M442 255 L486 255')
    s.rect(490, 195, 170, 120, '#fff', LINE, r=14)
    hm = s.block_h(t['mid'], 18, 150)
    s.text(575, 255 - hm / 2 + 18, t['mid'], fs=18, weight=700, anchor='middle', maxw=150)
    s.arrow(662, 255, 700, 255)
    # right: win theme
    s.rect(704, 30, 466, 450, PEACH, ACCENT, r=16, sw=2)
    s.text(732, 74, t['theme'], fs=22, weight=700, fill=ACCENT_INK)
    yy = 100
    for k, v, tag in t['rows']:
        s.rect(728, yy, 418, 112, '#fff', LINE, r=12)
        s.text(750, yy + 34, k, fs=16, weight=700, fill=MUTED)
        if tag:
            pw = tw(tag, 14) + 28
            s.pill(1146 - 16 - pw, yy + 14, tag, fs=14)
        s.text(750, yy + 74, v, fs=20, weight=700, maxw=380)
        yy += 126
    s.text(W / 2, 524, t['foot'], fs=18, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ('en', 'ko', 'ja', 'zh'):
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(fbd(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
