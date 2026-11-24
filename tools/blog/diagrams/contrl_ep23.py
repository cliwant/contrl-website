#!/usr/bin/env python3
"""EP23 (Resumes) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep23.py
Writes images/blog/resumes/contrl-resume-filter.svg (en) and .<lang>.svg.

A sieve from a career to a proposal page. Left: one person's full career record (the street resume),
eight entries in gray. Middle: the personnel requirements Contrl extracted from the RFP for the
proposed role, each with its RFP reference. Right: the proposal resume page for that role. Only the
entries that answer a requirement pass through; each lands on the page tagged with the requirement it
answers, and the rest are left out.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'resumes', 'contrl-resume-filter'
H = 680

# which career entry (index) answers which requirement (index); others are left out
LINKS = [(1, 0), (3, 1), (4, 2), (6, 3)]
REFS = ['4.2.1', '4.2.2', '4.2.3', '4.2.4']

T = {
    'en': dict(
        title='From a career to a proposal page. On the left, one person\'s full career record with eight entries. In the middle, the four personnel requirements Contrl extracted from the RFP for the proposed role, each with its RFP reference. On the right, the proposal resume page for that role: only the four entries that answer a requirement pass through, each tagged with the requirement it answers, and the other four are left out',
        head='The RFP decides what reaches the page, not the length of the career',
        left_h='Street resume', left_sub='Everything the person has done',
        career=['2024  Internal tools upgrade', '2023  Service desk lead, 30 agents',
                '2022  Office move logistics', '2021  ITIL certification',
                '2019  24/7 desk for a city agency', '2017  Sales support role',
                '2016  Cut ticket backlog by 40%', '2012  B.Sc. computing'],
        mid_h='In Contrl', mid_sub='Personnel requirements\nextracted from the RFP',
        reqs=['Leads a desk of 20+ agents', 'Holds ITIL certification',
              'Public-sector 24/7 operations', 'Shown service improvement'],
        right_h='Proposal resume', role='Service desk lead · RFP 4.2',
        out='Gray: left out of the proposal page',
        foot='Your team supplies the facts. The RFP decides which ones belong; each line cites the requirement it answers.'),
    'ko': dict(
        title='경력에서 제안서 페이지로. 왼쪽은 한 사람의 전체 경력 기록으로 항목이 여덟 개다. 가운데는 Contrl이 제안요청서에서 추출한 해당 역할의 인력 요구사항 네 개로 각각 출처 조항이 붙어 있다. 오른쪽은 그 역할의 제안용 이력서 페이지로, 요구사항에 답하는 경력 네 개만 통과해 대응하는 요구사항 번호가 붙고 나머지 네 개는 빠진다',
        head='페이지에 무엇이 오를지는 경력의 길이가 아니라 제안요청서가 정한다',
        left_h='일반 이력서', left_sub='그 사람이 해 온 모든 일',
        career=['2024  사내 도구 개선', '2023  서비스 데스크 리드, 상담원 30명',
                '2022  사무실 이전 지원', '2021  ITIL 자격 취득',
                '2019  시 기관 24시간 데스크', '2017  영업 지원 업무',
                '2016  미처리 티켓 40% 감축', '2012  컴퓨터공학 학사'],
        mid_h='Contrl에서', mid_sub='제안요청서에서 추출한\n인력 요구사항',
        reqs=['상담원 20명 이상 데스크 관리', 'ITIL 자격 보유',
              '공공 부문 24시간 운영 경험', '서비스 개선 실적'],
        right_h='제안용 이력서', role='서비스 데스크 리드 · 4.2항',
        out='회색: 제안용 이력서에서 제외',
        foot='사람에 대한 사실은 팀이 제공합니다. 무엇을 넣을지는 제안요청서가 정하고, 각 줄에는 대응하는 요구사항이 표시됩니다.'),
    'ja': dict(
        title='職歴から提案書のページへ。左は一人の職歴の全記録で、項目は八つ。中央は、ContrlがRFPから抽出したその役割の要員要件四つで、それぞれ出典の条項番号が付いている。右はその役割の提案用履歴書のページで、要件に答える四つの経歴だけが通り、対応する要件番号が付く。残りの四つは外される',
        head='ページに載るものを決めるのは職歴の長さではなく、RFPです',
        left_h='一般の履歴書', left_sub='その人がしてきたことのすべて',
        career=['2024  社内ツールの改善', '2023  サービスデスク責任者、30名',
                '2022  オフィス移転の支援', '2021  ITIL資格を取得',
                '2019  市の機関の24時間デスク', '2017  営業支援の業務',
                '2016  未処理チケットを40%削減', '2012  情報工学の学士'],
        mid_h='Contrlで', mid_sub='RFPから抽出した\n要員要件',
        reqs=['20名以上のデスクを統括', 'ITIL資格を保有',
              '公共部門の24時間運用', 'サービス改善の実績'],
        right_h='提案用の履歴書', role='サービスデスク責任者 · RFP 4.2',
        out='グレー：提案用の履歴書から外す',
        foot='人についての事実はチームが用意します。どれを載せるかはRFPが決め、各行には対応する要件が示されます。'),
    'zh': dict(
        title='从职业经历到提案页面。左边是一个人完整的职业记录，共八项。中间是Contrl从招标文件中为该岗位提取的四项人员要求，每项都标有出处条款。右边是该岗位的提案简历页面：只有回应要求的四项经历能通过，并标上对应的要求编号，其余四项被舍去',
        head='决定哪些内容上页面的是招标文件，而不是履历的长度',
        left_h='通用简历', left_sub='这个人做过的所有事情',
        career=['2024  内部工具升级', '2023  服务台负责人，30名坐席',
                '2022  办公室搬迁支持', '2021  取得ITIL认证',
                '2019  市级机构7×24服务台', '2017  销售支持岗位',
                '2016  积压工单减少40%', '2012  计算机专业学士'],
        mid_h='在Contrl中', mid_sub='从招标文件提取的\n人员要求',
        reqs=['管理20名以上坐席的服务台', '持有ITIL认证',
              '公共部门7×24运营经验', '有服务改进的实绩'],
        right_h='提案简历', role='服务台负责人 · 第4.2条',
        out='灰色：不放入提案简历',
        foot='关于这个人的事实由团队提供；放哪些内容由招标文件决定，每一行都标明它回应的要求。'),
}

LX, LW = 30, 330            # career card
MX, MW = 420, 340           # Contrl panel
RX, RW = 820, 350           # proposal page
TOP = 92
EY0, EH = 176, 44           # career entry rows
RY0, RH = 214, 70           # requirement rows
PY0, PH = 214, 70           # page rows


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    s.text(40, 52, t['head'], fs=22, weight=800, maxw=1120)

    # left: the long career record
    s.rect(LX, TOP, LW, EY0 - TOP + EH * 8 + 14, GRAY_BOX, GRAY_TXT, r=14, sw=1.2)
    s.text(LX + 20, TOP + 34, t['left_h'], fs=18, weight=800)
    s.text(LX + 20, TOP + 60, t['left_sub'], fs=14, weight=600, fill=MUTED)
    used = {c for c, _ in LINKS}
    for i, line in enumerate(t['career']):
        y = EY0 + i * EH
        hit = i in used
        s.rect(LX + 14, y + 4, LW - 28, EH - 8, '#fff' if hit else GRAY_BOX, ACCENT if hit else LINE,
               r=8, sw=1.6 if hit else 1)
        s.text(LX + 26, y + EH / 2 + 5, line, fs=14, weight=700 if hit else 500,
               fill=INK if hit else GRAY_TXT)
    # legend under the card: gray entries never reach the page
    s.rect(LX + 14, 562, 26, 18, GRAY_BOX, LINE, r=5, sw=1)
    s.text(LX + 50, 577, t['out'], fs=14, weight=600, fill=MUTED)

    # middle: Contrl panel with the extracted requirements (the sieve)
    ph = RY0 - TOP + RH * 4 + 10
    s.rect(MX, TOP, MW, ph, CREAM, ACCENT, r=16, sw=2)
    s.pill(MX + 20, TOP + 16, t['mid_h'], fs=15)
    s.text(MX + 20, TOP + 76, t['mid_sub'], fs=14, weight=600, fill=MUTED, lh=1.35)
    for j, req in enumerate(t['reqs']):
        y = RY0 + j * RH
        s.rect(MX + 16, y + 6, MW - 32, RH - 12, '#fff', LINE, r=10, sw=1.5)
        s.text(MX + 30, y + 30, REFS[j], fs=13, weight=800, fill=ACCENT_INK)
        s.text(MX + 30, y + 50, req, fs=15, weight=700)

    # right: the proposal resume page
    s.rect(RX, TOP, RW, ph, '#fff', INK, r=10, sw=1.6)
    s.rect(RX, TOP, RW, 70, PEACH, None, r=10)
    s.out.append(f'<rect x="{RX}" y="{TOP}" width="6" height="{ph}" fill="{ACCENT}"/>')
    s.text(RX + 22, TOP + 30, t['right_h'], fs=18, weight=800)
    s.text(RX + 22, TOP + 56, t['role'], fs=14, weight=700, fill=ACCENT_INK)

    # links: career entry -> requirement -> page line
    for c, r in LINKS:
        ey = EY0 + c * EH + EH / 2
        ry = RY0 + r * RH + RH / 2
        s.path(f'M{LX + LW - 14} {ey} C{LX + LW + 30} {ey} {MX - 30} {ry} {MX + 12} {ry}', sw=2.2)
        s.arrow(MX + MW - 14, ry, RX + 14, ry, sw=2.2)
        # line on the page: the career entry, tagged with the requirement it answers
        py = PY0 + r * PH
        entry = t['career'][c].split('  ', 1)[1]
        s.rect(RX + 18, py + 8, RW - 34, PH - 16, PEACH, LINE, r=8, sw=1.2)
        pw = s.pill(RX + 30, py + PH / 2 - 14, '✓ ' + REFS[r], fs=12)
        s.text(RX + 30 + pw + 12, py + PH / 2 + 5, entry, fs=15, weight=700)

    s.text(40, 630, t['foot'], fs=17, fill=MUTED, maxw=1120, lh=1.45)
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in T:
        fn = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fn), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print('wrote', fn)
