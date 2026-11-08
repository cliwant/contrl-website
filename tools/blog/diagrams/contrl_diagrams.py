#!/usr/bin/env python3
"""Concept diagrams for the blog's "Where Contrl fits" sections, one SVG per language.

Run:  python3 tools/blog/diagrams/contrl_diagrams.py
Writes images/blog/<slug>/contrl-<name>.<lang>.svg (en has no lang suffix).
Pure stdlib. Text is wrapped with a rough width estimate; check the output in a browser.
"""
import os
import unicodedata
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
LANGS = ['en', 'ko', 'ja', 'zh']
W = 1200

INK, MUTED, LINE = '#18181b', '#71717a', '#e2d6c9'
CREAM, PEACH = '#f9f6f2', '#fffaf6'
ACCENT, ACCENT_INK = '#F27A2E', '#b7551b'
GRAY_BOX, GRAY_TXT = '#f4f4f5', '#a1a1aa'
FONT = {
    'en': "'Pretendard', -apple-system, 'Helvetica Neue', Arial, sans-serif",
    'ko': "'Pretendard', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif",
    'ja': "'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', 'Yu Gothic', Meiryo, sans-serif",
    'zh': "'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', sans-serif",
}


def cw(ch, fs):
    if unicodedata.east_asian_width(ch) in ('W', 'F'):
        return fs
    if ch == ' ':
        return fs * 0.3
    if ch.isupper() or ch in 'mwMW':
        return fs * 0.74
    if ch in 'il.,:;\'’|!':
        return fs * 0.3
    return fs * 0.6


def tw(s, fs):
    return sum(cw(c, fs) for c in s)


def wrap(s, fs, maxw, lang):
    lines = []
    for para in s.split('\n'):
        tokens = para.split(' ') if lang in ('en', 'ko') else list(para)
        sep = ' ' if lang in ('en', 'ko') else ''
        cur = ''
        for t in tokens:
            cand = (cur + sep + t) if cur else t
            if tw(cand, fs) <= maxw or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = t
        lines.append(cur)
    return lines


class Svg:
    def __init__(self, lang, h):
        self.lang, self.h, self.out = lang, h, []

    def rect(self, x, y, w, h, fill, stroke=None, r=16, sw=1.5, dash=None):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{d}/>')

    def text(self, x, y, s, fs=20, fill=INK, weight=400, anchor='start', maxw=None, lh=1.4):
        """Draw (wrapped) text with its first baseline at y; return the y below the block."""
        lines = wrap(s, fs, maxw, self.lang) if maxw else s.split('\n')
        for i, ln in enumerate(lines):
            self.out.append(
                f'<text x="{x}" y="{y + i * fs * lh:.1f}" font-size="{fs}" font-weight="{weight}" '
                f'fill="{fill}" text-anchor="{anchor}">{escape(ln)}</text>')
        return y + len(lines) * fs * lh

    def block_h(self, s, fs, maxw, lh=1.4):
        return len(wrap(s, fs, maxw, self.lang)) * fs * lh

    def arrow(self, x1, y1, x2, y2, color=ACCENT, sw=3):
        self.out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                        f'stroke-width="{sw}" marker-end="url(#ah-{color[1:]})"/>')

    def path(self, d, color=ACCENT, sw=3):
        self.out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
                        f'marker-end="url(#ah-{color[1:]})"/>')

    def pill(self, x, y, s, fs=15, fill=ACCENT, color='#fff'):
        w = tw(s, fs) + 28
        self.rect(x, y, w, fs + 16, fill, r=(fs + 16) / 2)
        self.text(x + 14, y + fs + 3, s, fs=fs, fill=color, weight=700)
        return w

    def render(self, title):
        markers = ''.join(
            f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
            for c in (ACCENT, GRAY_TXT))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.h}" width="{W}" '
                f'height="{self.h}" role="img" aria-label="{escape(title)}" '
                f'font-family="{FONT[self.lang]}"><title>{escape(title)}</title>'
                f'<defs>{markers}</defs><rect width="{W}" height="{self.h}" fill="#fff"/>'
                + ''.join(self.out) + '</svg>\n')


# ---------------------------------------------------------------- EP02 · CRM
CRM = {
    'en': dict(
        title='Before the RFP, your team learns what the customer worries about; after it, Contrl turns those notes into the win theme',
        left='Before the RFP · your team', right='After the RFP · in Contrl',
        notes=[('Meeting · IT director', '“Downtime on the night shift is what I really fear.”'),
               ('Site visit', '“Staff key the same data in twice.”'),
               ('Call · program office', '“The last vendor missed go-live.”')],
        rfp='RFP released', interview='Strategy interview', interview_sub='You bring the meeting notes into the chat',
        theme='Win theme', rows=[('Client need', 'Zero night-shift downtime'), ('Our edge', 'Proven staged cutover'), ('Benefit', 'Operations never stop')],
        foot='A theme built on what the customer told you, not on what the RFP says.'),
    'ko': dict(
        title='제안요청서 전에는 팀이 고객의 걱정을 알아내고, 제안요청서가 나오면 Contrl이 그 기록을 윈 테마로 만든다',
        left='제안요청서 전 · 우리 팀', right='제안요청서 후 · Contrl에서',
        notes=[('미팅 · 정보화 부서장', '“진짜 걱정은 야간 근무 중 장애예요.”'),
               ('현장 방문', '“직원들이 같은 데이터를 두 번 입력해요.”'),
               ('통화 · 사업 담당', '“지난 업체는 오픈 일정을 못 지켰어요.”')],
        rfp='제안요청서 공고', interview='전략 인터뷰', interview_sub='미팅 기록을 채팅에 그대로 가져옵니다',
        theme='윈 테마', rows=[('고객 니즈', '야간 장애 제로'), ('우리의 강점', '검증된 단계적 전환'), ('효과', '운영이 멈추지 않음')],
        foot='제안요청서 문구가 아니라 고객에게 직접 들은 것으로 만든 테마.'),
    'ja': dict(
        title='RFPの前にチームが顧客の懸念を知り、RFPが出たらContrlがその記録をウィンテーマにする',
        left='RFPの前 · 自社チーム', right='RFPの後 · Contrlで',
        notes=[('面談 · 情報システム部長', '「本当に怖いのは夜間の障害です」'),
               ('現場訪問', '「職員が同じデータを二度入力している」'),
               ('電話 · 事業担当', '「前の業者は稼働日に間に合わなかった」')],
        rfp='RFP公示', interview='戦略インタビュー', interview_sub='面談記録をそのままチャットに持ち込む',
        theme='ウィンテーマ', rows=[('顧客ニーズ', '夜間障害ゼロ'), ('自社の強み', '実績ある段階的移行'), ('効果', '業務が止まらない')],
        foot='RFPの文言ではなく、顧客から直接聞いたことで作るテーマ。'),
    'zh': dict(
        title='招标前团队了解客户的担忧；招标后 Contrl 把这些记录变成制胜主题',
        left='招标前 · 我方团队', right='招标后 · 在 Contrl 中',
        notes=[('会面 · 信息化负责人', '“我真正担心的是夜班期间宕机。”'),
               ('现场走访', '“员工要把同样的数据录两遍。”'),
               ('电话 · 项目办公室', '“上一家供应商没能按时上线。”')],
        rfp='发布招标文件', interview='策略访谈', interview_sub='把会面记录直接带进对话',
        theme='制胜主题', rows=[('客户需求', '夜班零宕机'), ('我方优势', '经过验证的分阶段切换'), ('收益', '业务不中断')],
        foot='主题来自客户亲口说的话，而不是招标文件的措辞。'),
}


def crm(lang):
    t = CRM[lang]
    s = Svg(lang, 560)
    # zones
    s.rect(30, 30, 520, 470, CREAM, LINE)
    s.rect(650, 30, 520, 470, PEACH, ACCENT, sw=2)
    s.text(60, 72, t['left'], fs=20, weight=700, fill=MUTED)
    s.text(680, 72, t['right'], fs=20, weight=700, fill=ACCENT_INK)
    # notes
    y = 100
    for i, (who, quote) in enumerate(t['notes']):
        s.rect(60, y, 460, 112, '#fff', LINE, r=12)
        s.rect(60, y, 8, 112, ACCENT, r=4)
        s.text(88, y + 34, who, fs=16, weight=700, fill=ACCENT_INK)
        s.text(88, y + 66, quote, fs=19, maxw=410, lh=1.35)
        y += 128
    # RFP divider
    s.out.append(f'<line x1="600" y1="40" x2="600" y2="490" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 6"/>')
    pw = tw(t['rfp'], 15) + 28
    s.pill(600 - pw / 2, 250, t['rfp'], fs=15, fill=INK)
    # arrows into interview
    s.arrow(552, 154, 676, 154)
    # interview box
    s.rect(680, 100, 460, 108, '#fff', LINE, r=12)
    s.text(704, 140, t['interview'], fs=22, weight=700)
    s.text(704, 176, t['interview_sub'], fs=17, fill=MUTED, maxw=420)
    s.arrow(910, 212, 910, 248)
    # win theme
    s.rect(680, 252, 460, 218, '#fff', ACCENT, r=12, sw=2)
    s.text(704, 290, t['theme'], fs=22, weight=700, fill=ACCENT_INK)
    yy = 336
    for k, v in t['rows']:
        s.text(704, yy, k, fs=17, fill=MUTED, weight=600)
        s.text(860, yy, v, fs=18, weight=600, maxw=270)
        yy += 48
    s.text(W / 2, 536, t['foot'], fs=18, fill=MUTED, anchor='middle')
    return s.render(t['title'])


# ---------------------------------------------------- EP03 · capture strategy
CAP = {
    'en': dict(
        title='The proposal strategy is a subset of the capture strategy; in Contrl it becomes one win theme that every section inherits',
        when_l='Months before the RFP · your team', when_r='Once the RFP is out · Contrl',
        capture='Capture strategy', items=['Hot buttons', 'Bidder comparison (BCM)', 'Teaming & pricing position', 'Relationship plan'],
        proposal='Proposal strategy', proposal_sub='the part you put in writing',
        interview='Strategy interview', theme='One win theme', sec='Section', key='key sentence'),
    'ko': dict(
        title='제안 전략은 캡처 전략의 부분집합이고, Contrl에서는 모든 섹션이 이어받는 하나의 윈 테마가 된다',
        when_l='공고 몇 달 전 · 우리 팀', when_r='제안요청서가 나오면 · Contrl',
        capture='캡처 전략', items=['핫 버튼', '입찰자 비교 매트릭스(BCM)', '컨소시엄·가격 포지션', '관계 계획'],
        proposal='제안 전략', proposal_sub='그중 제안서에 쓰는 부분',
        interview='전략 인터뷰', theme='하나의 윈 테마', sec='섹션', key='핵심 문장'),
    'ja': dict(
        title='提案戦略はキャプチャー戦略の一部であり、Contrlではすべてのセクションが受け継ぐ一つのウィンテーマになる',
        when_l='公示の数か月前 · 自社チーム', when_r='RFPが出たら · Contrl',
        capture='キャプチャー戦略', items=['ホットボタン', '入札者比較マトリクス(BCM)', 'チーミング・価格ポジション', '関係構築計画'],
        proposal='提案戦略', proposal_sub='そのうち提案書に書く部分',
        interview='戦略インタビュー', theme='一つのウィンテーマ', sec='セクション', key='キーセンテンス'),
    'zh': dict(
        title='投标策略是捕获策略的子集；在 Contrl 中它成为每个章节都继承的一个制胜主题',
        when_l='招标前几个月 · 我方团队', when_r='招标文件发布后 · Contrl',
        capture='捕获策略', items=['热点诉求', '投标人比较矩阵（BCM）', '组队与价格定位', '关系计划'],
        proposal='投标策略', proposal_sub='其中写进标书的部分',
        interview='策略访谈', theme='一个制胜主题', sec='章节', key='核心句'),
}


def capture(lang):
    t = CAP[lang]
    s = Svg(lang, 540)
    s.text(40, 52, t['when_l'], fs=18, weight=700, fill=MUTED)
    s.text(640, 52, t['when_r'], fs=18, weight=700, fill=ACCENT_INK)
    # outer capture
    s.rect(40, 76, 520, 420, CREAM, LINE, r=22)
    s.text(70, 120, t['capture'], fs=24, weight=700)
    y = 160
    for it in t['items']:
        s.out.append(f'<circle cx="80" cy="{y - 6}" r="4" fill="{MUTED}"/>')
        s.text(96, y, it, fs=17, fill='#3f3f46')
        y += 32
    # inner proposal strategy
    s.rect(70, 316, 460, 150, PEACH, ACCENT, r=18, sw=2)
    s.text(96, 360, t['proposal'], fs=22, weight=700, fill=ACCENT_INK)
    s.text(96, 394, t['proposal_sub'], fs=17, fill=MUTED, maxw=410)
    # flow
    s.arrow(532, 391, 636, 391)
    s.rect(640, 346, 200, 90, '#fff', LINE, r=14)
    hi = s.block_h(t['interview'], 18, 180)
    s.text(740, 391 - hi / 2 + 18, t['interview'], fs=18, weight=700, anchor='middle', maxw=180)
    s.arrow(842, 391, 880, 391)
    s.rect(884, 330, 286, 122, INK, r=16)
    s.text(1027, 400, t['theme'], fs=22, weight=700, fill='#fff', anchor='middle')
    # fan out to sections
    xs = [884, 1027 - 0, 1170]
    cards = [(640, 96), (820, 96), (1000, 96)]
    for i, (cx, cy) in enumerate(cards):
        s.rect(cx, cy, 170, 112, '#fff', LINE, r=12)
        s.text(cx + 18, cy + 36, f"{t['sec']} {i + 1}", fs=16, weight=700, fill=MUTED)
        s.rect(cx + 18, cy + 52, 134, 40, PEACH, r=8)
        s.text(cx + 85, cy + 78, t['key'], fs=16, weight=600, fill=ACCENT_INK, anchor='middle')
        s.path(f'M1027 328 C1027 270 {cx + 85} 268 {cx + 85} 212')
    return s.render(t['title'])


# --------------------------------------------- EP05 · customer & competitor intel
INTEL = {
    'en': dict(
        title='With only the RFP, a draft could come from any bidder; add your team’s intelligence and the win theme has an edge competitors can’t claim',
        a_tag='RFP only', b_tag='RFP + your team’s intelligence',
        rfp='RFP', rfp_sub='Requirements, scoring',
        intel='Your team knows', intel_items=['What the customer worries about', 'Where each rival is weak', 'Your record with this customer'],
        ai='AI drafting', contrl='Contrl strategy interview',
        out_a='A compliant draft any bidder could have written', out_b='A win theme with an edge competitors can’t claim'),
    'ko': dict(
        title='제안요청서만 넣으면 누구나 쓸 수 있는 초안이 나오고, 팀의 인텔리전스를 더하면 경쟁사가 말할 수 없는 강점을 담은 윈 테마가 나온다',
        a_tag='제안요청서만', b_tag='제안요청서 + 우리 팀의 인텔리전스',
        rfp='제안요청서', rfp_sub='요구사항, 평가 기준',
        intel='우리 팀만 아는 것', intel_items=['고객이 걱정하는 것', '경쟁사별 약점', '이 고객과의 수행 이력'],
        ai='AI 초안 작성', contrl='Contrl 전략 인터뷰',
        out_a='요구사항은 다 맞췄지만 어느 회사가 써도 같은 초안', out_b='경쟁사는 말할 수 없는 강점을 담은 윈 테마'),
    'ja': dict(
        title='RFPだけでは誰でも書ける草案になり、チームのインテリジェンスを加えると競合が言えない強みを持つウィンテーマになる',
        a_tag='RFPだけ', b_tag='RFP + 自社チームのインテリジェンス',
        rfp='RFP', rfp_sub='要求事項、評価基準',
        intel='自社チームだけが知ること', intel_items=['顧客が懸念していること', '競合ごとの弱点', 'この顧客との実績'],
        ai='AIで草案作成', contrl='Contrl 戦略インタビュー',
        out_a='要件は満たしているが、どの会社が書いても同じ草案', out_b='競合には言えない強みを持つ\nウィンテーマ'),
    'zh': dict(
        title='只给招标文件，得到的是任何投标人都能写出的初稿；加上团队掌握的情报，制胜主题才有竞争对手说不出的优势',
        a_tag='只有招标文件', b_tag='招标文件 + 我方团队的情报',
        rfp='招标文件', rfp_sub='需求、评分标准',
        intel='只有我方团队知道', intel_items=['客户担心什么', '各竞争对手的弱点', '我们与该客户的合作记录'],
        ai='AI 起草', contrl='Contrl 策略访谈',
        out_a='合规，但任何投标人都写得出来的初稿', out_b='带有竞争对手说不出的优势的\n制胜主题'),
}


def intel(lang):
    t = INTEL[lang]
    s = Svg(lang, 600)
    # row A
    s.text(40, 52, t['a_tag'], fs=18, weight=700, fill=MUTED)
    s.rect(40, 70, 300, 100, CREAM, LINE, r=14)
    s.text(64, 112, t['rfp'], fs=22, weight=700)
    s.text(64, 146, t['rfp_sub'], fs=16, fill=MUTED, maxw=260)
    s.arrow(344, 120, 426, 120, color=GRAY_TXT)
    s.rect(430, 80, 270, 80, GRAY_BOX, r=14)
    s.text(565, 128, t['ai'], fs=19, weight=700, fill='#52525b', anchor='middle')
    s.arrow(704, 120, 778, 120, color=GRAY_TXT)
    s.rect(782, 70, 378, 100, GRAY_BOX, r=14, dash='6 6', stroke=GRAY_TXT, sw=1.5)
    h = s.block_h(t['out_a'], 19, 330, 1.35)
    s.text(806, 120 - h / 2 + 19, t['out_a'], fs=19, fill='#52525b', weight=600, maxw=330, lh=1.35)
    # divider
    s.out.append(f'<line x1="40" y1="212" x2="1160" y2="212" stroke="{LINE}" stroke-width="2"/>')
    # row B
    s.text(40, 258, t['b_tag'], fs=18, weight=700, fill=ACCENT_INK)
    s.rect(40, 276, 300, 100, CREAM, LINE, r=14)
    s.text(64, 318, t['rfp'], fs=22, weight=700)
    s.text(64, 352, t['rfp_sub'], fs=16, fill=MUTED, maxw=260)
    items_h = sum(s.block_h(it, 17, 236, 1.3) + 10 for it in t['intel_items'])
    head_h = s.block_h(t['intel'], 20, 260)
    box_h = 30 + head_h + 12 + items_h + 8
    s.rect(40, 392, 300, box_h, PEACH, ACCENT, r=14, sw=2)
    y = s.text(64, 428, t['intel'], fs=20, weight=700, fill=ACCENT_INK, maxw=260) + 12
    for it in t['intel_items']:
        s.out.append(f'<circle cx="70" cy="{y - 6}" r="4" fill="{ACCENT}"/>')
        y = s.text(84, y, it, fs=17, maxw=236, lh=1.3) + 10
    mid = (276 + 392 + box_h) / 2
    s.path(f'M344 326 C392 326 392 {mid - 5} 426 {mid - 5}')
    s.path(f'M344 {392 + box_h / 2} C392 {392 + box_h / 2} 392 {mid + 5} 426 {mid + 5}')
    s.rect(430, mid - 45, 270, 90, '#fff', ACCENT, r=14, sw=2)
    hc = s.block_h(t['contrl'], 19, 240)
    s.text(565, mid - hc / 2 + 19, t['contrl'], fs=19, weight=700, anchor='middle', maxw=240)
    s.arrow(704, mid, 778, mid)
    s.rect(782, mid - 63, 378, 126, INK, r=14)
    h = s.block_h(t['out_b'], 20, 330, 1.35)
    s.text(806, mid - h / 2 + 20, t['out_b'], fs=20, fill='#fff', weight=700, maxw=330, lh=1.35)
    s.h = int(392 + box_h + 32)
    return s.render(t['title'])


JOBS = [
    ('customer-relationship-management', 'contrl-before-rfp', crm),
    ('opportunity-capture-strategy', 'contrl-capture-flow', capture),
    ('customer-and-competitor-intelligence', 'contrl-intel-edge', intel),
]

if __name__ == '__main__':
    for slug, name, fn in JOBS:
        d = os.path.join(ROOT, 'images', 'blog', slug)
        os.makedirs(d, exist_ok=True)
        for lang in LANGS:
            fname = f'{name}.svg' if lang == 'en' else f'{name}.{lang}.svg'
            with open(os.path.join(d, fname), 'w', encoding='utf-8') as f:
                f.write(fn(lang))
            print(os.path.join('images', 'blog', slug, fname))
