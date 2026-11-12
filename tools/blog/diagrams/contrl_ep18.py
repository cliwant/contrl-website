#!/usr/bin/env python3
"""EP18 (Headings) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep18.py
Writes images/blog/headings/contrl-heading-anatomy.svg (en) and .<lang>.svg (ko/ja/zh).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'headings', 'contrl-heading-anatomy'
H = 600

T = {
    'en': dict(
        title='Anatomy of the top of one slide in Contrl: the section number and title follow the RFP required outline so evaluators can find it, the headline states the benefit from the win theme, and a tag cites the RFP requirements the page answers',
        l_tag='The top of one slide', r_tag='What each part does',
        sec='2.3  Data migration', head='Every record is checked twice\nbefore the switch',
        chip='Answers RFP req. 2.3-1, 2.3-2',
        cards=[('Findable', 'Number and title follow the RFP’s required outline'),
               ('Message', 'The headline states the benefit, drawn from your win theme'),
               ('Traceable', 'The page cites the RFP requirements it answers')],
        foot='Evaluators find the page by the RFP’s outline; the headline tells them why it matters.'),
    'ko': dict(
        title='Contrl 슬라이드 한 장의 윗부분 해부: 장 번호와 제목은 제안요청서가 정한 목차를 따라 평가위원이 찾을 수 있고, 헤드라인은 윈 테마에서 나온 효과를 말하며, 표시는 이 페이지가 답하는 제안요청서 요구사항을 밝힌다',
        l_tag='슬라이드 한 장의 윗부분', r_tag='각 부분이 하는 일',
        sec='2.3  데이터 이관', head='모든 데이터를 두 번 검증한 뒤\n전환합니다',
        chip='제안요청서 요구사항 2.3-1, 2.3-2 대응',
        cards=[('찾을 수 있다', '번호와 제목은\n제안요청서가 정한 목차 그대로'),
               ('메시지가 있다', '헤드라인이 효과를 말한다.\n윈 테마에서 나온 문장'),
               ('추적할 수 있다', '이 페이지가 답하는\n제안요청서 요구사항을 표시')],
        foot='평가위원은 제안요청서 목차로 페이지를 찾고, 헤드라인에서 왜 중요한지 읽습니다.'),
    'ja': dict(
        title='Contrlのスライド1枚の上部の構造：章番号と題はRFPが指定した目次に従うので評価者が見つけられ、見出しはウィンテーマから来る便益を語り、タグはそのページが答えるRFP要件を示す',
        l_tag='スライド1枚の上部', r_tag='それぞれの役割',
        sec='2.3  データ移行', head='すべてのデータを二重に検証してから\n切り替えます',
        chip='RFP要件2.3-1、2.3-2に対応',
        cards=[('見つけられる', '番号と題はRFPが指定した目次のとおり'),
               ('メッセージがある', '見出しが便益を語る。\nウィンテーマから生まれた一文'),
               ('たどれる', 'このページが答えるRFP要件を表示')],
        foot='評価者はRFPの目次でページを見つけ、見出しでその意味を知ります。'),
    'zh': dict(
        title='Contrl 中一张幻灯片顶部的构成：章节编号和标题沿用招标文件规定的提纲，评审专家找得到；主标题说出来自制胜主题的收益；标签注明本页回应的招标需求',
        l_tag='一张幻灯片的顶部', r_tag='每一部分的作用',
        sec='2.3  数据迁移', head='每条记录双重核验后\n再切换',
        chip='回应招标需求 2.3-1、2.3-2',
        cards=[('找得到', '编号和标题沿用招标文件规定的提纲'),
               ('有信息', '主标题说出收益，来自制胜主题'),
               ('可追溯', '注明本页回应的招标需求')],
        foot='评审专家按招标文件的提纲找到这一页，再从主标题读出它为什么重要。'),
}


def badge(s, x, y, n, filled=True):
    s.out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{ACCENT if filled else "#fff"}" '
                 f'stroke="{ACCENT}" stroke-width="2"/>')
    s.text(x, y + 6, str(n), fs=16, weight=700, fill='#fff' if filled else ACCENT_INK, anchor='middle')


def leader(s, x1, y1, x2, y2):
    mx = (x1 + x2) / 2
    s.out.append(f'<path d="M{x1} {y1} C{mx} {y1} {mx} {y2} {x2} {y2}" fill="none" stroke="{ACCENT}" '
                 f'stroke-width="2" stroke-dasharray="6 5"/>')


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    s.text(40, 50, t['l_tag'], fs=18, weight=700, fill=MUTED)
    s.text(800, 50, t['r_tag'], fs=18, weight=700, fill=ACCENT_INK)

    # ---- the slide top, zoomed in
    sx, sy, sw_, sh = 40, 74, 660, 440
    s.rect(sx, sy, sw_, sh, '#fff', LINE, r=14)
    # 1: section number + title, from the RFP's required outline
    s.rect(sx + 24, sy + 28, tw(t['sec'], 20) + 32, 44, CREAM, LINE, r=10)
    s.text(sx + 40, sy + 57, t['sec'], fs=20, weight=700, fill=MUTED)
    # 2: headline
    s.rect(sx + 24, sy + 104, 6, 92, ACCENT, r=3)
    s.text(sx + 46, sy + 138, t['head'], fs=30, weight=800, lh=1.3)
    # 3: requirement tag
    cw_ = tw(t['chip'], 14) + 28
    s.rect(sx + 46, sy + 222, cw_, 32, PEACH, ACCENT, r=16, sw=1.5)
    s.text(sx + 46 + cw_ / 2, sy + 243, t['chip'], fs=14, weight=700, fill=ACCENT_INK, anchor='middle')
    # body placeholder lines
    by = sy + 292
    for i, f in enumerate([1, 0.92, 0.97, 0.6, 0, 0.88, 0.75]):
        if f:
            s.rect(sx + 46, by + i * 20, (sw_ - 92) * f, 8, GRAY_BOX, r=4)

    # ---- annotation cards, linked to badges on the slide edge
    cx, cwid, ch = 800, 360, 118
    ys = [84, 236, 388]
    targets = [sy + 50, sy + 150, sy + 238]
    ex = sx + sw_
    ends = [sx + 24 + tw(t['sec'], 20) + 32,
            sx + 46 + max(tw(ln, 30) for ln in t['head'].split('\n')) * (1.06 if lang == 'en' else 0.9),
            sx + 46 + cw_]
    for i, ((lab, desc), y, ty) in enumerate(zip(t['cards'], ys, targets)):
        s.out.append(f'<line x1="{ends[i] + 14}" y1="{ty}" x2="{ex}" y2="{ty}" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>')
        leader(s, ex + 15, ty, cx - 2, y + 34)
        badge(s, ex, ty, i + 1)
        hi = i == 1
        s.rect(cx, y, cwid, ch, PEACH if hi else '#fff', ACCENT if hi else LINE, r=14, sw=2 if hi else 1.5)
        badge(s, cx + 32, y + 34, i + 1)
        s.text(cx + 58, y + 41, lab, fs=20, weight=700, fill=ACCENT_INK if hi else INK)
        s.text(cx + 24, y + 76, desc, fs=16, fill=MUTED, maxw=cwid - 48, lh=1.35)

    s.text(W / 2, 566, t['foot'], fs=17, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
