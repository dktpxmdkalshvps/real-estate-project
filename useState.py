import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QCheckBox, QProgressBar, 
                             QLabel, QScrollArea, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices

# --- [1] 데이터 정의 ---
REGION_DATA = {
    "서울": [
        {"name": "안심 집수리 보조사업", "target": "10년 이상 저층주택", "amount": "공사비 80%, 최대 1,200만원", "url": "https://jibsuri.seoul.go.kr"},
        {"name": "안심 집수리 융자 지원", "target": "사용승인 후 20년 이상", "amount": "최소 1,000만원~최대 6,000만원 (연 0.7%)", "url": "https://jibsuri.seoul.go.kr"}
    ],
    "경기": [
        {"name": "소규모 노후주택 집수리", "target": "사용승인 20년 이상", "amount": "최대 1,600만원 (도 30% + 시군 70%)", "url": "https://www.gg.go.kr/"}
    ],
    "농어촌": [
        {"name": "농촌 빈집 철거 보조금", "target": "1년 이상 방치 빈집", "amount": "일반 최대 300만원 / 슬레이트 400만원", "url": "https://www.gov.kr"},
        {"name": "농촌 주택 개량 저금리 융자", "target": "농어촌 지역 주택", "amount": "신축 최대 2.5억 / 개축 1.5억", "url": "https://www.returnfarm.com"}
    ]
}

CHECKLIST_DATA = {
    "자금조달 및 세금": [
        ("[대출] 스트레스 DSR 3단계 대출 한도 축소분 확인", True, None),
        ("[청약] 청약예금·부금 -> 주택청약종합저축 전환 검토", False, "https://www.applyhome.co.kr/"),
        ("[세금] 다주택자 양도세 중과 배제 종료(26.05.09) 대비", True, None)
    ],
    "계약 및 사기예방": [
        ("[서류] 등기부등본(갑·을구) 최신본 및 말소기준권리 확인", True, "http://www.iros.go.kr/"),
        ("[서류] 건축물대장 및 토지대장·토지이용계획 열람", True, "https://www.gov.kr/"),
        ("[사기예방] 공인중개사 신탁원부 의무 제시 요구", True, "http://www.iros.go.kr/"),
        ("[행정] 30일 이내 부동산거래신고 및 잔금일 전입신고", True, "https://rt.molit.go.kr/")
    ],
    "현장 및 건물임장": [
        ("[건물] 외벽·지붕 균열·누수 및 반지하 침수 흔적 확인", True, None),
        ("[건물] 점유자(임차인) 전입신고·확정일자 등 실제 거주 파악", True, "https://www.gov.kr/"),
        ("[토지] 도로 접도 조건 (건축허가 4m 이상) 및 경계 확인", True, None)
    ]
}

class RealEstateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏠 2026 부동산 스마트 도우미")
        self.setGeometry(100, 100, 900, 750)
        # 전체 앱 배경색을 밝은 회색으로 설정하여 모던한 느낌 부여
        self.setStyleSheet("QMainWindow { background-color: #f3f4f6; }")
        
        self.all_checkboxes = []
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 상단 헤더
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #1e3a8a; border-radius: 10px;")
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("🏠 2026 부동산 스마트 도우미")
        title.setFont(QFont("Malgun Gothic", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        
        subtitle = QLabel("최신 규제 반영 · 지원금 확인 + URL 연동 임장 체크리스트")
        subtitle.setFont(QFont("Malgun Gothic", 10))
        subtitle.setStyleSheet("color: #bfdbfe;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_frame)
        main_layout.addSpacing(10)

        # 탭 생성
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { background: #e5e7eb; padding: 10px 20px; font-weight: bold; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 2px;}
            QTabBar::tab:selected { background: #ffffff; color: #1d4ed8; border-bottom: 3px solid #1d4ed8;}
            QTabWidget::pane { border: 1px solid #d1d5db; background: #ffffff; border-radius: 8px; }
        """)
        main_layout.addWidget(self.tabs)

        # 1. 지원금 탭 세팅
        self.setup_support_tab()
        
        # 2. 체크리스트 탭 세팅
        self.setup_checklist_tab()

    # ==========================================
    # 탭 1: 지역별 지원금 화면 구성
    # ==========================================
    def setup_support_tab(self):
        self.support_tab = QWidget()
        layout = QVBoxLayout(self.support_tab)
        
        # 안내 문구
        info_label = QLabel("⚠️ 지원사업은 예산 소진 시 조기 마감됩니다. 지자체 최신 공고를 확인하세요.")
        info_label.setStyleSheet("background-color: #fefce8; color: #a16207; padding: 10px; border-radius: 5px; border: 1px solid #fef08a;")
        info_label.setFont(QFont("Malgun Gothic", 9, QFont.Weight.Bold))
        layout.addWidget(info_label)

        # 지역 선택 버튼 영역
        btn_layout = QHBoxLayout()
        self.region_btns = {}
        for region in REGION_DATA.keys():
            btn = QPushButton(f"📍 {region}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background-color: white; border: 2px solid #d1d5db; border-radius: 15px; padding: 8px 15px; font-weight: bold; color: #4b5563; }
                QPushButton:hover { border: 2px solid #60a5fa; color: #1d4ed8; }
            """)
            btn.clicked.connect(lambda checked, r=region: self.load_region_data(r))
            self.region_btns[region] = btn
            btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # 카드들이 들어갈 스크롤 영역
        self.support_scroll = QScrollArea()
        self.support_scroll.setWidgetResizable(True)
        self.support_scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.support_scroll.setWidget(self.cards_widget)
        
        layout.addWidget(self.support_scroll)
        self.tabs.addTab(self.support_tab, "🏛️ 지역별 지원금 혜택")
        
        # 초기 데이터 로드 (서울)
        self.load_region_data("서울")

    def load_region_data(self, region):
        # 버튼 색상 업데이트 (선택된 버튼 강조)
        for r, btn in self.region_btns.items():
            if r == region:
                btn.setStyleSheet("QPushButton { background-color: #1d4ed8; color: white; border-radius: 15px; padding: 8px 15px; font-weight: bold; }")
            else:
                btn.setStyleSheet("QPushButton { background-color: white; border: 2px solid #d1d5db; border-radius: 15px; padding: 8px 15px; font-weight: bold; color: #4b5563; }")

        # 기존 카드들 삭제
        for i in reversed(range(self.cards_layout.count())): 
            self.cards_layout.itemAt(i).widget().setParent(None)

        # 선택된 지역의 데이터로 카드 생성
        for prog in REGION_DATA[region]:
            card = QFrame()
            card.setStyleSheet("QFrame { background-color: white; border: 2px solid #bfdbfe; border-radius: 10px; margin-bottom: 10px; }")
            card_layout = QVBoxLayout(card)
            
            # 타이틀
            title = QLabel(prog['name'])
            title.setFont(QFont("Malgun Gothic", 12, QFont.Weight.Bold))
            title.setStyleSheet("color: #1e40af; border: none; margin-top: 5px;")
            card_layout.addWidget(title)
            
            # 내용
            content = QLabel(f"<b>대상:</b> {prog['target']}<br><br><b>지원액:</b> <span style='color:#b91c1c;'>{prog['amount']}</span>")
            content.setFont(QFont("Malgun Gothic", 10))
            content.setStyleSheet("border: none; color: #374151;")
            card_layout.addWidget(content)
            
            # 사이트 이동 버튼
            link_btn = QPushButton("사이트 이동 🌐")
            link_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            link_btn.setStyleSheet("""
                QPushButton { background-color: #eff6ff; border: 1px solid #93c5fd; color: #1d4ed8; border-radius: 12px; padding: 6px 15px; font-weight: bold; margin-bottom: 5px;}
                QPushButton:hover { background-color: #dbeafe; }
            """)
            link_btn.setFixedWidth(120)
            link_btn.clicked.connect(lambda checked, url=prog['url']: QDesktopServices.openUrl(QUrl(url)))
            
            btn_layout = QHBoxLayout()
            btn_layout.addWidget(link_btn, alignment=Qt.AlignmentFlag.AlignRight)
            card_layout.addLayout(btn_layout)
            
            self.cards_layout.addWidget(card)

    # ==========================================
    # 탭 2: 체크리스트 화면 구성
    # ==========================================
    def setup_checklist_tab(self):
        checklist_tab = QWidget()
        layout = QVBoxLayout(checklist_tab)

        # 스크롤 영역 설정
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # 데이터 파싱 및 UI 생성
        for category, items in CHECKLIST_DATA.items():
            # 카테고리 헤더
            cat_label = QLabel(category)
            cat_label.setFont(QFont("Malgun Gothic", 12, QFont.Weight.Bold))
            cat_label.setStyleSheet("background-color: #f3f4f6; color: #374151; padding: 8px; border-radius: 5px; margin-top: 10px;")
            content_layout.addWidget(cat_label)
            
            # 항목 리스트
            for text, is_critical, url in items:
                row_layout = QHBoxLayout()
                
                # 1. 체크박스
                cb = QCheckBox()
                cb.setStyleSheet("QCheckBox::indicator { width: 18px; height: 18px; }")
                cb.stateChanged.connect(self.update_progress)
                self.all_checkboxes.append(cb)
                row_layout.addWidget(cb)
                
                # 2. 텍스트 라벨 (자동 줄바꿈 적용)
                text_label = QLabel(text)
                text_label.setFont(QFont("Malgun Gothic", 10))
                text_label.setWordWrap(True)
                text_label.mousePressEvent = lambda event, checkbox=cb: checkbox.toggle()
                row_layout.addWidget(text_label, stretch=1)
                
                # 필수 태그
                if is_critical:
                    crit_label = QLabel("필수")
                    crit_label.setStyleSheet("background-color: #fee2e2; color: #b91c1c; font-weight: bold; border-radius: 4px; padding: 2px 5px;")
                    crit_label.setFont(QFont("Malgun Gothic", 8))
                    row_layout.addWidget(crit_label)
                
                # 3. 사이트 이동 버튼
                if url:
                    btn = QPushButton("이동 🌐")
                    btn.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn.setStyleSheet("QPushButton { background-color: white; border: 1px solid #d1d5db; border-radius: 10px; padding: 4px 10px; color: #4b5563; } QPushButton:hover { background-color: #f3f4f6; }")
                    btn.clicked.connect(lambda checked, link=url: QDesktopServices.openUrl(QUrl(link)))
                    row_layout.addWidget(btn)
                    
                content_layout.addLayout(row_layout)
                
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        # 프로그레스 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar { border: 1px solid #d1d5db; border-radius: 10px; text-align: center; height: 25px; font-weight: bold;}
            QProgressBar::chunk { background-color: #3b82f6; border-radius: 10px; }
        """)
        layout.addWidget(self.progress_bar)
        
        self.tabs.addTab(checklist_tab, "✅ 임장 체크리스트")

    def update_progress(self):
        total = len(self.all_checkboxes)
        checked = sum(1 for cb in self.all_checkboxes if cb.isChecked())
        if total > 0:
            percentage = int((checked / total) * 100)
            self.progress_bar.setValue(percentage)
            if percentage == 100:
                self.progress_bar.setFormat("임장 및 계약 전 확인 완료! 🎉")
            else:
                self.progress_bar.setFormat(f"전체 진척도: {percentage}% ({checked}/{total})")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RealEstateApp()
    ex.show()
    sys.exit(app.exec())