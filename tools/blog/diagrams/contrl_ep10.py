#!/usr/bin/env python3
"""EP10 (Proof Points) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep10.py
Writes images/blog/proof-points/contrl-proof-feedback.svg (en) and .<lang>.svg (ko/ja/zh).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'proof-points', 'contrl-proof-feedback'

T = {
    'en': dict(
        title='A slide with a generic claim, one line of chat feedback giving the real figure, and the rewritten slide that states the claim with its proof and the RFP requirement it answers',
        s1='Draft page', s2='Your feedback', s3='Rewritten page',
        h1='Extensive migration experience', tag1='Claim only',
        chat_from='From your records',
        chat='“Use our record: 14 site cutovers since 2021, none outside the downtime window.”',
        h3='Staged cutover keeps services running', proof='14 cutovers since 2021,\nnone outside the agreed window',
        req='Answers RFP req. 3.2',
        foot='AI can’t invent your proof. Give it the real figure, and the claim and its evidence share a page.'),
    'ko': dict(
        title='막연한 주장만 담긴 슬라이드에 실제 수치를 한 줄 피드백으로 주면, 주장과 증거, 대응하는 제안요청서 요구사항이 함께 담긴 페이지로 다시 쓰인다',
        s1='초안 페이지', s2='한 줄 피드백', s3='다시 쓴 페이지',
        h1='풍부한 시스템 전환 경험', tag1='주장뿐',
        chat_from='우리 회사 기록에서',
        chat='“실적으로 바꿔줘: 2021년 이후 14개 기관 전환, 약속한 중단 시간 초과 0건.”',
        h3='단계적 전환으로\n서비스 중단 없이', proof='2021년 이후 14개 기관 전환,\n약속한 중단 시간 초과 0건',
        req='제안요청서 요구사항 3.2 대응',
        foot='AI는 증거를 지어낼 수 없습니다. 실제 수치를 주면 주장과 증거가 한 페이지에 담깁니다.'),
    'ja': dict(
        title='漠然とした主張だけのスライドに実際の数値を一行のフィードバックで伝えると、主張と証拠、対応するRFP要件をそろえたページに書き直される',
        s1='下書きのページ', s2='一行のフィードバック', s3='書き直されたページ',
        h1='豊富な移行経験', tag1='主張だけ',
        chat_from='自社の記録から',
        chat='「実績に置き換えて：\n2021年以降14拠点を移行、\n合意した停止時間の超過0件」',
        h3='段階的移行で\nサービスを止めない', proof='2021年以降14拠点を移行、\n合意した停止時間の超過0件',
        req='RFP要件3.2に対応',
        foot='AIは証拠を作り出せません。実際の数値を渡せば、主張と証拠が同じページに並びます。'),
    'zh': dict(
        title='一页只有空泛主张的幻灯片，通过一句对话反馈给出真实数字后，被改写成主张、证据和所回应的招标需求同在一页',
        s1='初稿页面', s2='一句反馈', s3='改写后的页面',
        h1='丰富的系统迁移经验', tag1='只有主张',
        chat_from='来自公司记录',
        chat='“换成实绩：\n2021年以来切换了14个站点，\n无一超出约定停机时间。”',
        h3='分阶段切换，服务不中断', proof='2021年以来14个站点切换，\n无一超出约定停机时间',
        req='回应招标需求 3.2',
        foot='AI 无法凭空编造证据。给它真实数字，主张和证据就会出现在同一页。'),
}


def lines(s, x, y, n, w, color=LINE):
    for i in range(n):
        ww = w if i < n - 1 else w * 0.6
        s.rect(x, y + i * 22, ww, 8, color, r=4)


def diagram(lang):
    t = T[lang]
    s = Svg(lang, 470)
    # step labels
    for x, lab, col in ((40, t['s1'], MUTED), (440, t['s2'], ACCENT_INK), (820, t['s3'], ACCENT_INK)):
        s.text(x, 50, lab, fs=18, weight=700, fill=col)

    # 1 · draft page (generic)
    s.rect(40, 70, 340, 300, GRAY_BOX, GRAY_TXT, r=14, dash='6 6')
    y = s.text(64, 116, t['h1'], fs=22, weight=700, fill='#52525b', maxw=292)
    lines(s, 64, y + 6, 4, 260, '#d4d4d8')
    s.pill(64, 300, t['tag1'], fs=15, fill='#d4d4d8', color='#52525b')

    s.arrow(384, 220, 436, 220)

    # 2 · chat feedback (bubble centred in the box)
    bh = s.block_h(t['chat'], 19, 262, 1.4) + 40
    top = 70 + (300 - (bh + 34)) / 2
    s.rect(440, 70, 340, 300, PEACH, ACCENT, r=14, sw=2)
    s.text(464, top + 16, t['chat_from'], fs=16, weight=600, fill=MUTED, maxw=292)
    s.rect(464, top + 34, 292, bh, '#fff', LINE, r=12)
    s.text(482, top + 68, t['chat'], fs=19, weight=600, maxw=262, lh=1.4)

    s.arrow(784, 220, 816, 220)

    # 3 · rewritten page
    s.rect(820, 70, 340, 300, '#fff', ACCENT, r=14, sw=2)
    y = s.text(844, 116, t['h3'], fs=21, weight=700, maxw=292)
    ph = s.block_h(t['proof'], 16, 268, 1.35) + 26
    s.rect(844, y + 2, 292, ph, CREAM, r=10)
    s.rect(844, y + 2, 6, ph, ACCENT, r=3)
    s.text(864, y + 28, t['proof'], fs=16, weight=600, fill=ACCENT_INK, maxw=268, lh=1.35)
    lines(s, 844, y + ph + 18, 1, 260)
    s.pill(844, 316, t['req'], fs=15, fill=INK)

    s.text(W / 2, 428, t['foot'], fs=19, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in T:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
