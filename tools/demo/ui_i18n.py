import json, re, sys
D = '/private/tmp/claude-501/-Users-junhocho--claude-spares-spare-8yODFO/e96f1cec-610c-4fdf-91cc-406ae9815ecf/scratchpad/demo/'

# ---------------------------------------------------------------- problem.html UI
P = {
 'AI Deck Generator': ('AI 장표 생성기', 'AIスライド生成'),
 '· New deck': ('· 새 문서', '・新規'),
 'Sources': ('자료', 'ソース'),
 'Prompt': ('프롬프트', 'プロンプト'),
 'Drop files here': ('파일을 여기에 끌어다 놓으세요', 'ここにファイルをドロップ'),
 'Release to add 47 files': ('놓으면 파일 47개 추가', '離すと47件を追加'),
 'RFP_case-management-upgrade.hwp': ('RFP_사례관리시스템_기능개선.hwp', 'RFP_ケース管理システム改修.pdf'),
 'company_profile_2026.pdf': ('회사소개서_2026.pdf', '会社案内_2026.pdf'),
 'winning_proposal_2025.pptx': ('낙찰제안서_2025.pptx', '受注提案書_2025.pptx'),
 'evaluation_criteria.docx': ('평가기준.docx', '評価基準.docx'),
 'past_projects_list.xlsx': ('수행실적목록.xlsx', '実績一覧.xlsx'),
 'case_study_welfare_app.pdf': ('사례집_복지앱.pdf', '事例集_福祉アプリ.pdf'),
 'lost_proposal_2024_v3_final.pptx': ('탈락제안서_2024_v3_최종.pptx', '失注提案書_2024_v3_最終.pptx'),
 'security_checklist_11items.docx': ('보안_체크리스트_11항목.docx', 'セキュリティ_チェックリスト_11項目.docx'),
 'org_chart_and_resumes.pdf': ('조직도_및_이력서.pdf', '組織図_経歴書.pdf'),
 'pricing_draft_v7.xlsx': ('가격_초안_v7.xlsx', '見積_ドラフト_v7.xlsx'),
 'company_intro_long.pptx': ('회사소개_긴버전.pptx', '会社紹介_ロング版.pptx'),
 'reference_letters_2023-2026.pdf': ('추천서_2023-2026.pdf', '推薦状_2023-2026.pdf'),
 'meeting_notes_kickoff.docx': ('회의록_킥오프.docx', '議事録_キックオフ.docx'),
 '+ 42 more files · 312 MB': ('+ 42개 더 · 312 MB', '+ 他42件 · 312 MB'),
 'Describe the deck you want…': ('만들고 싶은 장표를 설명하세요…', '作りたいスライドを説明…'),
 '100 slides': ('100장', '100ページ'),
 'Professional': ('프로페셔널', 'プロ仕様'),
 'Auto images': ('이미지 자동', '画像を自動挿入'),
 '✦ Generate deck': ('✦ 장표 생성', '✦ スライド生成'),
 'Untitled deck': ('제목 없는 문서', '無題のスライド'),
 'Generating…': ('생성 중…', '生成中…'),
 '✓ Done · 100 slides': ('✓ 완료 · 100장', '✓ 完了・100ページ'),
 'Your deck will appear here': ('여기에 장표가 표시됩니다', 'ここにスライドが表示されます'),
 'Proposal_materials': ('제안자료_전체', '提案資料_全部'),
 'Favorites': ('즐겨찾기', 'よく使う項目'),
 'Recents': ('최근 항목', '最近の項目'),
 'Desktop': ('데스크탑', 'デスクトップ'),
 'Downloads': ('다운로드', 'ダウンロード'),
 'Shared': ('공유', '共有'),
 'Bids 2025': ('입찰 2025', '入札 2025'),
 'Templates': ('템플릿', 'テンプレート'),
 '47 items, 312 MB': ('47개 항목, 312MB', '47項目、312 MB'),
 '47 of 47 selected, 312 MB': ('47개 항목 중 47개 선택됨, 312MB', '47項目中47項目を選択、312 MB'),
 'Today, 9:12 AM': ('오늘 오전 9:12', '今日 9:12'), 'Today, 9:14 AM': ('오늘 오전 9:14', '今日 9:14'), 'Today, 9:20 AM': ('오늘 오전 9:20', '今日 9:20'),
 'Oct 2, 2026': ('2026. 10. 2.', '2026/10/02'), 'Dec 11, 2025': ('2025. 12. 11.', '2025/12/11'), 'Sep 18, 2026': ('2026. 9. 18.', '2026/09/18'),
 'Aug 30, 2026': ('2026. 8. 30.', '2026/08/30'), 'Mar 5, 2025': ('2025. 3. 5.', '2025/03/05'), 'Jul 22, 2026': ('2026. 7. 22.', '2026/07/22'),
 'Yesterday': ('어제', '昨日'), 'Jun 3, 2026': ('2026. 6. 3.', '2026/06/03'), 'May 14, 2026': ('2026. 5. 14.', '2026/05/14'), 'Oct 20, 2026': ('2026. 10. 20.', '2026/10/20'),
 '47 items': ('47개 항목', '47項目'),
 # slide 12
 'Section 3 · Technical approach': ('3장 · 기술 접근 방안', '第3章・技術的アプローチ'),
 'Comprehensive Approach to System Enhancement and Stakeholder Value': ('시스템 고도화 및 이해관계자 가치 창출을 위한 종합적 접근 방안', 'システム高度化とステークホルダー価値創出に向けた包括的アプローチ'),
 'Our methodology': ('수행 방법론', '当社の方法論'),
 'Leverage cross-functional synergies to deliver a robust, scalable and future-proof solution': ('부서 간 시너지를 활용하여 견고하고 확장 가능한 미래지향적 솔루션 제공', '部門横断のシナジーを活用し、堅牢で拡張性の高い将来対応型ソリューションを提供'),
 'Apply industry best practices and a systematic management framework': ('업계 모범 사례와 체계적인 관리 프레임워크 적용', '業界のベストプラクティスと体系的な管理フレームワークを適用'),
 'Ensure seamless integration across all stakeholder groups': ('모든 이해관계자 그룹 간 원활한 통합 보장', 'すべてのステークホルダー間のシームレスな統合を確保'),
 'Key differentiators': ('핵심 차별점', '主な差別化要素'),
 'Extensive experience in public-sector digital transformation': ('공공부문 디지털 전환에 대한 풍부한 경험', '公共分野のDXにおける豊富な経験'),
 'Commitment to excellence — we will do our utmost to ensure success': ('사업 성공을 위해 최선을 다하겠습니다', '成功に向けて最善を尽くします'),
 'Expected outcomes': ('기대 효과', '期待される成果'),
 'efficiency gain': ('효율 향상', '効率向上'), 'availability': ('가용성', '可用性'), 'weeks to launch': ('주 내 오픈', '週で稼働'),
 'Also covered on this slide': ('이 장에서 함께 다루는 내용', 'このページで扱う内容'),
 'Security & compliance': ('보안 및 컴플라이언스', 'セキュリティとコンプライアンス'),
 'Change management': ('변화 관리', '変更管理'),
 'Training & adoption': ('교육 및 정착', '研修と定着'),
 'Long-term roadmap': ('중장기 로드맵', '中長期ロードマップ'),
 'Off the point': ('논점 이탈', '論点ずれ'), 'Generic': ('평이함', 'ありきたり'), 'Scattered': ('산만함', '散漫'),
 'Where did 40% come from?': ('40%는 어디서 나왔죠?', '40%はどこから？'),
 # slack
 'Search Northwind Proposal Team': ('Northwind 제안팀 검색', 'Northwind 提案チームを検索'),
 '4 members': ('멤버 4명', 'メンバー4人'),
 'Thursday, October 30th': ('10월 30일 목요일', '10月30日（木）'),
 'Message #bid-casemgmt-upgrade': ('#bid-casemgmt-upgrade에 메시지 보내기', '#bid-casemgmt-upgrade へメッセージ'),
}
P_DYN = {  # JS-built strings
 '{n} slides': ('{n}장', '{n}ページ'),
}

# ---------------------------------------------------------------- replay.html UI (ko = original 나눔비타민 project text)
R = {
 'Student mental-health case management system · functional upgrade': ('학생 정신건강 사례관리시스템 기능개선', '学生メンタルヘルス事例管理システム機能改修'),
 'KEEPA · 16 provincial education offices · 100 pages': ('교육환경보호원 · 16개 시도교육청 · 100장', 'KEEPA・16都道府県教育庁・100ページ'),
 'Interview': ('인터뷰', 'インタビュー'), 'Storyboard': ('스토리보드', 'ストーリーボード'), 'Deck': ('덱', 'スライド'),
 "What the client wants, that we can prove, and competitors can't say": ('발주처가 원하는데, 우리는 증명할 수 있고, 경쟁사는 못하는 것', '顧客が求め、当社が証明でき、競合が言えないこと'),
 'Which theme do we build the whole proposal on?': ('제안서 전체를 어떤 테마 위에 세울까요?', '提案書全体をどのテーマで組み立てますか？'),
 'Three candidates from the RFP and the strategy interview. Pick one — every section inherits it.': ('RFP와 전략 인터뷰에서 뽑은 후보 3개. 하나를 고르면 모든 섹션이 이어받습니다.', 'RFPと戦略インタビューから3候補。1つ選ぶと全セクションに反映されます。'),
 'Selected': ('선택됨', '選択済み'),
 'THEME 1': ('테마 1', 'テーマ 1'), 'THEME 2': ('테마 2', 'テーマ 2'), 'THEME 3': ('테마 3', 'テーマ 3'),
 'Field pain, shipped fast': ('현장 불편의 빠른 기능화', '現場の不便を素早く機能に'),
 'Zero-downtime, zero-leak upgrade': ('무중단·무유출 안전한 개선', '無停止・無漏洩の安全な改修'),
 'Data-driven program operations': ('데이터 기반 사업 운영 지원', 'データに基づく事業運営支援'),
 'Turn the input burden and permission friction reported by 16 provincial offices into shipped features — the way we run our welfare field apps — delivered repeatedly within the contract.':
   ('16개 시도교육청 현장의 입력 부담과 권한 불편을, 복지 현장 앱에서 사용자 요청을 빠르게 배포로 옮겨 온 방식으로 해소해 계약 기간 안에 반복해서 전달합니다.',
    '16教育庁の現場が抱える入力負担と権限の不便を、福祉現場アプリで培った「要望を素早くリリースへ」の方式で解消し、契約期間内に繰り返し届けます。'),
 'Start from the existing source, change in stages without service interruption or data damage, and fold all 11 security items into the execution plan.':
   ('민감한 학생 정신건강 정보가 쌓인 운영 시스템을 기존 소스 파악부터 시작해 중단·훼손 없이 단계적으로 고치고, 보안 11개 항목을 수행계획에 그대로 녹입니다.',
    '既存ソースの把握から始め、サービス停止やデータ毀損なく段階的に改修し、セキュリティ11項目を実行計画にそのまま組み込みます。'),
 'Bundle the permission, alert, statistics and performance modules we already run into views the client can use as evidence for policy decisions.':
   ('권한·알림·통계·성과관리 모듈을 이미 운영해 온 팀이 사용자 의견과 운영 데이터를 조회·통계 기능으로 묶어, 발주처가 사업 성과를 숫자로 확인하게 합니다.',
    '既に運用している権限・通知・統計・成果管理モジュールを束ね、発注者が政策判断の根拠として使える画面にします。'),
 'Client need': ('고객 니즈', '顧客ニーズ'), 'Our edge': ('우리 강점', '自社の強み'), 'Benefit': ('효익', '効果'),
 'Simpler input, multi-school teachers, member-info edits, SMS without exposure': ('입력 간소화, 복수 학교 담당 교사, 회원정보 수정, 정보 비노출 문자', '入力簡素化、複数校担当教員、会員情報修正、情報非表示SMS'),
 'Field requests → release cycle, proven in 20+ municipalities': ('현장 요청 → 배포 주기, 지자체 20곳 이상 운영', '現場要望→リリース周期、20以上の自治体で実証'),
 'Staff feel the improvement in-contract, not after': ('담당자가 계약 기간 안에 개선을 체감', '担当者が契約期間内に改善を実感'),
 'Sensitive student data, no downtime, NIS security guideline': ('민감 학생정보, 무중단, 국가정보보안지침', '機微な学生情報、無停止、国家情報セキュリティ指針'),
 'eGovFrame builds; staged change scope': ('전자정부프레임워크 구축, 단계적 변경 범위', '電子政府フレームワーク構築、段階的な変更範囲'),
 'The client can hand it over with confidence': ('발주처가 안심하고 맡길 수 있음', '発注者が安心して任せられる'),
 'Program results as numbers for policy': ('사업 성과를 정책 근거 숫자로', '事業成果を政策根拠の数値に'),
 'Modules in production with user feedback': ('사용자 피드백이 쌓인 운영 중 모듈', 'ユーザーの声が蓄積された稼働中モジュール'),
 'Performance visible without manual reporting': ('수작업 보고 없이 성과 가시화', '手作業の報告なしで成果を可視化'),
 'III-1 Functional improvement requirements': ('III-1 기능개선수행 요구사항', 'III-1 機能改善要件'),
 '17 pages': ('17장', '17ページ'),
 '12 requirements · FR-001 – COR-006': ('요구사항 12개 · FR-001 – COR-006', '要件12件・FR-001 – COR-006'),
 'Win Theme · Field pain, shipped fast': ('Win Theme · 현장 불편의 빠른 기능화', 'Win Theme・現場の不便を素早く機能に'),
 'Turn the input burden and permission friction reported by 16 provincial offices into shipped features, delivered repeatedly within the contract.':
   ('16개 시도교육청 현장의 입력 부담과 권한 불편을 빠른 배포로 해소해, 계약 기간 안에 반복해서 전달합니다.', '16教育庁の入力負担と権限の不便を素早いリリースで解消し、契約期間内に繰り返し届けます。'),
 'Key sentence': ('핵심 문장', '核心文'), 'Not decided yet': ('아직 미정', '未決定'), '✓ Confirmed': ('✓ 확정', '✓ 確定'),
 'One sentence this section must land': ('이 섹션이 남겨야 할 한 문장', 'この章が伝えるべき一文'),
 'Three angles reduced from the Win Theme. Choose one, or write your own.': ('Win Theme에서 뽑은 세 가지 각도. 하나를 고르거나 직접 쓰세요.', 'Win Themeから導いた3つの切り口。選ぶか、自分で書くか。'),
 'CANDIDATE 1': ('후보 1', '候補 1'), 'CANDIDATE 2': ('후보 2', '候補 2'), 'CANDIDATE 3': ('후보 3', '候補 3'),
 'Lead with real-time monitoring': ('실시간 현황 모니터링을 앞세움', 'リアルタイム状況モニタリングを前面に'),
 'Lead with the institution-tier platform structure': ('기관 단위 계층 플랫폼 구조를 앞세움', '機関単位の階層プラットフォーム構造を前面に'),
 'Lead with common data infrastructure': ('공통 데이터 형식 인프라를 앞세움', '共通データ形式のインフラを前面に'),
 'Improve features through a live status dashboard': ('실시간 현황 화면으로 기능을 개선합니다', 'リアルタイム状況画面で機能を改善する'),
 'Role-based permissions connect student support': ('역할별 권한 체계로 학생지원을 연계합니다', '役割別の権限体系で学生支援をつなぐ'),
 'Same-format data links lookup and referral': ('같은 형식의 데이터로 조회와 연계를 잇습니다', '同じ形式のデータで照会と連携をつなぐ'),
 'Apply the usage-monitoring and regional-distribution screens we already operate, so office staff read program status at a glance and decide immediately.':
   ('사용 현황 모니터링과 지역 분포 리포트를 운영해 온 화면 구성을 적용해, 현황을 한눈에 읽는 형태로 교육청 담당자가 사업 운영 판단을 바로 내리게 합니다.',
    '運用中の利用状況モニタリングと地域分布レポートの画面構成を適用し、教育庁の担当者が状況を一目で読み取り、すぐ判断できるようにします。'),
 'Apply a 3-tier platform structure with a separate institution layer, so referral, counseling and admin roles each see a distinct scope — and a teacher covering several schools links student support in one place.':
   ('기관 운영 계층을 따로 둔 3층 플랫폼 구조를 적용해, 의뢰·상담·관리 역할마다 볼 수 있는 범위가 갈리는 체계로 복수 담당학교를 맡은 교사가 학생 지원 정보를 한곳에서 잇게 합니다.',
    '機関運営の階層を分けた3層プラットフォーム構造を適用し、依頼・相談・管理の役割ごとに閲覧範囲が分かれる体系で、複数校を担当する教員が学生支援情報を一か所でつなげます。'),
 'Store every program\'s data in one common format, so existing cases and screenings carry over without re-entry across the two systems.':
   ('모든 사업의 데이터를 같은 형식으로 쌓는 공통 인프라 방식을 적용해, 기존 사례와 검사 자료가 끊기지 않고 이어져 담당자가 두 시스템의 정보를 다시 입력하지 않게 합니다.',
    'すべての事業データを同じ形式で蓄積する共通インフラ方式を適用し、既存の事例と検査データが途切れずつながり、担当者が2つのシステムに再入力しなくて済むようにします。'),
 'Development': ('전개', '展開'),
 'How do the 17 pages unfold?': ('17장을 어떻게 전개할까요?', '17ページをどう展開しますか？'),
 'Three organizing principles. Each covers all 12 requirements — they differ in what the reader meets first.': ('구성 원칙 세 가지. 요구사항 12개는 모두 다루되, 독자가 먼저 만나는 것이 다릅니다.', '3つの構成原理。12要件はすべて網羅し、読み手が最初に出会うものが違います。'),
 'PLAN A': ('A안', 'A案'), 'PLAN B': ('B안', 'B案'), 'PLAN C': ('C안', 'C案'),
 'In RFP order': ('요구사항 순서대로', '要件の順序どおり'),
 'Around the 3-tier permission structure': ('권한 3층 구조 중심으로', '権限3層構造を中心に'),
 "As one student's journey": ('학생 지원 한 건의 흐름으로', '学生支援1件の流れで'),
 'Follow FR-001 to COR-006 as written; one bundle of screens, rules and deliverables per requirement.': ('RFP가 적은 FR-001부터 COR-006까지 요구사항 순서를 따라, 요구사항마다 구현 화면·규칙·산출물을 한 묶음씩 폅니다.', 'RFPの記載順にFR-001からCOR-006まで、要件ごとに画面・ルール・成果物を一束ずつ展開します。'),
 'Set up the institution / role permission structure first, then layer school workflows and lookup / data features on top.': ('기관과 역할의 권한 구조를 먼저 세우고, 그 위에 학교 현장 업무와 조회·데이터 기능을 얹는 층 순서로 폅니다.', '機関と役割の権限構造を先に立て、その上に学校現場の業務と照会・データ機能を重ねる順で展開します。'),
 'Follow a single case from admin setup through referral, screening, counseling, case management and analysis.': ('관리자의 기관·권한 설정에서 의뢰, 검사, 상담, 사례 운영, 분석까지 학생 지원 한 건이 지나는 순서로 폅니다.', '管理者の機関・権限設定から依頼、検査、相談、事例運営、分析まで、学生支援1件が辿る順で展開します。'),
 'Cases & statistics': ('사례와 통계', '事例と統計'), 'Permissions & search': ('권한과 검색', '権限と検索'), 'Screening & automation': ('검사와 자동화', '検査と自動化'), 'Convenience & standards': ('편의와 수행기준', '利便性と実施基準'),
 'Permission structure': ('권한 구조', '権限構造'), 'School-site workflows': ('학교 현장 업무', '学校現場の業務'), 'Lookup & data': ('조회와 데이터', '照会とデータ'), 'Automation & standards': ('자동화와 수행기준', '自動化と実施基準'),
 'Setup & referral': ('설정과 의뢰', '設定と依頼'), 'Screening & counseling': ('검사와 상담', '検査と相談'), 'Case operations': ('사례 운영', '事例運営'), 'Analysis & standards': ('분석과 수행기준', '分析と実施基準'),
 'Strength': ('강점', '強み'), 'Weakness': ('약점', '弱み'),
 'Easiest to cross-check': ('요구사항 대조가 가장 쉬움', '要件との照合が最も容易'),
 'Permissions scattered across three places': ('권한 체계가 세 곳에 흩어져 읽힘', '権限体系が3か所に分散'),
 'One spine; matches the key sentence': ('뼈대 하나, 핵심 문장과 맞음', '骨格が一本、核心文と一致'),
 'Leaves RFP order': ('RFP 순서를 벗어남', 'RFPの順序から外れる'),
 'Reads as a story': ('이야기처럼 읽힘', '物語として読める'),
 'Permissions arrive late': ('권한이 늦게 나옴', '権限の説明が後回しに'),
 'Plan B · Around the 3-tier permission structure': ('B안 · 권한 3층 구조 중심으로', 'B案・権限3層構造を中心に'),
 'Preview': ('프리뷰', 'プレビュー'),
 '/ 17 pages written': ('/ 17장 작성', '/ 17ページ作成'),
 'Writing to your decisions…': ('결정대로 작성 중…', '決定どおり作成中…'),
 '✓ 17 pages written · design system applied': ('✓ 17장 작성 완료 · 디자인 시스템 적용', '✓ 17ページ作成完了・デザインシステム適用'),
 'Permission framework · 3-tier design': ('권한 체계 · 3층 권한 설계', '権限体系・3層権限設計'),
 'III. Project execution · 1. Functional requirements': ('III. 프로젝트 수행 · 1. 기능개선수행 요구사항', 'III. プロジェクト遂行・1. 機能改善要件'),
 'Menus follow the role,': ('메뉴는 역할에 따라,', 'メニューは役割に、'),
 'what you can see follows the institution': ('볼 수 있는 자료는 소속에 따라', '閲覧範囲は所属に従う'),
 'Three tiers decide what you see.': ('3층 구조가 볼 수 있는 범위를 정합니다.', '3層が閲覧範囲を決める。'),
 'The server enforces it — not the screen.': ('지키는 건 화면이 아니라 서버입니다.', '守るのは画面ではなくサーバー。'),
 'Role': ('역할', '役割'), 'Menu access': ('메뉴 접근', 'メニュー権限'), 'Lookup scope': ('조회 범위', '照会範囲'), 'Actions': ('처리 권한', '操作権限'),
 'Tier 1 · Central admin': ('1층 중앙관리자', '第1層 中央管理者'), 'All menus · permission settings': ('전체 메뉴·권한 설정', '全メニュー・権限設定'), 'Every institution and school': ('전국 기관·학교 전체', '全国の機関・学校すべて'), 'Settings · export · all': ('설정·출력 전 기능', '設定・出力の全機能'),
 'Tier 2 · Office / program team': ('2층 교육청·사업팀 관리자', '第2層 教育庁・事業チーム管理者'), 'Cases · screening · stats · institutions': ('사례·검사·통계·기관', '事例・検査・統計・機関'), 'Institutions in jurisdiction': ('관할 기관·학교', '管轄の機関・学校'), 'View · edit · export': ('관할 내 조회·수정·출력', '管轄内の照会・修正・出力'),
 'Tier 3 · Referral teacher': ('3층 의뢰교사', '第3層 依頼教員'), 'Screening · referral · linkage': ('검사·의뢰·연계', '検査・依頼・連携'), 'Assigned schools & students': ('담당 학교·담당 학생', '担当校・担当学生'), 'Run screening · request linkage': ('검사 실시·연계 요청', '検査実施・連携依頼'),
 'Tier 3 · Counselor': ('3층 상담교사', '第3層 相談教員'), 'Cases · counseling records': ('사례·상담 기록', '事例・相談記録'), 'Linked students only': ('연계받은 학생', '連携された学生のみ'), 'Write counseling records': ('상담 기록 작성', '相談記録の作成'),
 'Server-side check': ('서버 측 판정', 'サーバー側判定'),
 "Scope is judged on the server from the login's institution code — out-of-scope records never load.": ('로그인한 사람의 소속 기관 코드로 서버에서 판정 — 범위 밖 자료는 조회되지 않습니다', 'ログイン者の所属機関コードでサーバー側が判定 — 範囲外のデータは表示されません'),
 'School mental-health case management system · Permission matrix': ('학교 정신건강 위기지원 사례관리시스템 · 권한 매트릭스 설정', '学校メンタルヘルス事例管理システム・権限マトリクス設定'),
 'Role × menu is configured; scope is judged by institution code': ('역할×메뉴 설정, 범위는 소속 코드로 판정', '役割×メニューを設定、範囲は所属コードで判定'),
 'Source: RFP FR-003 · FR-006 · 3-tier platform structure · menu scope to be confirmed on site': ('근거: 제안요청서 FR-003·FR-006 · 3층 플랫폼 구조 · 메뉴별 허용 범위 현장 확인 필요', '根拠：提案依頼書 FR-003・FR-006・3層プラットフォーム構造・メニュー別許可範囲は現場確認要'),
 'NANUM VITAMIN': ('나눔비타민', 'NANUM VITAMIN'),
 'Rewriting page 1 to your note…': ('메모대로 1장 다시 쓰는 중…', 'メモどおり1ページ目を書き直し中…'),
 'Live status dashboard': ('실시간 현황 화면', 'リアルタイム状況画面'), 'Role-based permissions': ('역할별 권한 체계', '役割別の権限体系'), 'Same-format data': ('같은 형식 데이터', '同じ形式のデータ'),
}
R_TITLES = {
 'ko': ['3층 구조의 권한 설계','권한 부여와 변경 이력','기관정보와 소속 현황','개인정보 접근 통제','의뢰교사 검사 권한과 연계','상담교사 사례 기록','복수 학교 담당 교사','사례관리 절차와 진행현황','사용자 중심 입력화면','다기준 운영 현황 통계','통계 출력과 성과 시각화','검사 자동화','정보 비노출 단체문자','검색과 조회','알림','산출물과 수행기준','보안 11개 항목'],
 'ja': ['3層構造の権限設計','権限付与と変更履歴','機関情報と所属状況','個人情報アクセス制御','依頼教員の検査権限と連携','相談教員の事例記録','複数校担当の教員','事例管理手順と進捗','ユーザー中心の入力画面','多基準の運営状況統計','統計出力と成果の可視化','検査の自動化','情報非表示の一斉SMS','検索と照会','通知','成果物と実施基準','セキュリティ11項目'],
}

RUNTIME = """
// ---- UI localization: replace text nodes / placeholders / data-type by exact match
const UI = %s;
const L = (s) => { const v = UI[s]; return v && v[LANG] ? v[LANG] : s; };
(function localizeUI() {
  if (LANG === 'en' || LANG === 'zh') return;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const n of nodes) { const t = n.nodeValue; const k = t.trim(); if (!k || !UI[k] || !UI[k][LANG]) continue; n.nodeValue = t.replace(k, UI[k][LANG]); }
  document.querySelectorAll('[placeholder]').forEach(el => el.setAttribute('placeholder', L(el.getAttribute('placeholder'))));
  document.querySelectorAll('[data-type]').forEach(el => el.setAttribute('data-type', L(el.getAttribute('data-type'))));
})();
"""

def inject(fname, table, extra=''):
    s = open(D + fname).read()
    ui = {k: {'ko': v[0], 'ja': v[1]} for k, v in table.items()}
    block = RUNTIME % json.dumps(ui, ensure_ascii=False) + extra
    a = "document.documentElement.lang = LANG;\n"
    assert a in s
    s = s.replace(a, a + block, 1)
    return s

# problem.html: dynamic strings
s = inject('problem.html', P)
rep = [
 ("$('#mcount').textContent = `${i + 1} slides`;", "$('#mcount').textContent = L('{n} slides').replace('{n}', i + 1);"),
 ("$('#st').innerHTML = '✓ Done · 100 slides';", "$('#st').innerHTML = L('✓ Done · 100 slides');"),
 ("$('#ffoot').textContent = '47 of 47 selected, 312 MB';", "$('#ffoot').textContent = L('47 of 47 selected, 312 MB');"),
 ("$('#hint').textContent = 'Release to add 47 files';", "$('#hint').textContent = L('Release to add 47 files');"),
]
for a, b in rep:
    assert a in s, a; s = s.replace(a, b)
s = s.replace("const UI = ", "UI['{n} slides'] = %s;\nconst UI = " % json.dumps({'ko': P_DYN['{n} slides'][0], 'ja': P_DYN['{n} slides'][1]}, ensure_ascii=False), 1) if False else s
# add dyn key into UI json directly
s = s.replace('"47 items":', '"{n} slides": %s, "47 items":' % json.dumps({'ko': P_DYN['{n} slides'][0], 'ja': P_DYN['{n} slides'][1]}, ensure_ascii=False), 1)
open(D + 'problem.html', 'w').write(s); print('problem.html localized')

# replay.html: dynamic strings (TITLES, chat option names)
s = inject('replay.html', R)
a = "const TITLES = ["; assert a in s
s = s.replace(a, "const TITLES_L = %s;\nconst TITLES = (TITLES_L[LANG] || null) || [" % json.dumps(R_TITLES, ensure_ascii=False), 1)
# the option names in AI messages are English literals inside strings -> wrap with L()
for en in ['Field pain, shipped fast', 'Zero-downtime, zero-leak upgrade', 'Data-driven program operations', 'Live status dashboard', 'Role-based permissions', 'Same-format data']:
    lit = "<b>%s</b>%s</div>"
    for n in '123':
        old = "<div><b>%s</b>%s</div>" % (n, en)
        if old in s: s = s.replace(old, "<div><b>%s</b>' + L('%s') + '</div>" % (n, en))
a = "addMsg('ai', '<div class=\"who\"><i></i>Contrl</div>' + T.ai4);"; assert a in s
s = s.replace("$('#pv-status').innerHTML = '<span class=\"ok\">✓ 17 pages written · design system applied</span>';", "$('#pv-status').innerHTML = '<span class=\"ok\">' + L('✓ 17 pages written · design system applied') + '</span>';")
s = s.replace("$('#ks-val').textContent = 'Role-based permissions connect student support';", "$('#ks-val').textContent = L('Role-based permissions connect student support');")
s = s.replace("$('#dv-val').textContent = 'Plan B · Around the 3-tier permission structure';", "$('#dv-val').textContent = L('Plan B · Around the 3-tier permission structure');")
open(D + 'replay.html', 'w').write(s); print('replay.html localized')
