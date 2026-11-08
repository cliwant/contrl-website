#!/usr/bin/env python3
"""EP16 (Persuasive Writing) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep16.py
Writes images/blog/persuasive-writing/contrl-doubt-margin.svg (en) and .<lang>.svg (ko/ja/zh).

One page read the way an evaluator reads it: doubts sit in the margin beside each claim. Two are
already answered on the page; the third is open, and one line of chat feedback fills it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'persuasive-writing', 'contrl-doubt-margin'
H = 590

T = {
    'en': dict(
        title='A proposal page read the way an evaluator reads it, with a doubt in the margin beside each claim. Two doubts are already answered on the page; the third is open, and one line of chat feedback adds its answer',
        page='The page', margin='What the evaluator is thinking',
        rows=[('We are a small company.', 'Our references: major companies', 'A company this small?'),
              ('It will work in your setting.', 'Results from a similar project', 'Says who?'),
              ('It is worth the higher price.', 'Answer still missing', 'Why pay more?')],
        ok='answered', open='still open',
        chat='One line of chat feedback',
        line='“Add what this saves them, using our figures.”',
        foot='Read each page as the doubter would. Whatever doubt is left open is your next line of feedback.'),
    'ko': dict(
        title='평가위원의 눈으로 읽은 제안서 한 페이지. 주장마다 옆 여백에 의심이 적혀 있다. 두 개는 이미 페이지 안에서 답이 되었고, 세 번째는 비어 있어 채팅 피드백 한 줄로 답을 채운다',
        page='페이지', margin='평가위원의 머릿속',
        rows=[('우리는 작은 회사입니다.', '레퍼런스: 굴지의 기업들', '이렇게 작은 회사가?'),
              ('귀사 환경에서도 통합니다.', '유사 사업의 수행 결과', '누가 그래요?'),
              ('더 높은 금액만큼의 값을 합니다.', '아직 답이 없음', '왜 더 내야 하죠?')],
        ok='답함', open='아직 열려 있음',
        chat='채팅 피드백 한 줄',
        line='“절감 효과를 우리 수치로 넣어줘.”',
        foot='의심하는 사람의 눈으로 페이지를 읽으세요. 남아 있는 의심이 다음 피드백입니다.'),
    'ja': dict(
        title='評価者の目で読んだ提案書の一ページ。主張ごとに余白に疑問が書かれている。二つはすでにページ内で答えがあり、三つ目は空いていて、チャットのフィードバック一行で答えを加える',
        page='ページ', margin='評価者の頭の中',
        rows=[('当社は小さな会社です。', '実績：有力企業との仕事', 'こんなに小さな会社で？'),
              ('貴社の環境でも機能します。', '類似案件の結果', '誰がそう言っている？'),
              ('高い金額に見合う価値があります。', '答えがまだない', 'なぜ高く払うのか？')],
        ok='回答済み', open='未回答',
        chat='チャットのフィードバック一行',
        line='「削減効果を当社の数字で入れてください」',
        foot='疑う人の目でページを読みましょう。残った疑問が、次のフィードバックです。'),
    'zh': dict(
        title='以评审专家的眼光阅读提案书的一页：每条主张旁的页边都写着疑问。两条已在页面上得到回答，第三条仍空缺，用一行聊天反馈补上答案',
        page='这一页', margin='评审专家心里在想',
        rows=[('我们是一家小公司。', '业绩：知名大企业', '这么小的公司行吗？'),
              ('在贵方的环境中同样可行。', '类似项目的结果', '谁说的？'),
              ('更高的价格物有所值。', '还没有答案', '为什么要多付钱？')],
        ok='已回答', open='尚未回答',
        chat='一行聊天反馈',
        line='“用我们的数字写明能省下多少。”',
        foot='用怀疑者的眼光读每一页。还没回答的疑问，就是下一条反馈。'),
}


def check(s, cx, cy):
    s.out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="{ACCENT}"/>')
    s.out.append(f'<path d="M{cx - 5} {cy}l4 4l7 -8" fill="none" stroke="#fff" stroke-width="2.4"/>')


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    px, py, pw, ph = 40, 64, 640, 370
    mx = 770

    s.text(px, 46, t['page'], fs=18, weight=700, fill=MUTED)
    s.text(mx, 46, t['margin'], fs=18, weight=700, fill=ACCENT_INK)

    # the page, with a folded corner so it reads as a sheet and not a card
    s.rect(px, py, pw, ph, '#fff', LINE, r=6)
    fx = px + pw
    s.out.append(f'<path d="M{fx - 34} {py}L{fx} {py + 34}L{fx - 34} {py + 34}z" fill="{CREAM}" stroke="{LINE}" stroke-width="1.5"/>')

    row_h = 116
    for i, (claim, answer, doubt) in enumerate(t['rows']):
        is_open = i == 2
        y = py + 24 + i * row_h
        # claim, with placeholder text lines beneath it
        s.text(px + 28, y + 22, claim, fs=21, weight=700)
        # answer strip on the page
        ay = y + 38
        aw = pw - 56
        if is_open:
            s.rect(px + 28, ay, aw, 44, PEACH, ACCENT, r=8, sw=2, dash='6 5')
            s.text(px + 46, ay + 28, answer, fs=16, weight=600, fill=ACCENT_INK)
        else:
            s.rect(px + 28, ay, aw, 44, CREAM, None, r=8)
            s.rect(px + 28, ay, 5, 44, ACCENT, r=2)
            s.text(px + 46, ay + 28, answer, fs=16, weight=600)

        # margin note: speech bubble with a tail pointing at the claim
        by, bh = y + 2, 80
        bx, bw = mx, W - mx - 40
        stroke = ACCENT if is_open else LINE
        fill = PEACH if is_open else '#fff'
        s.out.append(f'<line x1="{px + pw + 4}" y1="{by + bh / 2}" x2="{bx - 14}" y2="{by + bh / 2}" '
                     f'stroke="{ACCENT if is_open else GRAY_TXT}" stroke-width="2" stroke-dasharray="3 6"/>')
        s.rect(bx, by, bw, bh, fill, stroke, r=18, sw=2 if is_open else 1.5)
        s.out.append(f'<path d="M{bx + 1} {by + bh / 2 - 9}L{bx - 13} {by + bh / 2}L{bx + 1} {by + bh / 2 + 9}" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="{2 if is_open else 1.5}"/>')
        s.text(bx + 22, by + 34, doubt, fs=20, weight=700, fill=ACCENT_INK if is_open else INK)
        if is_open:
            s.text(bx + 22, by + 62, t['open'], fs=15, weight=700, fill=ACCENT_INK)
        else:
            check(s, bx + 33, by + 56)
            s.text(bx + 52, by + 62, t['ok'], fs=15, weight=600, fill=MUTED)

    # chat line, feeding up into the open slot
    cy = py + ph + 26
    cw_ = pw
    s.rect(px, cy, cw_, 58, INK, r=29)
    lab_w = tw(t['chat'], 13) + 24
    s.rect(px + 14, cy + 15, lab_w, 28, ACCENT, r=14)
    s.text(px + 14 + lab_w / 2, cy + 34, t['chat'], fs=13, weight=700, fill='#fff', anchor='middle')
    s.text(px + 14 + lab_w + 14, cy + 36, t['line'], fs=17, weight=600, fill='#fff')
    ax = px + pw - 60
    s.arrow(ax, cy - 2, ax, py + 24 + 2 * row_h + 86)

    s.text(W / 2, H - 22, t['foot'], fs=17, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
