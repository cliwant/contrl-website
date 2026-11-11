#!/usr/bin/env python3
"""EP17 (Writing Clearly) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep17.py
Writes images/blog/writing-clearly/contrl-sentence-profile.svg (en) and .<lang>.svg (ko/ja/zh).

The sentence-length profile of one page, before and after one line of chat feedback: each bar is a
sentence, its length in words, with the sentence's subject beside it. Before: four long sentences
whose subjects are abstract nouns. After: nine short ones, all under the 15-word line, each with a
person or team as subject.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'writing-clearly', 'contrl-sentence-profile'
H = 640

BEFORE = [38, 29, 44, 26]
AFTER = [12, 9, 14, 11, 8, 13, 10, 12, 7]

T = {
    'en': dict(
        title='Sentence-length profile of one page before and after one line of chat feedback. Before: four sentences averaging 34 words, with abstract nouns as subjects. After: nine sentences averaging 11 words, all under the 15-word line, each with a person or team as subject',
        chat='One line of chat feedback',
        line='“Say who does each step. Keep sentences under 15 words.”',
        left='Draft page', right='After the feedback',
        subj='Subject', bar='Words per sentence', limit='15 words',
        bs=['Implementation', 'Support', 'It', 'Monitoring'],
        as_=['We', 'Your staff', 'Our engineers', 'We', 'You', 'Our team', 'Your manager', 'We', 'You'],
        lstat='4 sentences · avg 34 words · 0 people as subjects',
        rstat='9 sentences · avg 11 words · 9 people as subjects',
        foot='Same page, same content. Shorter sentences, and people doing the work.'),
    'ko': dict(
        title='채팅 피드백 한 줄 전후로 본 한 페이지의 문장 길이. 전: 평균 34단어의 문장 네 개, 주어는 추상 명사. 후: 평균 11단어의 문장 아홉 개, 모두 15단어 선 아래이고 주어는 모두 사람이나 팀',
        chat='채팅 피드백 한 줄',
        line='“단계마다 누가 하는지 쓰고, 문장은 15단어 안으로.”',
        left='초안 페이지', right='피드백 후',
        subj='주어', bar='문장당 단어 수', limit='15단어',
        bs=['구축', '지원', '이는', '모니터링'],
        as_=['저희', '직원분들', '엔지니어', '저희', '귀 기관', '운영팀', '담당자', '저희', '귀 기관'],
        lstat='문장 4개 · 평균 34단어 · 사람 주어 0개',
        rstat='문장 9개 · 평균 11단어 · 사람 주어 9개',
        foot='같은 페이지, 같은 내용. 문장은 짧아지고 일하는 사람이 보입니다.'),
    'ja': dict(
        title='チャットのフィードバック一行の前後で見た、一ページの文の長さ。前：平均34語の文が四つで、主語は抽象名詞。後：平均11語の文が九つで、すべて15語の線より短く、主語はすべて人やチーム',
        chat='チャットのフィードバック一行',
        line='「各ステップを誰がやるか書いて。一文は15語以内に」',
        left='下書きのページ', right='フィードバック後',
        subj='主語', bar='一文あたりの語数', limit='15語',
        bs=['導入', '支援', 'これは', '監視'],
        as_=['当社', '貴社職員', 'エンジニア', '当社', '貴社', '運用チーム', '担当者', '当社', '貴社'],
        lstat='4文 · 平均34語 · 人が主語の文 0',
        rstat='9文 · 平均11語 · 人が主語の文 9',
        foot='同じページ、同じ内容。文は短くなり、働く人が見えるようになります。'),
    'zh': dict(
        title='一行聊天反馈前后，同一页的句子长度分布。之前：四个句子，平均34个词，主语是抽象名词。之后：九个句子，平均11个词，全部低于15词线，主语都是人或团队',
        chat='一行聊天反馈',
        line='“写清每一步由谁来做，每句不超过15个词。”',
        left='初稿页面', right='反馈之后',
        subj='主语', bar='每句词数', limit='15个词',
        bs=['实施', '支持', '这', '监控'],
        as_=['我们', '贵方员工', '我方工程师', '我们', '贵方', '运维团队', '贵方负责人', '我们', '贵方'],
        lstat='4句 · 平均34词 · 以人为主语 0句',
        rstat='9句 · 平均11词 · 以人为主语 9句',
        foot='同一页，同样的内容。句子变短了，做事的人也出现了。'),
}

PX = (40, 640)      # panel x
PW = 520            # panel width
PY, PH = 120, 445   # panel y, height
SUBJ_W = 130        # subject column
SCALE = 7.4         # px per word
ROW = 30


def panel(s, t, x, lengths, subjects, title, stat, good):
    s.rect(x, PY, PW, PH, PEACH if good else CREAM, ACCENT if good else LINE, r=14, sw=2 if good else 1.5)
    s.text(x + 24, PY + 38, title, fs=20, weight=700, fill=ACCENT_INK if good else INK)
    s.text(x + 24, PY + 66, stat, fs=14, weight=600, fill=ACCENT_INK if good else MUTED)
    hy = PY + 100
    s.text(x + 24, hy, t['subj'], fs=13, weight=700, fill=MUTED)
    bx = x + 24 + SUBJ_W
    s.text(bx, hy, t['bar'], fs=13, weight=700, fill=MUTED)
    # 15-word guideline
    lx = bx + 15 * SCALE
    top, bot = hy + 12, PY + PH - 20
    s.out.append(f'<line x1="{lx}" y1="{top}" x2="{lx}" y2="{bot}" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="5 5"/>')
    s.text(lx + 6, bot - 4, t['limit'], fs=13, weight=700, fill=ACCENT_INK)
    y = hy + 22
    for n, sub in zip(lengths, subjects):
        s.text(x + 24, y + 17, sub, fs=15, weight=600 if good else 400,
               fill=INK if good else GRAY_TXT)
        w = n * SCALE
        if good:
            s.rect(bx, y + 3, w, 18, ACCENT, r=4)
        else:
            s.rect(bx, y + 3, 15 * SCALE, 18, '#d4d4d8', r=4)
            s.rect(bx + 15 * SCALE, y + 3, w - 15 * SCALE, 18, GRAY_TXT, r=4)
        nx = lx + 12 if good else bx + w + 8  # after-panel numbers sit in a column past the line
        s.text(nx, y + 17, str(n), fs=14, weight=700, fill=ACCENT_INK if good else MUTED)
        y += ROW + (14 if not good else 0)


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    # chat feedback bar across the top
    cw_ = tw(t['chat'], 13) + 24
    lw = tw(t['line'], 17)
    total = cw_ + 14 + lw + 28
    cx = (W - total) / 2
    s.rect(cx, 30, total, 56, INK, r=28)
    s.rect(cx + 14, 44, cw_, 28, ACCENT, r=14)
    s.text(cx + 14 + cw_ / 2, 63, t['chat'], fs=13, weight=700, fill='#fff', anchor='middle')
    s.text(cx + 14 + cw_ + 14, 64, t['line'], fs=17, weight=600, fill='#fff')

    panel(s, t, PX[0], BEFORE, t['bs'], t['left'], t['lstat'], False)
    panel(s, t, PX[1], AFTER, t['as_'], t['right'], t['rstat'], True)
    # arrow between panels, fed from the chat line
    s.arrow(PX[0] + PW + 8, PY + PH / 2, PX[1] - 8, PY + PH / 2)
    s.out.append(f'<line x1="{W / 2}" y1="88" x2="{W / 2}" y2="{PY + PH / 2 - 4}" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="3 6"/>')

    s.text(W / 2, H - 28, t['foot'], fs=17, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in ['en', 'ko', 'ja', 'zh']:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
