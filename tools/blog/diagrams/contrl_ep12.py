#!/usr/bin/env python3
"""EP12 (Compliance Matrix) concept diagram for the "Where Contrl fits" section.

Run:  python3 tools/blog/diagrams/contrl_ep12.py
Writes images/blog/compliance-matrix/contrl-requirement-map.svg (en) and .<lang>.svg (ko/ja/zh).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from contrl_diagrams import Svg, tw, ROOT, W, INK, MUTED, LINE, CREAM, PEACH, ACCENT, ACCENT_INK, GRAY_BOX, GRAY_TXT  # noqa: E402,F401

SLUG, NAME = 'compliance-matrix', 'contrl-requirement-map'

T = {
    'en': dict(
        title='Contrl splits the uploaded RFP into requirements, maps each one to a section of the required outline, and each page cites the requirements it answers, with a check that none is left unmapped',
        rfp='RFP', rfp_sub='Uploaded',
        zone='In Contrl',
        h_req='Requirements', h_sec='Required outline', h_page='Pages',
        reqs=['Describe the transition plan', 'Identify key staff', 'Report SLAs monthly',
              'Run a 24/7 service desk', 'Keep data in-country'],
        hidden='in narrative',
        secs=['1. Transition\napproach', '2. Project team', '3. Service\noperations'],
        pages=['Transition plan', 'Key staff', 'Service desk'],
        answers='Answers',
        check='5 of 5 requirements mapped · 0 unmapped',
        foot='Every requirement lands in a section, and every page says which ones it answers.'),
    'ko': dict(
        title='Contrl은 업로드한 제안요청서를 요구사항으로 나누어 제안서 목차의 각 섹션에 연결하고, 각 페이지는 대응하는 요구사항을 밝히며, 연결되지 않은 요구사항이 없는지 확인한다',
        rfp='제안요청서', rfp_sub='업로드',
        zone='Contrl에서',
        h_req='요구사항', h_sec='제안서 목차', h_page='페이지',
        reqs=['전환 계획 설명', '핵심 인력 명시', '월간 SLA 보고',
              '24시간 서비스 데스크 운영', '데이터 국내 보관'],
        hidden='본문 속 요구사항',
        secs=['1. 전환 방안', '2. 수행 조직', '3. 서비스 운영'],
        pages=['전환 계획', '핵심 인력', '서비스 데스크'],
        answers='대응',
        check='요구사항 5개 중 5개 연결 · 미연결 0',
        foot='모든 요구사항이 섹션에 자리 잡고, 모든 페이지가 어떤 요구사항에 답하는지 밝힙니다.'),
    'ja': dict(
        title='ContrlはアップロードしたRFPを要求事項に分け、指定された提案書目次の各セクションに対応づけ、各ページが答える要求事項を示し、対応先のない要求事項がないことを確認する',
        rfp='RFP', rfp_sub='アップロード',
        zone='Contrlで',
        h_req='要求事項', h_sec='指定の目次', h_page='ページ',
        reqs=['移行計画を説明', '主要要員を明示', 'SLAを毎月報告',
              '24時間サービスデスク', 'データを国内で保管'],
        hidden='本文中の要件',
        secs=['1. 移行方針', '2. 実施体制', '3. サービス運用'],
        pages=['移行計画', '主要要員', 'サービスデスク'],
        answers='対応',
        check='要求事項5件中5件を対応づけ · 未対応0件',
        foot='すべての要求事項がセクションに収まり、すべてのページがどの要求に答えるかを示します。'),
    'zh': dict(
        title='Contrl 把上传的招标文件拆成需求，逐条对应到规定提纲的章节，每页注明它回应的需求，并检查没有遗漏未对应的需求',
        rfp='招标文件', rfp_sub='已上传',
        zone='在 Contrl 中',
        h_req='需求', h_sec='规定的提纲', h_page='页面',
        reqs=['说明过渡计划', '明确关键人员', '每月报告SLA',
              '运行24小时服务台', '数据境内存储'],
        hidden='正文中的需求',
        secs=['1. 过渡方案', '2. 项目团队', '3. 服务运营'],
        pages=['过渡计划', '关键人员', '服务台'],
        answers='回应',
        check='5条需求全部对应 · 未对应 0',
        foot='每条需求都落到一个章节，每一页都注明它回应哪些需求。'),
}

# requirement index -> section index
MAP = [0, 1, 2, 2, 0]
CITES = [['R-01', 'R-05'], ['R-02'], ['R-03', 'R-04']]


def diagram(lang):
    t = T[lang]
    s = Svg(lang, 600)

    # RFP document (outside Contrl)
    s.rect(30, 150, 130, 220, CREAM, LINE, r=12)
    s.text(95, 190, t['rfp'], fs=20 if lang == 'en' else 17, weight=700, anchor='middle')
    for i in range(7):
        y = 214 + i * 20
        color = ACCENT if i in (1, 4) else LINE
        s.rect(50, y, 90 if i % 3 else 70, 6, color, r=3)
    s.text(95, 394, t['rfp_sub'], fs=15, fill=MUTED, anchor='middle')
    s.arrow(162, 260, 206, 260)

    # Contrl zone
    s.rect(212, 40, 962, 492, PEACH, ACCENT, r=22, sw=2)
    s.pill(236, 56, t['zone'], fs=15, fill=ACCENT)

    xr, wr = 236, 380
    xs, ws = 680, 200
    xp, wp = 948, 206
    s.text(xr, 128, t['h_req'], fs=17, weight=700, fill=MUTED)
    s.text(xs, 128, t['h_sec'], fs=17, weight=700, fill=MUTED)
    s.text(xp, 128, t['h_page'], fs=17, weight=700, fill=MUTED)

    # requirement rows
    row_c = []
    for i, req in enumerate(t['reqs']):
        y = 146 + i * 62
        hidden = i == 4
        s.rect(xr, y, wr, 50, '#fff', ACCENT if hidden else LINE, r=10, sw=2 if hidden else 1.5)
        s.text(xr + 16, y + 31, f'R-0{i + 1}', fs=14, weight=700, fill=ACCENT_INK)
        s.text(xr + 70, y + 31, req, fs=17, weight=600)
        if hidden:
            pw = tw(t['hidden'], 12) + 20
            s.rect(xr + wr - pw - 12, y + 13, pw, 24, CREAM, r=12)
            s.text(xr + wr - pw / 2 - 12, y + 30, t['hidden'], fs=12, weight=700, fill=ACCENT_INK, anchor='middle')
        row_c.append(y + 25)

    # sections and pages
    sec_c = []
    for j, sec in enumerate(t['secs']):
        y = 146 + j * 100
        s.rect(xs, y, ws, 80, '#fff', LINE, r=12)
        nlines = len(sec.split('\n'))
        s.text(xs + 18, y + 40 - (nlines - 1) * 11 + 6, sec, fs=17, weight=700, lh=1.3)
        sec_c.append(y + 40)
        # page card
        s.rect(xp, y, wp, 80, '#fff', LINE, r=10)
        s.rect(xp, y, 6, 80, ACCENT, r=3)
        s.text(xp + 20, y + 26, t['pages'][j], fs=15, weight=700)
        s.rect(xp + 20, y + 36, 120, 5, LINE, r=2.5)
        label = f"{t['answers']} {' · '.join(CITES[j])}"
        s.pill(xp + 20, y + 47, label, fs=12, fill=INK)
        s.arrow(xs + ws + 2, y + 40, xp - 4, y + 40)

    # requirement -> section links
    for i, j in enumerate(MAP):
        x1, y1 = xr + wr + 2, row_c[i]
        x2, y2 = xs - 4, sec_c[j] + (i - 2) * 4
        s.path(f'M{x1} {y1} C{x1 + 36} {y1} {x2 - 36} {y2} {x2} {y2}', sw=2.5)

    # coverage check
    s.rect(xr, 462, 918, 50, INK, r=12)
    s.out.append(f'<circle cx="{xr + 30}" cy="487" r="13" fill="{ACCENT}"/>')
    s.out.append(f'<path d="M{xr + 23} 487 l5 5 l9 -10" fill="none" stroke="#fff" stroke-width="3" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
    s.text(xr + 56, 493, t['check'], fs=18, weight=700, fill='#fff')

    s.text(W / 2, 572, t['foot'], fs=18, fill=MUTED, anchor='middle')
    return s.render(t['title'])


if __name__ == '__main__':
    d = os.path.join(ROOT, 'images', 'blog', SLUG)
    os.makedirs(d, exist_ok=True)
    for lang in T:
        fname = f'{NAME}.svg' if lang == 'en' else f'{NAME}.{lang}.svg'
        with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
            f.write(diagram(lang))
        print(os.path.join('images', 'blog', SLUG, fname))
