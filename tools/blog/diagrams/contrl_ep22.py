#!/usr/bin/env python3
"""EP22 (Relevant Past Performance) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep22.py
Writes images/blog/relevant-past-performance/contrl-coverage-grid.svg (en) and .<lang>.svg.

A past performance coverage grid. The rows are requirements Contrl extracted from the RFP (each with
its RFP reference); the columns are the candidate projects your team chose. Dots mark which project
covers which requirement; the last row has none and is flagged as a gap.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'relevant-past-performance', 'contrl-coverage-grid'
H = 610

COVER = [  # rows x projects (B, C, D)
    (1, 1, 0),
    (1, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
    (0, 0, 0),
]

T = {
    'en': dict(
        title='A past performance coverage grid. The rows are five requirements Contrl extracted from the RFP, each with its section reference. The columns are three candidate projects chosen by your team. Orange dots mark which requirements each project covers; the transition requirement has no dot and is flagged as a gap to close with a teammate\'s project or an explained approach',
        head='Who covers what: the rows come from the RFP, the checks from your record',
        rows_h='Rows · in Contrl', rows_sub='Requirements extracted from the RFP',
        cols_h='Columns · your team', cols_sub='Candidate projects',
        tag='SOW',
        reqs=['24/7 service desk', 'Ticketing system maintenance', 'Field support at stations',
              'Monthly service-level reports', 'Transition from the incumbent'],
        projs=['Project B', 'Project C', 'Project D'],
        gap='Gap', gapnote='Add a teammate\'s project\nor explain the approach',
        foot='Contrl doesn\'t choose your projects. It makes sure you check them against the whole scope.'),
    'ko': dict(
        title='수행 실적 커버리지 표. 행은 Contrl이 제안요청서에서 추출한 요구사항 다섯 개로, 각각 출처 조항이 붙어 있다. 열은 팀이 고른 후보 사업 세 개다. 주황색 점은 각 사업이 어떤 요구사항을 다루는지 표시하고, 수행사 전환 요구사항에는 점이 없어 컨소시엄 파트너의 실적이나 수행 방안 설명으로 메워야 할 공백으로 표시된다',
        head='무엇을 누가 증명하나: 행은 제안요청서에서, 체크는 우리 실적에서',
        rows_h='행 · Contrl에서', rows_sub='제안요청서에서 추출한 요구사항',
        cols_h='열 · 우리 팀', cols_sub='후보 사업',
        tag='과업',
        reqs=['24시간 서비스 데스크', '발권 시스템 유지보수', '역사 현장 지원',
              '월간 서비스 수준 보고', '기존 수행사로부터 전환'],
        projs=['사업 B', '사업 C', '사업 D'],
        gap='공백', gapnote='파트너사 실적을 더하거나\n수행 방안을 설명',
        foot='Contrl이 사업을 골라 주지는 않습니다. 대신 과업 범위 전체에 비춰 확인하게 해 줍니다.'),
    'ja': dict(
        title='過去実績のカバレッジ表。行はContrlがRFPから抽出した五つの要件で、それぞれ出典の条項番号が付いている。列はチームが選んだ三つの候補案件。オレンジの点は各案件がどの要件をカバーするかを示し、現行業者からの移行の要件には点がなく、協力会社の実績か説明した実施方法で埋めるべき空白として示されている',
        head='どの実績が何を証明するか：行はRFPから、チェックは自社の記録から',
        rows_h='行 · Contrlで', rows_sub='RFPから抽出した要件',
        cols_h='列 · 自社チーム', cols_sub='候補案件',
        tag='SOW',
        reqs=['24時間サービスデスク', '発券システムの保守', '駅での現地サポート',
              '月次のサービスレベル報告', '現行業者からの移行'],
        projs=['案件B', '案件C', '案件D'],
        gap='空白', gapnote='協力会社の実績を加えるか\n実施方法を説明する',
        foot='Contrlが案件を選ぶわけではありません。作業範囲の全体に照らして確認できるようにします。'),
    'zh': dict(
        title='过往业绩覆盖表。行是Contrl从招标文件中提取的五项需求，每项都标有出处条款。列是团队选出的三个候选项目。橙色圆点标出每个项目覆盖了哪些需求；从现有承包商过渡这一需求没有圆点，被标为需要用合作伙伴业绩或说明实施方法来填补的空白',
        head='谁来证明什么：行来自招标文件，勾选来自你的业绩',
        rows_h='行 · 在Contrl中', rows_sub='从招标文件提取的需求',
        cols_h='列 · 你的团队', cols_sub='候选项目',
        tag='SOW',
        reqs=['7×24小时服务台', '票务系统维护', '车站现场支持',
              '月度服务水平报告', '从现有承包商过渡'],
        projs=['项目B', '项目C', '项目D'],
        gap='空白', gapnote='补充合作伙伴业绩\n或说明实施方法',
        foot='Contrl不替你挑选项目，而是让你对照完整的工作范围去核对。'),
}

PX0, PX1 = 30, 600                 # Contrl panel (rows)
COLS = [700, 820, 940]             # project column centers
GX = 1010                          # gap note x
Y0, RH = 212, 62                   # first row top, row height


def diagram(lang):
    t = T[lang]
    s = Svg(lang, H)
    s.text(40, 50, t['head'], fs=22, weight=800, maxw=1120)

    # Contrl panel holding the rows
    s.rect(PX0, 86, PX1 - PX0, Y0 - 86 + RH * 5 + 20, CREAM, ACCENT, r=16, sw=2)
    s.pill(PX0 + 20, 102, t['rows_h'], fs=15)
    s.text(PX0 + 20, 166, t['rows_sub'], fs=15, weight=600, fill=MUTED)

    # columns header
    s.text(COLS[0] - 50, 116, t['cols_h'], fs=17, weight=800)
    s.text(COLS[0] - 50, 144, t['cols_sub'], fs=15, weight=600, fill=MUTED)

    for i, (req, cov) in enumerate(zip(t['reqs'], COVER)):
        y = Y0 + i * RH
        gap = not any(cov)
        # requirement card
        s.rect(PX0 + 20, y + 6, PX1 - PX0 - 40, RH - 12, '#fff', ACCENT if gap else LINE, r=10,
               sw=2 if gap else 1.5, dash='6 5' if gap else None)
        s.text(PX0 + 38, y + RH / 2 + 5, f"{t['tag']} 3.{i + 1}", fs=14, weight=800, fill=ACCENT_INK)
        s.text(PX0 + 38 + tw(f"{t['tag']} 3.{i + 1}", 14) + 22, y + RH / 2 + 6, req, fs=17, weight=600)
        # row guide across the grid
        s.out.append(f'<line x1="{PX1 + 10}" y1="{y + RH / 2}" x2="{COLS[-1] + 40}" y2="{y + RH / 2}" '
                     f'stroke="{ACCENT if gap else LINE}" stroke-width="1.5" stroke-dasharray="{"6 5" if gap else "0"}"/>')
        for x, c in zip(COLS, cov):
            if c:
                s.out.append(f'<circle cx="{x}" cy="{y + RH / 2}" r="13" fill="{ACCENT}"/>')
                s.out.append(f'<path d="M{x - 6} {y + RH / 2}l4 4.5l8-9" fill="none" stroke="#fff" stroke-width="3" '
                             f'stroke-linecap="round" stroke-linejoin="round"/>')
            else:
                s.out.append(f'<circle cx="{x}" cy="{y + RH / 2}" r="12" fill="#fff" stroke="{GRAY_TXT}" '
                             f'stroke-width="1.5" stroke-dasharray="3 3"/>')
        if gap:
            s.pill(GX, y + RH / 2 - 15, t['gap'], fs=14)
            s.text(GX, y + RH / 2 + 38, t['gapnote'], fs=14, weight=600, fill=ACCENT_INK, lh=1.35)

    # project headers (drawn last so they sit above the guides)
    for x, p in zip(COLS, t['projs']):
        w = max(96, tw(p, 15) + 24)
        s.rect(x - w / 2, 160, w, 30, GRAY_BOX, GRAY_TXT, r=8, sw=1.2)
        s.text(x, 180, p, fs=15, weight=700, anchor='middle')

    s.text(40, 576, t['foot'], fs=17, fill=MUTED, maxw=1120, lh=1.45)
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in T:
        fn = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fn), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print('wrote', fn)
