"""
2026년 부동산 매수 도우미 — PyQt6 데스크톱 앱
탭 1: 지역별 집수리 지원금
탭 2: 구비 서류
탭 3: 임장 체크리스트
"""

import sys
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QLabel, QPushButton, QFrame, QCheckBox,
    QButtonGroup, QProgressBar, QSizePolicy, QGroupBox, QGridLayout,
    QComboBox, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QFontDatabase

# ── 색상 팔레트 ──────────────────────────────────────────────────────────────
C = {
    "primary":      "#1F4E79",
    "secondary":    "#2E75B6",
    "accent":       "#C55A11",
    "blue_bg":      "#DEEAF1",
    "blue_border":  "#2E75B6",
    "green_bg":     "#E2EFDA",
    "green_border": "#70AD47",
    "orange_bg":    "#FCE4D6",
    "orange_border":"#ED7D31",
    "purple_bg":    "#EAE3F5",
    "purple_border":"#7030A0",
    "red_bg":       "#FDECEA",
    "red_border":   "#C00000",
    "yellow_bg":    "#FFF2CC",
    "yellow_border":"#FFB300",
    "teal_bg":      "#D9F1F1",
    "teal_border":  "#009688",
    "gray_bg":      "#F2F2F2",
    "gray_border":  "#BDBDBD",
    "indigo_bg":    "#E8EAF6",
    "indigo_border":"#3949AB",
    "white":        "#FFFFFF",
    "dark":         "#1A1A1A",
    "warn_bg":      "#FFF3CD",
    "warn_border":  "#F0A500",
}

COLOR_THEME = {
    "blue":   (C["blue_bg"],   C["blue_border"],   C["secondary"]),
    "green":  (C["green_bg"],  C["green_border"],  "#388E3C"),
    "orange": (C["orange_bg"], C["orange_border"], "#D84315"),
    "purple": (C["purple_bg"], C["purple_border"], "#6A1B9A"),
    "red":    (C["red_bg"],    C["red_border"],    "#B71C1C"),
    "yellow": (C["yellow_bg"], C["yellow_border"], "#E65100"),
    "teal":   (C["teal_bg"],   C["teal_border"],   "#00695C"),
    "gray":   (C["gray_bg"],   C["gray_border"],   "#424242"),
    "indigo": (C["indigo_bg"], C["indigo_border"],  "#283593"),
}

SECTION_COLOR = {
    "기본서류": "blue", "권리관계": "red", "건물상태": "orange",
    "주변환경": "green", "점유확인": "purple", "가격협상": "yellow",
}

# ── 데이터 ────────────────────────────────────────────────────────────────────
REGION_DATA = {
    "서울": {
        "programs": [
            {
                "name": "안심 집수리 보조사업",
                "target": "사용승인 후 10년 이상 저층주택 (단독·다가구·다세대·연립)",
                "who": "① 주거취약가구: 기초수급자·차상위·한부모가족 등 중위소득 이하\n② 반지하 주택\n③ 주택성능개선지원구역 내 20년 이상 주택",
                "amount": "① 주거취약가구: 공사비 80%, 최대 1,200만원\n② 반지하: 공사비 50%, 최대 600만원 (빗물 유입 방지 시설 등)\n③ 지원구역: 공사비 50%, 최대 1,200만원",
                "works": "단열·방수·창호·설비, 침수·화재 안전시설, 빗물 유입 방지 시설",
                "note": "보조사업: 통상 4월경 신청(자치구별 상이) / 융자사업: 예산 소진 시까지 상시 접수\n\n[위반건축물 기준]\n① 건축물대장에 위반건축물로 표기된 주택은 지원 불가\n② 예외: 불법건축물 기준이 해소(양성화)된 옥탑방 — 단, 건축물대장에 양성화 사실이 명확히 기재된 경우에 한함\n③ 반지하 주택: 건축물대장·현황이 지하층이어야 하며, 창고 등 비주거 용도 사용 시 제외",
                "apply": "주택 소재 자치구 담당부서 / 집수리닷컴(jibsuri.seoul.go.kr)",
                "url": "https://jibsuri.seoul.go.kr",
                "color": "blue",
            },
            {
                "name": "안심 집수리 융자 지원",
                "target": "사용승인 후 20년 이상 저층주택 (서울 전 지역)",
                "who": "주택 소유자 (소득 제한 없음)",
                "amount": "최대 6,000만원(단독) / 연 0.7% 고정금리",
                "works": "지붕·외벽·단열·창호·도배·장판·설비 등 전반",
                "note": "공시가격 9억원 이상·재개발구역 주택 제외. 최근 3~5년 내 유사 지원 수혜자 신청 불가. 지방세 체납 시 탈락",
                "apply": "관할 자치구 담당부서 / 집수리닷컴",
                "url": "https://jibsuri.seoul.go.kr",
                "color": "green",
            },
        ],
        "contact": "서울주거포털 집수리닷컴 (jibsuri.seoul.go.kr) / 서울시 주택정책과 ☎ 02-120",
        "tip": "집수리닷컴에서 찾아가는 무료 상담 신청 가능. 공사업체 선정 전 상담 필수",
    },
    "경기": {
        "programs": [
            {
                "name": "소규모 노후주택 집수리 지원",
                "target": "단독주택: 사용승인 20년 이상\n소규모 공동주택(빌라 등): 15년 이상",
                "who": "도내 전 지역 소유자\n우선순위: 주거취약계층 > 반지하 > 중위소득 100% 이하",
                "amount": "공사비 90% 지원 (자부담 10%)\n• 단독주택: 최대 1,200만원\n• 공동(공용부): 최대 1,600만원\n• 공동(전유): 최대 500만원\n※ 기초수급자 등 취약계층: 자부담 면제(100% 지원)",
                "works": "지붕·외벽·단열·방수공사, 경관개선(담장·대문), 방범창 등 안전시설",
                "note": "제외: 공시가격 9억원 이상, 재개발구역. 2025년 194개 지역 추진. 시·군별 일정 상이",
                "apply": "해당 시·군 도시재생·주택 담당부서",
                "url": "https://www.gg.go.kr",
                "color": "purple",
            },
        ],
        "contact": "경기도청 도시재생과 ☎ 031-8008-3800 / 각 시·군 담당부서",
        "tip": "'찾아가는 집수리 기술자문' 서비스 활용 가능. 불법 건축물·세금 체납 시 지원 불가",
    },
    "인천": {
        "programs": [
            {
                "name": "남동구 — 마을주택관리소 사업",
                "target": "사용승인 후 20년 이상 경과 주택",
                "who": "중위소득 50~70% 이하 (수급자·장애인·국가유공자 등 우선)",
                "amount": "가구당 최대 500만원",
                "works": "지붕·외벽·단열·창호·내부 마감 등",
                "note": "남동구 거주 확인 필수. 타 구는 해당 구청에 별도 확인",
                "apply": "인천 남동구청 주택과",
                "url": "https://www.namdong.go.kr",
                "color": "orange",
            },
            {
                "name": "중구 — 저층주거지 재생사업",
                "target": "월남촌 사랑마을 등 특정 구역 내 20년 이상 노후 주택",
                "who": "해당 구역 주택 소유자",
                "amount": "공사비 80% 지원\n• 단독주택: 최대 1,200만원\n• 공동주택 공용부: 최대 1,600만원",
                "works": "지붕·외벽·단열·창호 등",
                "note": "구역 지정 여부 사전 확인 필수. 구역 외는 주거급여 수선유지급여 활용",
                "apply": "인천 중구청 도시재생과",
                "url": "https://www.icjung.go.kr",
                "color": "teal",
            },
        ],
        "contact": "인천시 주택정책과 ☎ 032-440-4749 / 해당 자치구청 주택·도시재생과",
        "tip": "재생사업 구역 여부는 인천시 도시재생지원센터 또는 해당 구청에 문의. 구별 지원 조건 상이",
    },
    "부산": {
        "programs": [
            {
                "name": "희망의 집수리 사업",
                "target": "저소득 주거 취약가구 노후 주택",
                "who": "중위소득 60% 이하 가구 (반지하 우선 지원)",
                "amount": "도배·장판·단열 등 18개 항목 수리 지원",
                "works": "도배·장판·단열·창호·설비 등 18개 항목",
                "note": "반지하 주택 우선 지원. 구·군별 예산 배정 상이, 조기 신청 권장",
                "apply": "부산시 각 구·군 건축·주택 담당부서",
                "url": "https://www.busan.go.kr",
                "color": "red",
            },
        ],
        "contact": "부산시 도시주택국 ☎ 051-888-3700",
        "tip": "청년모두家(공공임대 임대료 지원), 청년 중개보수·이사비(최대 40만원) 지원도 별도 확인",
    },
    "대구": {
        "programs": [
            {
                "name": "노후 공동주택 공용시설 수리비 지원 (북구)",
                "target": "사용검사 후 10년 이상, 20세대 미만 소규모 공동주택",
                "who": "북구 소재 입주자대표회의",
                "amount": "공용시설 수리비 70% 지원",
                "works": "옥상·담장·주차장·복도·경로당 등 공용부분",
                "note": "20세대 이상 단지형 아파트 및 타 구는 해당 구청에 별도 확인",
                "apply": "대구 북구청 도시재생·주택과",
                "url": "https://www.daegu.go.kr",
                "color": "indigo",
            },
        ],
        "contact": "대구시 도시주택국 ☎ 053-803-6500 / 해당 구청 주택과",
        "tip": "도시재생뉴딜사업 구역 내 추가 지원 가능. 해당 구청에 구역 포함 여부 확인",
    },
    "세종·대전": {
        "programs": [
            {
                "name": "주거취약가구 수리 지원",
                "target": "노후 주택 (연수 기준 지자체 별도 확인)",
                "who": "중위소득 80% 이내 주거 취약가구",
                "amount": "가구당 최대 400만원 이내",
                "works": "창호·단열·난방 등 집수리 (생활 필수 항목 위주)",
                "note": "세종·대전 공통 기준. 지자체별 세부 조건 상이하므로 해당 구청·동사무소 확인 필수",
                "apply": "해당 시청·구청·동 행정복지센터",
                "url": "https://www.gov.kr",
                "color": "teal",
            },
        ],
        "contact": "세종시청 ☎ 044-300-3114 / 대전시청 ☎ 042-120",
        "tip": "정부24 '보조금24' 메뉴에서 본인 인증 후 지역별 혜택 통합 조회 가능",
    },
    "농어촌": {
        "programs": [
            {
                "name": "농촌주택개량사업 저금리 융자",
                "target": "농어촌 지역 노후 주택",
                "who": "농촌 주택 소유자·귀농·귀촌 예정자",
                "amount": "신축: 최대 2억5천만원 / 증·개축·대수선: 최대 1억5천만원\n연 2% (청년 1.5%) 저금리\n※ 취득세 최대 280만원 감면 (~2027년 말)",
                "works": "주택 신축·증축·개축·리모델링 전반",
                "note": "취득세 감면 혜택 2027년 12월 31일까지. 귀농귀촌종합센터 상담 권장",
                "apply": "농림축산식품부 / 해당 지역 농협",
                "url": "https://www.returnfarm.com",
                "color": "green",
            },
            {
                "name": "농촌 빈집 철거 보조금",
                "target": "1년 이상 방치된 농촌 빈집",
                "who": "빈집 소유자 (전국)",
                "amount": "일반: 최대 300만원 / 슬레이트(석면) 지붕: 최대 400만원",
                "works": "건물 철거, 석면·슬레이트 안전 처리 포함",
                "note": "지자체 지정 업체 사용 의무. 사전 신청 후 진행 필수",
                "apply": "해당 읍·면·동 사무소 또는 시·군청 농촌개발과",
                "url": "https://www.gov.kr",
                "color": "yellow",
            },
            {
                "name": "슬레이트 지붕 철거 지원 (전국)",
                "target": "슬레이트(석면) 지붕 주택 — 소규모 주택 우선",
                "who": "전국 슬레이트 지붕 건물 소유자",
                "amount": "주택 기준 최대 700만원 한도 내 철거비 지원",
                "works": "석면 슬레이트 철거 및 안전 처리",
                "note": "반드시 지자체 신청 후 지정 업체 사용. 자의적 철거 시 지원 불가",
                "apply": "환경부 / 해당 시·군·구 환경부서",
                "url": "https://www.me.go.kr",
                "color": "gray",
            },
        ],
        "contact": "귀농귀촌종합센터 ☎ 1899-9097 / 각 읍·면·동 사무소",
        "tip": "그린리모델링 이자지원(창호·단열 공사 이자 국가 지원)은 전국 공통 — 에너지공단 ☎ 1588-6106 문의",
    },
}

DOCS_DATA = [
    {
        "category": "주택 수리·리모델링 지원",
        "subtitle": "서울·경기·인천 등 집수리 보조금·융자",
        "color": "blue",
        "groups": [
            {
                "title": "기본 서류",
                "items": [
                    {"text": "지원 신청서 (해당 기관 양식)", "required": True},
                    {"text": "개인정보 수집·이용 동의서", "required": True},
                    {"text": "신분증 사본 (주민등록증 또는 운전면허증)", "required": True},
                ],
            },
            {
                "title": "소유 및 자격 증빙",
                "items": [
                    {"text": "건축물대장 (위반건축물 여부 확인)", "required": True},
                    {"text": "등기사항전부증명서 (소유자 확인)", "required": True},
                    {"text": "지방세 완납 증명서 ※ 체납 시 지원 불가", "required": True},
                    {"text": "기초생활수급자·차상위·한부모 증명서 (해당자 — 가점·자부담 면제)", "required": False},
                ],
            },
            {
                "title": "공사 관련 서류",
                "items": [
                    {"text": "공사 계획서 및 견적서 (수리 항목·예상 비용 내역)", "required": True},
                    {"text": "공사 전 현장 사진 (수리 필요 부위)", "required": True},
                    {"text": "입주자(구분소유자) 동의서 — 공동주택 공용부 수리 시: 2/3 이상 동의", "required": False},
                    {"text": "소유주(임대인) 동의서 — 임차인이 신청할 경우 필수", "required": False},
                ],
            },
        ],
        "tip": "대부분의 서류는 공고일 이후 발급분만 인정됩니다. 신청 전 발급 시기를 반드시 확인하세요.",
        "warnings": [
            {"title": "위반건축물 (서울 기준)", "body": "건축물대장에 위반건축물로 표기된 주택은 원칙적으로 지원 불가. 단, 양성화된 옥탑방은 건축물대장에 양성화 사실이 명확히 기재된 경우에 한해 신청 가능."},
            {"title": "반지하 주택 요건", "body": "건축물대장 및 실제 현황이 '지하층'이어야 함. 창고 등 비주거 용도로 사용 중인 경우 제외."},
            {"title": "중복 지원 제한", "body": "최근 3~5년 이내 주거급여 수선유지급여 등 유사 공공 지원을 받은 경우 신청 제한."},
            {"title": "지방세 체납", "body": "지방세 체납 시 지원 탈락 — 사전 납부 완료 후 납세완납증명서 제출 필수."},
        ],
    },
    {
        "category": "청년·신혼부부 주거비·이사비 지원",
        "subtitle": "부산·대구 등 주거비·중개보수·이사비 지원",
        "color": "green",
        "groups": [
            {
                "title": "가족 및 주거 확인",
                "items": [
                    {"text": "주민등록등본 (세대원 구성·주소지 확인)", "required": True},
                    {"text": "가족관계증명서(상세) (부모·배우자 관계 확인)", "required": True},
                    {"text": "임대차계약서 사본 (확정일자 날인된 계약서 또는 공공임대 계약서)", "required": True},
                ],
            },
            {
                "title": "소득 및 자격 증빙",
                "items": [
                    {"text": "건강보험 자격득실확인서 (최근 3개월분)", "required": True},
                    {"text": "건강보험료 납부확인서 (소득 검증·맞벌이 여부 확인)", "required": True},
                    {"text": "혼인관계증명서(상세) — 신혼부부 전세임대료 지원 시 필수", "required": False},
                ],
            },
            {
                "title": "지출 증빙 (이사비 지원 시)",
                "items": [
                    {"text": "이사비·중개보수 계좌이체 내역 또는 현금영수증", "required": True},
                    {"text": "이사비 영수증", "required": True},
                    {"text": "본인 명의 통장 사본 (지원금 수령용)", "required": True},
                ],
            },
        ],
        "tip": "건강보험 납부확인서는 최근 3개월분을 요구하는 경우가 많으므로 신청 직전 발급하세요.",
        "warnings": [],
    },
    {
        "category": "농어촌 빈집 정비·주택 개량",
        "subtitle": "전국 공통 — 농촌 빈집 철거·개량 융자",
        "color": "yellow",
        "groups": [
            {
                "title": "빈집 철거 지원",
                "items": [
                    {"text": "건축물대장 및 등기사항전부증명서 (소유자 확인)", "required": True},
                    {"text": "제적등본·가족관계증명서 — 소유자 사망 시", "required": False},
                    {"text": "상속인 전원 동의서·위임장·인감증명서 — 소유자 사망 시", "required": False},
                    {"text": "과세 자료 또는 소유 사실 확인서 — 무허가 건물 소유 증빙 대체", "required": False},
                ],
            },
            {
                "title": "농지 취득 및 주택 개량 융자",
                "items": [
                    {"text": "농업경영계획서 (직업·영농 경력·영농 거리 기재 + 재직증명서 등 증빙)", "required": True},
                    {"text": "재산세 과세 증명서(전국 단위) — 무주택·1세대2주택 제외 확인", "required": True},
                    {"text": "귀농·귀촌 확인서 (해당자)", "required": False},
                ],
            },
        ],
        "tip": "소유자가 사망한 경우 상속인 전원의 동의·인감이 필요합니다. 상속 정리를 먼저 완료하거나 법무사 조력을 받는 것을 권장합니다.",
        "warnings": [],
    },
    {
        "category": "그린리모델링 및 기타",
        "subtitle": "에너지 성능 개선 공사·대리 신청",
        "color": "teal",
        "groups": [
            {
                "title": "그린리모델링 — 정산 서류 (공사 완료 후)",
                "items": [
                    {"text": "세금계산서 (공사비)", "required": True},
                    {"text": "준공검사조서", "required": True},
                    {"text": "공사 전·후 사진 대지", "required": True},
                    {"text": "자재 납품확인서", "required": True},
                ],
            },
            {
                "title": "대리 신청 시 추가 서류",
                "items": [
                    {"text": "위임장 (위임자 자필 서명)", "required": True},
                    {"text": "위임자 신분증 사본", "required": True},
                    {"text": "수임자(대리인) 신분증 원본", "required": True},
                ],
            },
        ],
        "tip": "그린리모델링은 공사 완료 후 정산 서류가 매우 까다롭습니다. 공사 전·중·후 사진을 단계별로 촬영해 두세요.",
        "warnings": [],
    },
]

CHECKLIST_DATA = {
    "기본서류": {
        "icon": "📋",
        "items": [
            {"id": "d1", "text": "등기사항전부증명서 (갑구·을구 전체) — 방문 당일 최신본", "critical": True},
            {"id": "d2", "text": "건축물대장 (일반·집합) — 용도·면적·위반건축물 여부", "critical": True},
            {"id": "d3", "text": "토지등기사항전부증명서", "critical": True},
            {"id": "d4", "text": "토지이용계획확인원 — 용도지역·도시계획시설 저촉 여부", "critical": False},
            {"id": "d5", "text": "지적도 (토지 경계·접도 확인)", "critical": False},
            {"id": "d6", "text": "공시지가 확인 (국토부 공시지가 열람)", "critical": False},
        ],
    },
    "권리관계": {
        "icon": "⚖️",
        "items": [
            {"id": "r1", "text": "근저당·저당권 설정 여부 및 채권최고액 확인", "critical": True},
            {"id": "r2", "text": "가압류·가처분·가등기 존재 여부", "critical": True},
            {"id": "r3", "text": "전세권·지상권·지역권 설정 여부", "critical": True},
            {"id": "r4", "text": "임차인 존재 시: 전입신고일·확정일자·보증금 금액", "critical": True},
            {"id": "r5", "text": "경매개시결정 여부 (등기부 확인)", "critical": True},
            {"id": "r6", "text": "재건축·재개발 구역 편입 여부 (정비사업정보시스템)", "critical": False},
        ],
    },
    "건물상태": {
        "icon": "🏠",
        "items": [
            {"id": "b1", "text": "외벽·지붕 균열·누수·박리 흔적 확인", "critical": True},
            {"id": "b2", "text": "지하실·반지하 침수 흔적 (벽면 수위 자국)", "critical": True},
            {"id": "b3", "text": "창호 단열 상태 (결로·곰팡이 흔적)", "critical": False},
            {"id": "b4", "text": "배관·수도·보일러 상태 (녹물·소음)", "critical": False},
            {"id": "b5", "text": "전기 배선·분전함 노후화 여부", "critical": False},
            {"id": "b6", "text": "불법 증·개축 여부 (건축물대장 대조)", "critical": True},
            {"id": "b7", "text": "석면·슬레이트 지붕 여부 (노후 건물)", "critical": False},
        ],
    },
    "주변환경": {
        "icon": "🗺️",
        "items": [
            {"id": "e1", "text": "도로 접도 조건 확인 (건축허가 가능 폭 4m 이상)", "critical": True},
            {"id": "e2", "text": "대중교통 접근성 (버스·지하철 도보 거리)", "critical": False},
            {"id": "e3", "text": "혐오시설 인근 여부 (쓰레기 처리장·장례식장 등)", "critical": False},
            {"id": "e4", "text": "소음원 확인 (간선도로·철도·공장)", "critical": False},
            {"id": "e5", "text": "일조권·채광 (남향 여부, 주변 건물 높이)", "critical": False},
            {"id": "e6", "text": "주변 신규 개발 계획 (호재·악재 판단)", "critical": False},
            {"id": "e7", "text": "학군·편의시설 (마트·병원·학교) 거리", "critical": False},
        ],
    },
    "점유확인": {
        "icon": "👥",
        "items": [
            {"id": "o1", "text": "현재 거주자 확인 (세입자인지 소유자인지)", "critical": True},
            {"id": "o2", "text": "임대차계약서 원본 확인 (계약기간·보증금·월세)", "critical": True},
            {"id": "o3", "text": "전입세대 열람원 확인 (실제 거주자 수)", "critical": True},
            {"id": "o4", "text": "명도 일정 협의 (잔금일 기준 이사 완료 확인)", "critical": True},
            {"id": "o5", "text": "관리비 체납 여부 (공동주택 관리사무소 문의)", "critical": False},
            {"id": "o6", "text": "공과금·재산세 체납 여부 확인", "critical": False},
        ],
    },
    "가격협상": {
        "icon": "💰",
        "items": [
            {"id": "p1", "text": "국토부 실거래가 최근 3년 비교 분석", "critical": True},
            {"id": "p2", "text": "공시지가 대비 매도호가 비율 확인", "critical": False},
            {"id": "p3", "text": "리모델링·수리 예상 비용 감안한 실질 가격 산정", "critical": False},
            {"id": "p4", "text": "인근 동일 면적 급매물 비교", "critical": False},
            {"id": "p5", "text": "매도자 매도 사유·급매 여부 파악 (협상 레버리지)", "critical": False},
            {"id": "p6", "text": "지원사업 해당 시 수리비 지원금 감안한 수익 계산", "critical": False},
        ],
    },
}

QUICK_LINKS = [
    ("정부24", "https://www.gov.kr", "주민등록등본·건축물대장·지방세납세증명"),
    ("대법원 인터넷등기소", "https://www.iros.go.kr", "등기사항전부증명서"),
    ("국민건강보험공단", "https://www.nhis.or.kr", "자격득실확인서·납부확인서"),
    ("복지로", "https://www.bokjiro.go.kr", "수급자·차상위 증명서"),
    ("국토부 실거래가", "https://rt.molit.go.kr", "실거래가 공개시스템"),
]

NATIONAL_PROGRAMS = [
    "주거급여 수선유지급여: 기준 중위소득 48% 이하 — 경보수 38만원 / 중보수 702만원 / 대보수 1,241만원 (주민센터 신청)",
    "그린리모델링 이자지원: 창호·단열 공사비 대출 이자 국가 보전 → 에너지공단 ☎ 1588-6106",
    "슬레이트 지붕 철거: 주택 기준 최대 700만원 → 해당 시·군·구 환경부서 신청",
]


# ── 공통 위젯 헬퍼 ────────────────────────────────────────────────────────────
def make_label(text, bold=False, size=10, color="#1A1A1A", wrap=True):
    lbl = QLabel(text)
    font = QFont("Malgun Gothic", size)
    font.setBold(bold)
    lbl.setFont(font)
    lbl.setStyleSheet(f"color: {color};")
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def make_card(bg, border, radius=8, padding=12):
    frame = QFrame()
    frame.setStyleSheet(
        f"QFrame {{ background:{bg}; border:2px solid {border}; "
        f"border-radius:{radius}px; padding:{padding}px; }}"
    )
    return frame


def make_tip_box(text, bg="#E3F2FD", border="#90CAF9", prefix="💡 "):
    frame = QFrame()
    frame.setStyleSheet(
        f"QFrame {{ background:{bg}; border:1px solid {border}; "
        f"border-radius:6px; padding:8px; }}"
    )
    lbl = make_label(prefix + text, size=9)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(4, 4, 4, 4)
    layout.addWidget(lbl)
    return frame


def make_section_header(text, bg, radius=6):
    lbl = QLabel(text)
    lbl.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
    lbl.setStyleSheet(
        f"color: white; background:{bg}; border-radius:{radius}px; "
        f"padding: 6px 10px;"
    )
    return lbl


def scrollable(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    scroll.setStyleSheet("QScrollArea { border: none; background: #F5F7FA; }")
    return scroll


# ── 탭 1: 지역별 집수리 지원금 ─────────────────────────────────────────────────
class SupportTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # 경고 배너
        warn = make_tip_box(
            "지원사업은 예산 소진 시 조기 마감됩니다. 반드시 해당 기관에 최신 공고를 직접 확인하세요.",
            bg=C["warn_bg"], border=C["warn_border"], prefix="⚠️  "
        )
        outer.addWidget(warn)

        # 지역 선택 콤보박스
        region_bar = QHBoxLayout()
        region_bar.addWidget(make_label("지역 선택:", bold=True, size=10))
        self.combo = QComboBox()
        self.combo.addItems(list(REGION_DATA.keys()))
        self.combo.setFont(QFont("Malgun Gothic", 10))
        self.combo.setFixedHeight(32)
        self.combo.currentTextChanged.connect(self._load_region)
        region_bar.addWidget(self.combo)
        region_bar.addStretch()
        outer.addLayout(region_bar)

        # 스크롤 영역
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(12)
        outer.addWidget(scrollable(self.content_widget))

        self._load_region("서울")

    def _load_region(self, region_name):
        # 기존 위젯 제거
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        data = REGION_DATA[region_name]

        for prog in data["programs"]:
            self.content_layout.addWidget(self._make_program_card(prog))

        # 문의처
        contact_box = make_tip_box(data["contact"], bg="#E3F2FD", border="#90CAF9", prefix="📞  ")
        self.content_layout.addWidget(contact_box)

        # 팁
        if data.get("tip"):
            tip_box = make_tip_box(data["tip"], bg=C["green_bg"], border=C["green_border"], prefix="💡  ")
            self.content_layout.addWidget(tip_box)

        # 전국 공통
        nat = QGroupBox("🇰🇷  전국 공통 지원사업")
        nat.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
        nat.setStyleSheet(
            "QGroupBox { background:#263238; border-radius:8px; color:white; "
            "padding:10px; margin-top:6px; } "
            "QGroupBox::title { subcontrol-origin:margin; left:10px; color:white; }"
        )
        nat_layout = QVBoxLayout(nat)
        for line in NATIONAL_PROGRAMS:
            lbl = make_label("• " + line, size=9, color="#CFD8DC")
            nat_layout.addWidget(lbl)
        self.content_layout.addWidget(nat)
        self.content_layout.addStretch()

    def _make_program_card(self, prog):
        color = prog.get("color", "blue")
        bg, border, header_c = COLOR_THEME.get(color, COLOR_THEME["blue"])

        card = make_card(bg, border)
        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # 헤더
        header = make_section_header(prog["name"], header_c)
        layout.addWidget(header)

        rows = [
            ("대상 주택", prog["target"]),
            ("신청 자격", prog["who"]),
            ("💰 지원 금액", prog["amount"]),
            ("지원 공사 범위", prog["works"]),
            ("📌 주의·기간", prog["note"]),
            ("신청처", prog["apply"]),
        ]
        for label, value in rows:
            row = QHBoxLayout()
            lbl = make_label(label + "  ", bold=True, size=9, color="#555555", wrap=False)
            lbl.setMinimumWidth(90)
            lbl.setAlignment(Qt.AlignmentFlag.AlignTop)
            val = make_label(value, size=9)
            row.addWidget(lbl)
            row.addWidget(val, 1)
            layout.addLayout(row)

        # URL 버튼
        url_btn = QPushButton("🔗  사이트 바로가기")
        url_btn.setFont(QFont("Malgun Gothic", 9))
        url = prog["url"]
        url_btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
        url_btn.setStyleSheet(
            f"QPushButton {{ background:{header_c}; color:white; border-radius:4px; padding:4px 10px; }}"
            f"QPushButton:hover {{ opacity:0.8; }}"
        )
        layout.addWidget(url_btn, alignment=Qt.AlignmentFlag.AlignRight)
        return card


# ── 탭 2: 구비 서류 ────────────────────────────────────────────────────────────
class DocsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        warn = make_tip_box(
            "공고일 이후 발급분만 인정되는 경우가 많습니다. "
            "정부24 '보조금24' 또는 주민센터에서 최신 구비 서류 목록을 확인하세요.",
            bg=C["warn_bg"], border=C["warn_border"], prefix="⚠️  "
        )
        outer.addWidget(warn)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(14)

        for section in DOCS_DATA:
            layout.addWidget(self._make_section(section))

        # 범례
        legend = QFrame()
        legend.setStyleSheet(f"QFrame {{ background:{C['gray_bg']}; border-radius:6px; padding:6px; }}")
        leg_layout = QHBoxLayout(legend)
        leg_layout.addWidget(make_label("🔴 필수 제출", bold=True, size=9))
        leg_layout.addWidget(make_label("  🔵 해당 시 제출", size=9))
        leg_layout.addStretch()
        layout.addWidget(legend)

        # 빠른 링크
        link_box = QGroupBox("📎  서류 발급 빠른 링크")
        link_box.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
        link_box.setStyleSheet(
            "QGroupBox { background:#1A237E; border-radius:8px; color:white; padding:10px; margin-top:6px; }"
            "QGroupBox::title { subcontrol-origin:margin; left:10px; color:white; }"
        )
        link_layout = QGridLayout(link_box)
        for i, (name, url, desc) in enumerate(QUICK_LINKS):
            btn = QPushButton(name)
            btn.setFont(QFont("Malgun Gothic", 9, QFont.Weight.Bold))
            btn.setStyleSheet(
                "QPushButton { background:#3949AB; color:white; border-radius:4px; padding:4px 8px; }"
                "QPushButton:hover { background:#5C6BC0; }"
            )
            btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
            desc_lbl = make_label(desc, size=8, color="#B0BEC5")
            link_layout.addWidget(btn, i, 0)
            link_layout.addWidget(desc_lbl, i, 1)
        layout.addWidget(link_box)
        layout.addStretch()

        outer.addWidget(scrollable(content))

    def _make_section(self, section):
        color = section["color"]
        bg, border, header_c = COLOR_THEME.get(color, COLOR_THEME["blue"])

        card = make_card(bg, border)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        header = make_section_header(
            f"{section['category']}  —  {section['subtitle']}", header_c
        )
        layout.addWidget(header)

        for group in section["groups"]:
            grp_lbl = make_label(f"▸  {group['title']}", bold=True, size=9, color=header_c)
            layout.addWidget(grp_lbl)
            for item in group["items"]:
                dot = "🔴" if item["required"] else "🔵"
                suffix = "  [필수]" if item["required"] else ""
                row_lbl = make_label(f"  {dot}  {item['text']}{suffix}", size=9)
                layout.addWidget(row_lbl)

        if section.get("tip"):
            layout.addWidget(make_tip_box(section["tip"]))

        if section.get("warnings"):
            warn_lbl = make_label("🚫  신청 자격 제외 기준 (상세)", bold=True, size=9, color="#B71C1C")
            layout.addWidget(warn_lbl)
            for w in section["warnings"]:
                wf = QFrame()
                wf.setStyleSheet(
                    "QFrame { background:#FFEBEE; border:1px solid #EF9A9A; border-radius:5px; padding:6px; }"
                )
                wl = QVBoxLayout(wf)
                wl.setSpacing(2)
                wl.addWidget(make_label(f"⚠  {w['title']}", bold=True, size=9, color="#B71C1C"))
                wl.addWidget(make_label(w["body"], size=9, color="#C62828"))
                layout.addWidget(wf)

        return card


# ── 탭 3: 임장 체크리스트 ──────────────────────────────────────────────────────
class ChecklistTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checks = {}       # id → QCheckBox
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # 진행률 패널
        progress_frame = QFrame()
        progress_frame.setStyleSheet(
            "QFrame { background:white; border:1px solid #E0E0E0; border-radius:8px; padding:8px; }"
        )
        pf_layout = QVBoxLayout(progress_frame)

        top_row = QHBoxLayout()
        self.progress_lbl = make_label("임장 진행률", bold=True, size=10)
        self.count_lbl = make_label("0 / 0", bold=True, size=10, color=C["secondary"])
        top_row.addWidget(self.progress_lbl)
        top_row.addStretch()
        top_row.addWidget(self.count_lbl)
        pf_layout.addLayout(top_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet(
            "QProgressBar { border-radius:6px; background:#E0E0E0; }"
            "QProgressBar::chunk { border-radius:6px; background:#2196F3; }"
        )
        pf_layout.addWidget(self.progress_bar)

        self.status_lbl = make_label("", size=9, color="#C62828")
        pf_layout.addWidget(self.status_lbl)

        outer.addWidget(progress_frame)

        # 초기화 버튼
        reset_btn = QPushButton("🔄  전체 초기화")
        reset_btn.setFont(QFont("Malgun Gothic", 9))
        reset_btn.setStyleSheet(
            "QPushButton { border:2px solid #BDBDBD; border-radius:6px; padding:5px 12px; color:#555; background:white; }"
            "QPushButton:hover { background:#F5F5F5; }"
        )
        reset_btn.clicked.connect(self._reset)
        outer.addWidget(reset_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # 체크리스트 섹션
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)

        for section_name, section_data in CHECKLIST_DATA.items():
            section_widget = self._make_section(section_name, section_data)
            content_layout.addWidget(section_widget)

        # 계약 순서 안내
        guide = QFrame()
        guide.setStyleSheet("QFrame { background:#212121; border-radius:8px; padding:10px; }")
        gl = QVBoxLayout(guide)
        gl.addWidget(make_label("⚡  계약 전 핵심 순서", bold=True, size=10, color="white"))
        gl.addWidget(make_label(
            "① 등기부등본 확인  →  ② 현장 임장  →  ③ 대출 사전심사  "
            "→  ④ 자금조달계획서 작성  →  ⑤ 계약금 계좌이체  →  ⑥ 30일 내 거래신고",
            size=9, color="#BDBDBD"
        ))
        content_layout.addWidget(guide)
        content_layout.addStretch()

        outer.addWidget(scrollable(content))
        self._update_progress()

    def _make_section(self, name, data):
        color = SECTION_COLOR.get(name, "blue")
        bg, border, header_c = COLOR_THEME.get(color, COLOR_THEME["blue"])

        card = make_card(bg, border)
        layout = QVBoxLayout(card)
        layout.setSpacing(6)

        # 헤더 (아이콘 + 이름 + 카운트)
        header_row = QHBoxLayout()
        header_lbl = make_section_header(f"{data['icon']}  {name}", header_c)
        self.section_count_labels = getattr(self, "section_count_labels", {})
        count_lbl = make_label(f"0/{len(data['items'])}", bold=True, size=9,
                               color="white", wrap=False)
        count_lbl.setStyleSheet(
            f"color:white; background:{header_c}; border-radius:8px; padding:2px 8px;"
        )
        self.section_count_labels[name] = count_lbl
        header_row.addWidget(header_lbl, 1)
        header_row.addWidget(count_lbl)
        layout.addLayout(header_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{border};")
        layout.addWidget(sep)

        for item in data["items"]:
            cb = QCheckBox()
            cb.setFont(QFont("Malgun Gothic", 9))
            text = item["text"]
            if item["critical"]:
                cb.setText(text + "  ★필수")
                cb.setStyleSheet(
                    "QCheckBox { color:#1A1A1A; }"
                    "QCheckBox::indicator { width:16px; height:16px; }"
                    "QCheckBox:checked { color:#9E9E9E; text-decoration:line-through; }"
                )
            else:
                cb.setText(text)
                cb.setStyleSheet(
                    "QCheckBox { color:#333; }"
                    "QCheckBox::indicator { width:16px; height:16px; }"
                    "QCheckBox:checked { color:#9E9E9E; text-decoration:line-through; }"
                )
            cb.stateChanged.connect(self._update_progress)
            self.checks[item["id"]] = cb
            layout.addWidget(cb)

        return card

    def _update_progress(self):
        total = len(self.checks)
        checked = sum(1 for cb in self.checks.values() if cb.isChecked())
        pct = int(checked / total * 100) if total else 0

        self.count_lbl.setText(f"{checked} / {total}")
        self.progress_bar.setValue(pct)

        # 색상 변경
        if pct == 100:
            chunk_color = "#4CAF50"
        elif pct > 60:
            chunk_color = "#2196F3"
        else:
            chunk_color = "#FF9800"
        self.progress_bar.setStyleSheet(
            "QProgressBar { border-radius:6px; background:#E0E0E0; }"
            f"QProgressBar::chunk {{ border-radius:6px; background:{chunk_color}; }}"
        )

        # 필수 미완료 카운트
        critical_ids = {
            item["id"]
            for data in CHECKLIST_DATA.values()
            for item in data["items"]
            if item["critical"]
        }
        critical_left = sum(
            1 for iid, cb in self.checks.items()
            if iid in critical_ids and not cb.isChecked()
        )
        if critical_left:
            self.status_lbl.setText(f"🚨  필수 항목 {critical_left}개 미확인")
            self.status_lbl.setStyleSheet("color:#C62828;")
        else:
            self.status_lbl.setText("✅  필수 항목 모두 확인 완료")
            self.status_lbl.setStyleSheet("color:#388E3C;")

        # 섹션별 카운트 업데이트
        for section_name, data in CHECKLIST_DATA.items():
            lbl = self.section_count_labels.get(section_name)
            if lbl:
                sec_total = len(data["items"])
                sec_done = sum(
                    1 for item in data["items"]
                    if self.checks.get(item["id"], QCheckBox()).isChecked()
                )
                lbl.setText(f"{sec_done}/{sec_total}")

    def _reset(self):
        reply = QMessageBox.question(
            self, "초기화 확인",
            "모든 체크 항목을 초기화하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            for cb in self.checks.values():
                cb.setChecked(False)


# ── 메인 윈도우 ─────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏠  2026년 부동산 매수 도우미")
        self.setMinimumSize(820, 680)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # 헤더
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet(
            f"QFrame {{ background: qlineargradient("
            f"x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 {C['primary']}, stop:1 {C['secondary']}); }}"
        )
        hl = QVBoxLayout(header)
        hl.setContentsMargins(20, 8, 20, 8)
        hl.addWidget(make_label("🏠  2026년 부동산 매수 도우미", bold=True, size=14, color="white"))
        hl.addWidget(make_label(
            "2026년 기준  ·  지원금 확인  +  구비서류  +  임장 체크리스트",
            size=9, color="#B3D4F5"
        ))
        root.addWidget(header)

        # 탭
        tabs = QTabWidget()
        tabs.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
        tabs.setStyleSheet(
            "QTabWidget::pane { border:none; background:#F5F7FA; }"
            "QTabBar::tab { padding:10px 20px; font-size:10pt; }"
            f"QTabBar::tab:selected {{ color:{C['secondary']}; border-bottom:3px solid {C['secondary']}; background:#EEF4FB; }}"
            "QTabBar::tab:!selected { color:#777; background:#F5F7FA; }"
        )

        # 각 탭에 여백 컨테이너 추가
        def wrap_tab(widget):
            w = QWidget()
            l = QVBoxLayout(w)
            l.setContentsMargins(12, 10, 12, 10)
            l.addWidget(widget)
            return w

        tabs.addTab(wrap_tab(SupportTab()), "🏛️  지역별 집수리 지원금")
        tabs.addTab(wrap_tab(DocsTab()),    "📋  구비 서류")
        tabs.addTab(wrap_tab(ChecklistTab()), "✅  임장 체크리스트")
        root.addWidget(tabs)

        # 상태바
        self.statusBar().showMessage(
            "※ 지원사업은 예산 소진 시 조기 마감됩니다. 반드시 해당 기관에서 최신 공고를 확인하세요.  |  2026년 기준"
        )


# ── 진입점 ────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 전역 폰트
    font = QFont("Malgun Gothic", 10)
    app.setFont(font)

    # 밝은 팔레트
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#F5F7FA"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#1A1A1A"))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
