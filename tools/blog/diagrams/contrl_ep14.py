#!/usr/bin/env python3
"""EP14 (Effective Presentations) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep14.py
Writes images/blog/effective-presentations/contrl-slide-and-notes.svg (en) and .<lang>.svg (ko/ja/zh).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'effective-presentations', 'contrl-slide-and-notes'
H = 560

T = {
    'en': dict(
        title='One proposal page split in two: the slide the evaluators see carries a benefit headline and a visual, while the speaker notes carry the section key sentence the presenter says first; both come from the win theme and export to .pptx',
        l_tag='What the evaluators see', r_tag='What the presenter says',
        sec='Section 3 · Transition', head='Your services stay up\nduring the switch',
        steps=['Site 1', 'Site 2', 'Site 3'], req='Answers RFP req. 3.2',
        notes='Speaker notes', key_lab='Key sentence · say it first',
        key='“We move one site at a time, so no service you run ever stops.”',
        more='Then the three steps and the rollback plan.',
        link='one message',
        chain=['Win theme', 'Key sentence', 'Slide + notes', '.pptx'],
        foot='The slide stays light; the full argument lives in the notes, in your company’s design system.'),
    'ko': dict(
        title='한 페이지가 둘로 나뉜다. 평가위원이 보는 슬라이드에는 효과를 담은 제목과 시각 자료가, 발표자가 말하는 발표자 노트에는 섹션 핵심 문장이 담기고, 둘 다 윈 테마에서 나와 .pptx로 내보내진다',
        l_tag='평가위원이 보는 것', r_tag='발표자가 말하는 것',
        sec='3장 · 시스템 전환', head='전환하는 동안에도\n서비스는 멈추지 않습니다',
        steps=['1단계', '2단계', '3단계'], req='제안요청서 요구사항 3.2 대응',
        notes='발표자 노트', key_lab='핵심 문장 · 가장 먼저 말하기',
        key='“한 기관씩 차례로 옮기기 때문에 운영 중인 서비스는 하나도 멈추지 않습니다.”',
        more='이어서 3단계와 롤백 계획을 짚어 줍니다.',
        link='하나의 메시지',
        chain=['윈 테마', '핵심 문장', '슬라이드 + 노트', '.pptx'],
        foot='슬라이드는 가볍게, 논리 전체는 노트에. 모두 우리 회사 디자인 시스템으로.'),
    'ja': dict(
        title='一枚のページが二つに分かれる。評価者が見るスライドには便益を示す見出しと図、発表者が話すスピーカーノートにはセクションのキーセンテンスが入り、どちらもウィンテーマから生まれ.pptxで書き出される',
        l_tag='評価者が見るもの', r_tag='発表者が話すこと',
        sec='第3章 · システム移行', head='移行中も\nサービスは止まりません',
        steps=['拠点1', '拠点2', '拠点3'], req='RFP要件3.2に対応',
        notes='スピーカーノート', key_lab='キーセンテンス · 最初に話す',
        key='「一拠点ずつ順に移行するため、\n稼働中のサービスは一つも\n止まりません」',
        more='続いて3つの段階と切り戻し計画を説明する。',
        link='一つのメッセージ',
        chain=['ウィンテーマ', 'キーセンテンス', 'スライド＋ノート', '.pptx'],
        foot='スライドは軽く、論理のすべてはノートに。どちらも自社のデザインシステムで。'),
    'zh': dict(
        title='同一页分成两部分：评审专家看到的幻灯片上是体现收益的标题和图示，演讲者备注里是演讲者首先要说的章节核心句；两者都来自制胜主题，并导出为 .pptx',
        l_tag='评审专家看到的', r_tag='演讲者说出的',
        sec='第3章 · 系统切换', head='切换期间\n服务不中断',
        steps=['站点1', '站点2', '站点3'], req='回应招标需求 3.2',
        notes='演讲者备注', key_lab='核心句 · 第一句就说',
        key='“我们一次只切换一个站点，\n所以您运行中的服务\n一项都不会中断。”',
        more='接着讲三个步骤和回退方案。',
        link='同一个信息',
        chain=['制胜主题', '核心句', '幻灯片 + 备注', '.pptx'],
        foot='幻灯片保持简洁，完整论证放在备注里，全部采用贵公司的设计系统。'),
}


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    # column labels
    s.text(40, 50, t['l_tag'], fs=18, weight=700, fill=MUTED)
    s.text(720, 50, t['r_tag'], fs=18, weight=700, fill=ACCENT_INK)

    # ---- the slide (16:9-ish card)
    sx, sy, sw_, sh = 40, 70, 560, 330
    s.rect(sx, sy, sw_, sh, '#fff', LINE, r=14)
    s.text(sx + 28, sy + 46, t['sec'], fs=15, weight=600, fill=MUTED)
    y = s.text(sx + 28, sy + 84, t['head'], fs=26, weight=700, lh=1.3)
    # visual: three stages with arrows
    cy = sy + 230
    xs = [sx + 100, sx + 280, sx + 460]
    for i, (x, lab) in enumerate(zip(xs, t['steps'])):
        fill = ACCENT if i == 0 else PEACH
        s.out.append(f'<circle cx="{x}" cy="{cy}" r="34" fill="{fill}" stroke="{ACCENT}" stroke-width="2"/>')
        s.text(x, cy + 6, str(i + 1), fs=22, weight=700, fill='#fff' if i == 0 else ACCENT_INK, anchor='middle')
        s.text(x, cy + 62, lab, fs=15, weight=600, fill=MUTED, anchor='middle')
        if i < 2:
            s.arrow(x + 40, cy, xs[i + 1] - 42, cy)
    # requirement chip
    rw = tw(t['req'], 13) + 24
    s.rect(sx + sw_ - rw - 20, sy + 26, rw, 28, CREAM, LINE, r=14)
    s.text(sx + sw_ - rw / 2 - 20, sy + 45, t['req'], fs=13, weight=600, fill=MUTED, anchor='middle')

    # ---- link between slide and notes
    s.out.append(f'<line x1="604" y1="235" x2="716" y2="235" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="5 5"/>')
    lw = tw(t['link'], 12) + 14
    s.rect(660 - lw / 2, 200, lw, 24, '#fff', ACCENT, r=12, sw=1.5)
    s.text(660, 216, t['link'], fs=12, weight=700, fill=ACCENT_INK, anchor='middle')

    # ---- speaker notes
    nx, ny, nw, nh = 720, 70, 440, 330
    s.rect(nx, ny, nw, nh, PEACH, ACCENT, r=14, sw=2)
    s.text(nx + 24, ny + 40, t['notes'], fs=20, weight=700)
    s.rect(nx + 24, ny + 62, nw - 48, 2, LINE, r=1)
    s.text(nx + 24, ny + 96, t['key_lab'], fs=15, weight=700, fill=ACCENT_INK)
    s.rect(nx + 24, ny + 110, 6, 118, ACCENT, r=3)
    s.text(nx + 44, ny + 140, t['key'], fs=19, weight=600, maxw=nw - 80, lh=1.4)
    yy = ny + 258
    yy = s.text(nx + 24, yy, t['more'], fs=16, fill=MUTED, maxw=nw - 48)
    for i in range(2):
        ww = nw - 48 if i == 0 else (nw - 48) * 0.6
        s.rect(nx + 24, yy - 4 + i * 18, ww, 7, LINE, r=3)

    # ---- chain strip
    fs = 16
    pads = [tw(c, fs) + 36 for c in t['chain']]
    gap = 56
    total = sum(pads) + gap * (len(pads) - 1)
    x = (W - total) / 2
    by = 440
    for i, (c, w) in enumerate(zip(t['chain'], pads)):
        last = i == len(pads) - 1
        fill = INK if last else '#fff'
        s.rect(x, by, w, 40, fill, None if last else LINE, r=20)
        s.text(x + w / 2, by + 26, c, fs=fs, weight=700, fill='#fff' if last else INK, anchor='middle')
        if not last:
            s.arrow(x + w + 6, by + 20, x + w + gap - 8, by + 20)
        x += w + gap
    s.text(W / 2, 526, t['foot'], fs=17, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
