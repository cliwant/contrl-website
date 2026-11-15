#!/usr/bin/env python3
"""EP21 (Managing Questions to the Customer) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep21.py
Writes images/blog/managing-questions-to-the-customer/contrl-question-window.svg (en) and .<lang>.svg.

Two swimlanes over the same question window (RFP released -> question deadline -> last answers ->
proposal due). By hand, shredding the RFP fills most of the window, questions go in at the last
minute and come back in the last batch. With Contrl, extraction happens on day one, the team reviews
one list, the important questions go in early and come back in the first batch, leaving time to
change the plan.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'managing-questions-to-the-customer', 'contrl-question-window'
H = 540

T = {
    'en': dict(
        title='Two timelines of the same RFP question window. By hand, breaking down the RFP fills most of the window, questions go in just before the deadline and are answered in the last batch. With Contrl, requirements, outline and evaluation criteria are extracted on day one, technical, contracts and finance review one list, important questions go in early and are answered in the first batch, leaving time to change the plan',
        head='One question window, two ways to spend it',
        ms=['RFP released', 'Question deadline', 'Last answers', 'Proposal due'],
        lane1='By hand', lane2='With Contrl',
        shred='Breaking down the RFP by hand', late='Questions at the last minute',
        lastA='Answers in the last batch', little='Little time left to change the plan',
        ext='Extract', extnote='Day one:\nrequirements,\noutline, criteria',
        review='Team review', reviewnote='Technical · contracts · finance',
        firstA='Answers in the first batch', time='Time to update solution, price and outline',
        foot='Same RFP, same deadline. When the breakdown is done on day one, the window is spent on asking good questions.'),
    'ko': dict(
        title='같은 제안요청서 질의 기간을 두 가지 타임라인으로 비교한다. 직접 분석하면 제안요청서를 쪼개는 일이 기간 대부분을 차지해 질의는 마감 직전에 나가고 답변도 마지막 묶음으로 온다. Contrl을 쓰면 첫날 요구사항, 목차, 평가 기준이 추출되고 기술·계약·재무 담당이 같은 목록을 검토해 중요한 질의를 일찍 보내고 첫 묶음에서 답을 받아 계획을 바꿀 시간이 남는다',
        head='같은 질의 기간, 두 가지 쓰임',
        ms=['공고', '질의 마감', '마지막 답변', '제안서 제출'],
        lane1='직접 분석', lane2='Contrl 사용',
        shred='제안요청서를 손으로 쪼개는 중', late='마감 직전에 질의',
        lastA='마지막 묶음으로 답변', little='계획을 바꿀 시간이 거의 없음',
        ext='추출', extnote='첫날:\n요구사항,\n목차, 평가 기준',
        review='팀 검토', reviewnote='기술 · 계약 · 재무',
        firstA='첫 묶음으로 답변', time='해결 방안, 가격, 목차를 고칠 시간',
        foot='제안요청서도 마감도 같습니다. 분석을 첫날 끝내면 질의 기간을 좋은 질문을 쓰는 데 쓸 수 있습니다.'),
    'ja': dict(
        title='同じRFP質問期間を2本のタイムラインで比べる。手作業ではRFPの分解が期間の大半を占め、質問は締切直前に出て回答も最後のまとまりで届く。Contrlでは初日に要件、目次、評価基準が抽出され、技術・契約・財務が同じ一覧を確認し、重要な質問を早く出して最初のまとまりで回答を受け、計画を変える時間が残る',
        head='同じ質問期間、二つの使い方',
        ms=['RFP公示', '質問締切', '最後の回答', '提案書提出'],
        lane1='手作業', lane2='Contrlを使う',
        shred='RFPを手作業で分解中', late='締切直前に質問',
        lastA='最後のまとまりで回答', little='計画を変える時間はわずか',
        ext='抽出', extnote='初日：\n要件、目次、\n評価基準',
        review='チームで確認', reviewnote='技術・契約・財務',
        firstA='最初のまとまりで回答', time='解決策・価格・目次を見直す時間',
        foot='RFPも締切も同じです。分解を初日に終えれば、質問期間を良い質問づくりに使えます。'),
    'zh': dict(
        title='用两条时间线比较同一个招标答疑期。手工拆解招标文件占去大部分时间，问题在截止前才提交，答复也在最后一批才到。使用Contrl时，第一天就提取出需求、目录和评分标准，技术、合同和财务人员审阅同一份清单，重要问题尽早提交并在第一批得到答复，留出调整方案的时间',
        head='同一个答疑期，两种用法',
        ms=['发布招标', '提问截止', '最后答复', '提交投标'],
        lane1='手工拆解', lane2='使用Contrl',
        shred='手工拆解招标文件', late='截止前才提问',
        lastA='最后一批才答复', little='几乎没有时间调整方案',
        ext='提取', extnote='第一天：\n需求、目录、\n评分标准',
        review='团队审阅', reviewnote='技术 · 合同 · 财务',
        firstA='第一批即答复', time='有时间调整方案、价格和目录',
        foot='同样的招标文件，同样的截止日。第一天完成拆解，答疑期就能用来写好问题。'),
}

X0, X1 = 230, 1150                      # timeline span
MS = [X0, 640, 830, X1]                 # milestone x positions
L1, L2 = 140, 296                       # lane tops
LH = 136                                # lane 1 height
LH2 = 150                               # lane 2 height


def circle(s, x, y, ch, fill, color='#fff', r=12):
    s.out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')
    s.text(x, y + 5, ch, fs=13, weight=800, fill=color, anchor='middle')


def bar(s, x0, x1, y, h, fill, stroke, label, fs=15, color=INK, weight=700):
    s.rect(x0, y, x1 - x0, h, fill, stroke, r=8, sw=1.5)
    s.text((x0 + x1) / 2, y + h / 2 + fs * 0.36, label, fs=fs, weight=weight, fill=color, anchor='middle')


def label_bg(s, x, y, txt, fs, bg, color, weight):
    w = tw(txt, fs)
    s.rect(x - 4, y - fs, w + 8, fs + 7, bg, r=3)
    s.text(x, y, txt, fs=fs, weight=weight, fill=color)


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    s.text(40, 52, t['head'], fs=22, weight=800)

    # lanes
    s.rect(30, L1, 1140, LH, '#fff', LINE, r=14, sw=1.5)
    s.rect(30, L2, 1140, LH2, CREAM, ACCENT, r=14, sw=2)
    s.text(50, L1 + LH / 2 + 6, t['lane1'], fs=17, weight=800, fill=MUTED)
    s.text(50, L2 + LH2 / 2 + 6, t['lane2'], fs=17, weight=800, fill=ACCENT_INK)

    # milestones: labels on top, dashed guides through both lanes
    for i, (x, lab) in enumerate(zip(MS, t['ms'])):
        anchor = 'start' if i == 0 else ('end' if i == 3 else 'middle')
        s.text(x, 104, lab, fs=15, weight=800 if i == 1 else 700, fill=ACCENT_INK if i == 1 else INK, anchor=anchor)
        s.out.append(f'<line x1="{x}" y1="{116}" x2="{x}" y2="{L2 + LH2 + 10}" stroke="{ACCENT if i == 1 else GRAY_TXT}" '
                     f'stroke-width="{2 if i == 1 else 1.2}" stroke-dasharray="5 5"/>')

    # lane 1: by hand
    by = L1 + 28
    bar(s, X0, 540, by, 44, GRAY_BOX, GRAY_TXT, t['shred'], fs=15, color=MUTED)
    circle(s, 562, by + 22, 'Q', GRAY_TXT)
    circle(s, 590, by + 22, 'Q', GRAY_TXT)
    s.out.append(f'<line x1="606" y1="{by + 22}" x2="814" y2="{by + 22}" stroke="{GRAY_TXT}" stroke-width="2.5" '
                 f'stroke-dasharray="6 5" marker-end="url(#ah-{GRAY_TXT[1:]})"/>')
    circle(s, MS[2], by + 22, 'A', GRAY_TXT, r=13)
    bar(s, 850, X1, by + 8, 28, '#fff', GRAY_TXT, t['little'], fs=13, color=MUTED, weight=600)
    s.text(600, by + 76, t['late'], fs=14, weight=600, fill=MUTED, anchor='end')
    label_bg(s, 816, by + 76, t['lastA'], 14, '#fff', MUTED, 600)

    # lane 2: with Contrl
    cy = L2 + 22
    bar(s, X0, 300, cy, 44, ACCENT, None, t['ext'], fs=15, color='#fff', weight=800)
    bar(s, 306, 520, cy, 44, PEACH, ACCENT, t['review'], fs=15, color=ACCENT_INK)
    circle(s, 540, cy + 22, 'Q', ACCENT)
    circle(s, 566, cy + 22, 'Q', ACCENT)
    s.arrow(580, cy + 22, 596, cy + 22)
    circle(s, 612, cy + 22, 'A', ACCENT, r=13)
    s.rect(632, cy, X1 - 632, 44, PEACH, ACCENT, r=8, sw=2)
    s.text((632 + X1) / 2, cy + 27, t['time'], fs=15, weight=800, fill=ACCENT_INK, anchor='middle')
    s.text(X0 + 6, cy + 70, t['extnote'], fs=13, weight=600, fill=ACCENT_INK, lh=1.35)
    s.text(345, cy + 70, t['reviewnote'], fs=13, weight=600, fill=MUTED)
    label_bg(s, 598, cy + 70, t['firstA'], 14, CREAM, ACCENT_INK, 700)

    s.text(40, 496, t['foot'], fs=17, fill=MUTED, maxw=1120, lh=1.45)
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in T:
        fn = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fn), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print('wrote', fn)
