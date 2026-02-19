import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QCheckBox, QProgressBar, 
                             QLabel, QScrollArea, QPushButton)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices

class RealEstateChecklistApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2026 부동산 완벽 체크리스트 가이드 (스마트 링크 연동)")
        self.setGeometry(100, 100, 1100, 700)
        
        self.all_checkboxes = []
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 상단 타이틀
        title_label = QLabel("📋 2026 부동산 완벽 체크리스트 (스마트 링크 연동)")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(10)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # 1. 자금 조달 및 세금 탭
        tab1_items = [
            ("[대출] 스트레스 DSR 3단계 한도 축소분 사전 은행 상담 완료", None),
            ("[청약] 2026.09.30. 이전 청약예금·부금 -> 주택청약종합저축 전환 검토", "https://www.applyhome.co.kr/"),
            ("[자금] 투기과열/토지거래허가구역 자금조달계획서 작성 (가상자산/사업자대출 소명)", "https://rt.molit.go.kr/"),
            ("[세금] 2026.05.09. 다주택자 양도세 중과 배제 종료 전 매도/잔금 전략 수립", None),
            ("[세금] 기준시가 12억 초과 & 전세금 12억 초과 고가 주택 간주임대료 과세 산정", "https://www.hometax.go.kr/"),
            ("[세금] 특수관계인(가족) 저가 양도 시 차액 3억/30% 증여취득세 리스크 주의", None)
        ]
        tabs.addTab(self.create_scrollable_tab(tab1_items), "자금 조달 및 세금")

        # 2. 계약 전후 및 사기 예방 탭
        tab2_items = [
            ("[사전검토] 등기부등본(권리관계/갑을구) 최신본 열람 및 말소기준권리 확인", "http://www.iros.go.kr/"),
            ("[사전검토] 건축물대장(위반건축물 여부) 및 토지대장 열람", "https://www.gov.kr/"),
            ("[사전검토] 토지이용계획확인원(건폐율·용적률, 개발제한구역 등 규제) 확인", "http://www.eum.go.kr/"),
            ("[계약금] 실거래 신고용 계약금 입금 내역(매수인 명의 계좌이체) 필수 확보", None),
            ("[사기예방] 신탁 사기 방지용 공인중개사의 신탁원부 의무 제시 요구", "http://www.iros.go.kr/"),
            ("[사기예방] 임대인 동의 하에 국세/지방세 납세증명서(완납) 직접 수령 및 확인", "https://www.gov.kr/"),
            ("[사기예방] 보증금 보증보험 가입 가능 여부(HUG 등) 사전 조회", "https://www.khug.or.kr/"),
            ("[행정] 계약 체결일로부터 30일 이내 관할 시·군·구청에 부동산거래신고 완료", "https://rt.molit.go.kr/"),
            ("[행정] 전입신고 및 확정일자 잔금일 당일 즉시 처리 완료", "https://www.gov.kr/")
        ]
        tabs.addTab(self.create_scrollable_tab(tab2_items), "계약 및 사기예방")

        # 3. 주택 및 상가/오피스텔 탭
        tab3_items = [
            ("[주택] 점유자(임차인) 전입신고·확정일자 열람 및 임대차 만료일 파악", "https://www.gov.kr/"),
            ("[주택] 재건축·재개발 등 정비사업 정보시스템 편입 여부 조회", "https://cleanup.seoul.go.kr/"),
            ("[상가/오피스텔] 주택(1~3%)과 다른 4.6% 취득세율 자금 계획 반영", "https://www.wetax.go.kr/"),
            ("[오피스텔] 주택임대관리업 등록 의무(자기 100호/위탁 300호 임대 시) 확인", None),
            ("[오피스텔] 주거용 사용 시 주택수 산입에 따른 다주택 세금 영향 검토", None)
        ]
        tabs.addTab(self.create_scrollable_tab(tab3_items), "주택 및 상가")

        # 4. 토지 및 경매 특수 탭
        tab4_items = [
            ("[토지] 농업경영계획서 제출 및 농지취득자격증명(농취증) 발급 가능 여부 타진", "https://www.gov.kr/"),
            ("[토지] 경계복원측량 실시 (인접 토지 침범 및 20년 점유취득시효 분쟁 예방)", "https://baro.lx.or.kr/"),
            ("[임야] 산지정보시스템 산지구분도 확인 (경사도 25도 이상 개발행위허가 제한)", "https://www.forestland.go.kr/"),
            ("[경매-권리분석] 대법원 법원경매정보 매각물건명세서 및 감정평가서 열람", "https://www.courtauction.go.kr/"),
            ("[공매-권리분석] 한국자산관리공사 온비드 공매 물건 조회 및 입찰", "https://www.onbid.co.kr/"),
            ("[경매-유치권] 허위 유치권자 미퇴거 시 경매방해죄 형사 고발 및 인도명령 신청", None),
            ("[경매-대항력] 대항력 갖춘 임차인 미배당 보증금 전액 인수 리스크 대비", None)
        ]
        tabs.addTab(self.create_scrollable_tab(tab4_items), "토지 및 경매")

        # 5. 지원사업 혜택 탭
        tab5_items = [
            ("[전국] 그린리모델링(창호교체/단열 등) 에너지공단 대출 이자 지원 사업 신청", "https://www.greenremodeling.or.kr/"),
            ("[전국] 마이홈 포털에서 거주지별 청년/신혼부부 주거 지원 사업(임대료 등) 확인", "https://www.myhome.go.kr/"),
            ("[농어촌] 귀농귀촌종합센터 농촌 주택 개량 저금리 융자 및 빈집 철거 보조금 상담", "https://www.returnfarm.com/"),
            ("[지자체] 관할 구청/시청 홈페이지 노후 주택 집수리 보조금 공고 확인", None)
        ]
        tabs.addTab(self.create_scrollable_tab(tab5_items), "지원사업 혜택")

        # 하단 프로그레스 바
        main_layout.addSpacing(10)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.progress_bar)

    def create_scrollable_tab(self, items):
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        for text, url in items:
            row_layout = QHBoxLayout()
            
            # 1. 체크박스 생성 (텍스트 없음)
            cb = QCheckBox()
            cb.stateChanged.connect(self.update_progress)
            self.all_checkboxes.append(cb)
            row_layout.addWidget(cb)
            
            # 2. 텍스트 라벨 생성 (자동 줄바꿈 적용)
            text_label = QLabel(text)
            text_label.setFont(QFont("Arial", 10))
            text_label.setWordWrap(True) # 라벨에는 완벽하게 작동합니다!
            
            # 텍스트를 클릭해도 체크박스가 선택/해제되도록 설정
            text_label.mousePressEvent = lambda event, checkbox=cb: checkbox.toggle()
            row_layout.addWidget(text_label, stretch=1)
            
            # 3. 사이트 이동 버튼 생성 (URL이 있는 경우에만)
            if url:
                btn = QPushButton("사이트 이동 🌐")
                btn.setFixedWidth(110)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda checked, link=url: QDesktopServices.openUrl(QUrl(link)))
                row_layout.addWidget(btn)
                
            layout.addLayout(row_layout)
            
        layout.addStretch()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        
        return scroll_area

    def update_progress(self):
        total_items = len(self.all_checkboxes)
        checked_items = sum(1 for cb in self.all_checkboxes if cb.isChecked())
        
        if total_items > 0:
            progress_percentage = int((checked_items / total_items) * 100)
            self.progress_bar.setValue(progress_percentage)
            
            if progress_percentage == 100:
                self.progress_bar.setFormat("2026년 부동산 매수 전 모든 확인을 완료했습니다! 🎉")
            else:
                self.progress_bar.setFormat(f"전체 진척도: {progress_percentage}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RealEstateChecklistApp()
    ex.show()
    sys.exit(app.exec())