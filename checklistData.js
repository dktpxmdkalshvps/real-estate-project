import { useState } from "react";

const regionData = {
  서울: {
    programs: [
      {
        name: "안심 집수리 보조사업",
        target: "10년 이상 저층주택 (단독·다가구·다세대·연립)",
        who: "주거취약가구 (기초수급자·차상위·중증장애인·65세이상·다자녀·한부모·다문화), 반지하, 옥탑방, 주택성능개선지원구역(20년↑)",
        amount: "주거취약가구: 공사비 80%, 최대 1,200만원\n반지하: 공사비 50%, 최대 600만원\n옥탑·지원구역: 공사비 50%, 최대 1,200만원",
        works: "단열·방수·창호·설비, 침수·화재 안전시설, 편의시설(손잡이·단차제거)",
        note: "세입자 있는 경우 4년 임차료 동결 협약 조건. 에너지효율 자재 사용 시 추가 보조",
        apply: "주택 소재 자치구 담당부서",
        url: "https://jibsuri.seoul.go.kr",
        color: "blue",
      },
      {
        name: "안심 집수리 융자 지원",
        target: "사용승인 후 20년 이상 저층주택 (서울 전 지역)",
        who: "주택 소유자 (소득 제한 없음)",
        amount: "공사비 80% 이내, 최소 1,000만원~최대 6,000만원 / 연 0.7% 저리",
        works: "지붕·외벽·단열·창호·도배·장판·설비 등 전반",
        note: "2025년부터 이자지원사업은 신규 중단. 직접 융자 방식으로 전환",
        apply: "건축물 소재 관할 자치구 담당부서",
        url: "https://jibsuri.seoul.go.kr",
        color: "green",
      },
    ],
    contact: "서울주거포털 집수리닷컴 (jibsuri.seoul.go.kr) / 서울시 주택정책과 02-120",
    tip: "집수리닷컴에서 찾아가는 무료 상담 신청 가능 (공사업체 선정 전 상담 권장)",
  },
  경기: {
    programs: [
      {
        name: "소규모 노후주택 집수리 지원",
        target: "사용승인 20년 이상 단독·소규모 공동주택",
        who: "도내 전 지역 / 주거취약계층(기초수급·차상위·한부모가정)은 자부담 면제",
        amount: "최대 1,600만원 (도 30% + 시·군 70%)\n단독: 최대 1,200만원 / 공동(전유): 500만원 / 공동(공용): 1,600만원\n자부담 10% (취약계층 면제)",
        works: "지붕·외벽·단열·방수공사, 경관개선(담장·대문), 방범창 등 안전시설",
        note: "2025년 194개 지역 추진. 시·군별 일정 상이하므로 해당 시·군에 확인 필수",
        apply: "해당 시·군 도시재생·주택 담당부서",
        url: "https://www.gg.go.kr/contents/contents.do?ciIdx=987001",
        color: "purple",
      },
    ],
    contact: "경기도청 도시재생과 031-8008-3800 / 각 시·군 담당부서",
    tip: "'찾아가는 집수리 기술자문' 서비스 활용 가능 — 노후 주택 진단 및 시공방법 제시",
  },
  인천: {
    programs: [
      {
        name: "도시재생구역 노후주택 수리비 지원",
        target: "중구·동구 등 저층 주거지 재생사업 구역 내 20년 이상 노후 주택",
        who: "해당 구역 주택 소유자 (소득 기준 별도 확인)",
        amount: "최대 1,600만원 (공사비 80%)",
        works: "지붕·외벽·단열·창호·내부 마감 등",
        note: "구역 지정 여부 사전 확인 필수. 구역 외 주택은 주거급여 수선유지급여 활용",
        apply: "해당 자치구(중구·동구 등) 도시재생·주택과",
        url: "https://www.incheon.go.kr/housing",
        color: "orange",
      },
      {
        name: "주거급여 수선유지급여 (국가)",
        target: "전국 공통 — 주거급여 수급자 노후 주택",
        who: "기준 중위소득 48% 이하 가구 (인천 거주)",
        amount: "경보수 38만원 / 중보수 702만원 / 대보수 1,241만원",
        works: "도배·장판·지붕·창호·배관 등 필수 수선",
        note: "임차가구는 임대인 동의 필요. 연 1회 신청",
        apply: "주민센터 / 복지로(bokjiro.go.kr)",
        url: "https://www.incheon.go.kr/housing",
        color: "teal",
      },
    ],
    contact: "인천주거포털 (incheon.go.kr/housing) / 인천시 주택정책과 032-440-4749",
    tip: "재생사업 구역 여부는 인천시 도시재생지원센터 또는 해당 구청에 문의",
  },
  부산: {
    programs: [
      {
        name: "빈집 리모델링·정비 지원",
        target: "1년 이상 방치 빈집 / 구도심 빈집",
        who: "빈집 소유자",
        amount: "철거 보조 (슬레이트 지붕 포함 시 최대 400만원) / 리모델링 지원 별도",
        works: "빈집 철거, 창업공간·공유주택으로 개조 시 리모델링비 일부",
        note: "구·군별 사업 시기 상이. 빈집실태조사 후 우선 지원 대상 선정",
        apply: "부산시 각 구·군 건축·주택 담당부서",
        url: "https://www.busan.go.kr",
        color: "red",
      },
    ],
    contact: "부산시 도시주택국 051-888-3700",
    tip: "청년모두家(공공임대 임대료 지원), 청년 중개보수·이사비(최대 40만원) 지원도 별도 확인",
  },
  대구: {
    programs: [
      {
        name: "노후 공동주택 공용시설 수리비 지원 (북구)",
        target: "노후 공동주택 (아파트·연립·다세대)",
        who: "북구 소재 입주자대표회의",
        amount: "공용시설 수리비 70% 지원",
        works: "엘리베이터·주차장·복도·옥상 등 공용부분",
        note: "구별 별도 사업 존재. 중구·수성구 등 다른 구는 해당 구청에 확인",
        apply: "대구 북구청 도시재생·주택과",
        url: "https://www.daegu.go.kr",
        color: "indigo",
      },
    ],
    contact: "대구시 도시주택국 053-803-6500 / 해당 구청 주택과",
    tip: "도시재생뉴딜사업 구역 내 추가 지원 가능 — 해당 구청에 구역 포함 여부 확인",
  },
  농어촌: {
    programs: [
      {
        name: "농촌 빈집 철거 보조금",
        target: "1년 이상 방치된 농촌 빈집",
        who: "빈집 소유자",
        amount: "일반 최대 300만원 / 슬레이트(석면) 지붕 최대 400만원 (지자체별 상이)",
        works: "건물 철거, 석면·슬레이트 처리 포함",
        note: "지자체 지정 업체 사용 의무. 사전 신청 후 진행 필수",
        apply: "해당 읍·면·동 사무소 또는 시·군청 농촌개발과",
        url: "https://www.gov.kr",
        color: "yellow",
      },
      {
        name: "농촌 주택 개량 저금리 융자",
        target: "농어촌 지역 주택 (농촌지역 거주자)",
        who: "농촌 주택 소유자 또는 귀농·귀촌 예정자",
        amount: "신축: 최대 2억5천만원 / 증·개축: 최대 1억5천만원 / 연 1~2%대 저금리",
        works: "주택 신축·증축·개축·리모델링",
        note: "취득세 감면 혜택 ~2027년 12월 31일. 귀농귀촌종합센터 상담 권장",
        apply: "농림축산식품부 / 해당 지역 농협",
        url: "https://www.returnfarm.com",
        color: "green",
      },
      {
        name: "슬레이트 지붕 철거 지원 (전국)",
        target: "슬레이트(석면) 지붕 건물",
        who: "전국 슬레이트 지붕 건물 소유자 (소득 기준 우선순위 있음)",
        amount: "철거비 전액 지원 (지자체 예산 한도 내)",
        works: "석면 슬레이트 철거 및 안전 처리",
        note: "반드시 지자체 신청 후 지정 업체 사용. 자의적 철거 시 지원 불가",
        apply: "환경부 / 해당 시·군·구 환경부서",
        url: "https://www.me.go.kr",
        color: "gray",
      },
    ],
    contact: "귀농귀촌종합센터 1899-9097 / 각 읍·면·동 사무소",
    tip: "그린리모델링 이자지원(창호·단열 공사 이자 국가 지원)은 전국 공통 — 에너지공단(1588-6106) 문의",
  },
};

// 2026년 기준 종합 체크리스트 및 URL 연동 데이터 업데이트
const checklistData = {
  자금조달_세금: {
    icon: "💰",
    color: "blue",
    items: [
      { id: "f1", text: "스트레스 DSR 3단계 대출 한도 축소분 사전 은행 상담 완료", critical: true },
      { id: "f2", text: "청약예금·부금 -> 주택청약종합저축 전환 (2026.09.30 기한) 검토", critical: false, url: "https://www.applyhome.co.kr/" },
      { id: "f3", text: "자금조달계획서 작성 (가상자산/사업자대출 명확히 소명)", critical: true, url: "https://rt.molit.go.kr/" },
      { id: "f4", text: "다주택자 양도세 중과 배제 종료(2026.05.09) 전 매도/잔금 전략 수립", critical: true },
      { id: "f5", text: "고가 주택(12억 초과) 간주임대료 과세 금액 산정", critical: false, url: "https://www.hometax.go.kr/" },
      { id: "f6", text: "특수관계인(가족) 저가 양도 시 차액 3억/30% 증여취득세 리스크 대비", critical: true },
    ],
  },
  계약_사기예방: {
    icon: "🛡️",
    color: "red",
    items: [
      { id: "c1", text: "등기부등본(갑·을구) 최신본 열람 및 말소기준권리 확인", critical: true, url: "http://www.iros.go.kr/" },
      { id: "c2", text: "건축물대장(위반건축물) 및 토지대장·토지이용계획 열람 교차 검증", critical: true, url: "https://www.gov.kr/" },
      { id: "c3", text: "실거래 신고용 계약금 입금 내역(매수인 명의 계좌이체) 필수 확보", critical: true },
      { id: "c4", text: "신탁 사기 방지용 공인중개사의 신탁원부 의무 제시 요구", critical: true, url: "http://www.iros.go.kr/" },
      { id: "c5", text: "임대인 동의 하에 국세/지방세 완납 증명서 직접 수령 및 확인", critical: true, url: "https://www.gov.kr/" },
      { id: "c6", text: "계약 체결일로부터 30일 이내 관할 시·군·구청 부동산거래신고 완료", critical: true, url: "https://rt.molit.go.kr/" },
      { id: "c7", text: "전입신고 및 확정일자 잔금일 당일 즉시 처리", critical: true, url: "https://www.gov.kr/" },
      { id: "c8", text: "보증금 보증보험 가입 가능 여부(HUG 등) 사전 조회", critical: true, url: "https://www.khug.or.kr/" },
    ],
  },
  주택_상가특화: {
    icon: "🏢",
    color: "purple",
    items: [
      { id: "h1", text: "점유자(임차인) 전입신고·확정일자 열람 및 임대차 만료일 파악", critical: true, url: "https://www.gov.kr/" },
      { id: "h2", text: "재건축·재개발 등 정비사업 정보시스템 편입 여부 조회", critical: false, url: "https://cleanup.seoul.go.kr/" },
      { id: "h3", text: "상가/오피스텔 4.6% 취득세율에 맞춘 자금 계획 반영", critical: true, url: "https://www.wetax.go.kr/" },
      { id: "h4", text: "오피스텔 주택임대관리업 등록 의무(자기 100호/위탁 300호) 확인", critical: false },
      { id: "h5", text: "오피스텔 주거용 사용 시 주택수 산입 다주택 세금 영향 검토", critical: true },
      { id: "h6", text: "상가 사업용 부동산 부가가치세(VAT) 과세 여부 확인", critical: true },
    ],
  },
  토지_경매특화: {
    icon: "🌿",
    color: "green",
    items: [
      { id: "l1", text: "농업경영계획서 제출 및 농취증 발급 가능 여부 사전 타진", critical: true, url: "https://www.gov.kr/" },
      { id: "l2", text: "경계복원측량 실시 (인접 토지 침범 및 20년 점유취득시효 분쟁 예방)", critical: false, url: "https://baro.lx.or.kr/" },
      { id: "l3", text: "산지정보시스템 산지구분도 확인 (경사도 25도 이상 개발행위 제한)", critical: true, url: "https://www.forestland.go.kr/" },
      { id: "l4", text: "법원경매 매각물건명세서 및 감정평가서 꼼꼼히 열람", critical: true, url: "https://www.courtauction.go.kr/" },
      { id: "l5", text: "허위 유치권자 미퇴거 시 경매방해죄 고발 및 인도명령/명도소송 준비", critical: false },
      { id: "l6", text: "대항력 갖춘 선순위 임차인 미배당 보증금 전액 인수 리스크 대비", critical: true },
    ],
  },
  현장_건물임장: {
    icon: "🔍",
    color: "orange",
    items: [
      { id: "i1", text: "외벽·지붕 균열·누수·박리 흔적 직접 확인", critical: true },
      { id: "i2", text: "지하실·반지하 침수 흔적 (벽면 수위 자국) 점검", critical: true },
      { id: "i3", text: "도로 접도 조건 확인 (건축허가 가능 폭 4m 이상)", critical: true },
      { id: "i4", text: "배관·수도·보일러 노후 상태 (녹물·소음) 점검", critical: false },
      { id: "i5", text: "관리비, 공과금, 재산세 체납 여부 (관리사무소 문의)", critical: false },
      { id: "i6", text: "일조권·채광 및 인근 혐오시설, 소음원 확인", critical: false },
    ],
  },
};

const REGION_KEYS = Object.keys(regionData);
const SECTION_KEYS = Object.keys(checklistData);
const COLOR_MAP = {
  blue: { bg: "bg-blue-50", border: "border-blue-300", tag: "bg-blue-600", text: "text-blue-800", badge: "bg-blue-100 text-blue-700" },
  green: { bg: "bg-green-50", border: "border-green-300", tag: "bg-green-600", text: "text-green-800", badge: "bg-green-100 text-green-700" },
  purple: { bg: "bg-purple-50", border: "border-purple-300", tag: "bg-purple-600", text: "text-purple-800", badge: "bg-purple-100 text-purple-700" },
  orange: { bg: "bg-orange-50", border: "border-orange-300", tag: "bg-orange-600", text: "text-orange-800", badge: "bg-orange-100 text-orange-700" },
  red: { bg: "bg-red-50", border: "border-red-300", tag: "bg-red-600", text: "text-red-800", badge: "bg-red-100 text-red-700" },
  indigo: { bg: "bg-indigo-50", border: "border-indigo-300", tag: "bg-indigo-600", text: "text-indigo-800", badge: "bg-indigo-100 text-indigo-700" },
  yellow: { bg: "bg-yellow-50", border: "border-yellow-300", tag: "bg-yellow-600", text: "text-yellow-800", badge: "bg-yellow-100 text-yellow-700" },
  teal: { bg: "bg-teal-50", border: "border-teal-300", tag: "bg-teal-600", text: "text-teal-800", badge: "bg-teal-100 text-teal-700" },
  gray: { bg: "bg-gray-50", border: "border-gray-300", tag: "bg-gray-600", text: "text-gray-800", badge: "bg-gray-100 text-gray-700" },
};

export default function App() {
  const [tab, setTab] = useState("support");
  const [selectedRegion, setSelectedRegion] = useState("서울");
  const [checks, setChecks] = useState({});
  const [propertyType, setPropertyType] = useState("주택");

  const toggleCheck = (id) => setChecks((prev) => ({ ...prev, [id]: !prev[id] }));

  const totalItems = SECTION_KEYS.reduce((a, k) => a + checklistData[k].items.length, 0);
  const checkedItems = Object.values(checks).filter(Boolean).length;
  const progress = Math.round((checkedItems / totalItems) * 100);

  const criticalUnchecked = SECTION_KEYS.reduce((acc, k) => {
    return acc + checklistData[k].items.filter(i => i.critical && !checks[i.id]).length;
  }, 0);

  const region = regionData[selectedRegion];

  return (
    <div style={{ fontFamily: "'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif" }} className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900 to-blue-700 text-white px-6 py-5 shadow-md">
        <h1 className="text-2xl font-bold">🏠 2026 부동산 스마트 도우미</h1>
        <p className="text-blue-200 text-sm mt-1">최신 규제 반영 · 지원금 확인 + URL 연동 임장 체크리스트</p>
      </div>

      {/* Tab */}
      <div className="flex bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
        <button
          onClick={() => setTab("support")}
          className={`flex-1 py-3 text-sm font-bold transition-all ${tab === "support" ? "border-b-4 border-blue-600 text-blue-700 bg-blue-50" : "text-gray-500 hover:bg-gray-50"}`}
        >
          🏛️ 지역별 지원금 혜택
        </button>
        <button
          onClick={() => setTab("checklist")}
          className={`flex-1 py-3 text-sm font-bold transition-all ${tab === "checklist" ? "border-b-4 border-orange-500 text-orange-700 bg-orange-50" : "text-gray-500 hover:bg-gray-50"}`}
        >
          ✅ 계약/임장 체크리스트
        </button>
      </div>

      {/* Support Tab */}
      {tab === "support" && (
        <div className="p-4 max-w-2xl mx-auto pb-10">
          <p className="text-xs text-gray-500 mb-3 bg-yellow-50 border border-yellow-200 rounded p-2">
            ⚠️ 지원사업은 예산 소진 시 조기 마감됩니다. 반드시 해당 기관에 최신 공고를 직접 확인하세요.
          </p>

          <div className="flex flex-wrap gap-2 mb-4">
            {REGION_KEYS.map((r) => (
              <button
                key={r}
                onClick={() => setSelectedRegion(r)}
                className={`px-4 py-2 rounded-full text-sm font-bold border-2 transition-all ${
                  selectedRegion === r
                    ? "bg-blue-700 text-white border-blue-700 shadow"
                    : "bg-white text-gray-600 border-gray-300 hover:border-blue-400"
                }`}
              >
                {r === "농어촌" ? "🌾 " : "🏙️ "}{r}
              </button>
            ))}
          </div>

          <div className="space-y-4">
            {region.programs.map((prog, i) => {
              const c = COLOR_MAP[prog.color] || COLOR_MAP.blue;
              return (
                <div key={i} className={`rounded-xl border-2 ${c.border} ${c.bg} overflow-hidden shadow-sm`}>
                  <div className={`${c.tag} text-white px-4 py-2 flex items-center justify-between`}>
                    <span className="font-bold text-sm">{prog.name}</span>
                  </div>
                  <div className="p-4 space-y-3">
                    <div>
                      <span className="text-xs font-bold text-gray-500 uppercase">대상 주택</span>
                      <p className="text-sm text-gray-800 mt-0.5">{prog.target}</p>
                    </div>
                    <div>
                      <span className="text-xs font-bold text-gray-500 uppercase">신청 자격</span>
                      <p className="text-sm text-gray-800 mt-0.5">{prog.who}</p>
                    </div>
                    <div className={`rounded-lg p-3 ${c.badge.split(" ")[0].replace("text", "bg").replace("-700", "-100")} border ${c.border}`}>
                      <span className="text-xs font-bold text-gray-600">💰 지원 금액</span>
                      <p className="text-sm font-bold mt-0.5 whitespace-pre-line" style={{ color: "#1e3a5f" }}>{prog.amount}</p>
                    </div>
                    <div>
                      <span className="text-xs font-bold text-gray-500 uppercase">지원 공사 범위</span>
                      <p className="text-sm text-gray-800 mt-0.5">{prog.works}</p>
                    </div>
                    {prog.note && (
                      <div className="bg-amber-50 border border-amber-200 rounded-lg p-2">
                        <p className="text-xs text-amber-800">📌 {prog.note}</p>
                      </div>
                    )}
                    <div className="flex items-center justify-between pt-2">
                      <div>
                        <span className="text-xs font-bold text-gray-500">신청처: </span>
                        <span className="text-xs text-gray-700">{prog.apply}</span>
                      </div>
                      <a href={prog.url} target="_blank" rel="noreferrer"
                        className={`text-xs px-3 py-1.5 rounded-full font-bold text-white ${c.tag} hover:opacity-80 transition-opacity`}>
                        사이트 이동 →
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-4 bg-blue-50 border border-blue-200 rounded-xl p-4">
            <p className="text-sm font-bold text-blue-800 mb-1">📞 문의처</p>
            <p className="text-sm text-blue-900">{region.contact}</p>
          </div>
          {region.tip && (
            <div className="mt-3 bg-green-50 border border-green-200 rounded-xl p-4">
              <p className="text-sm font-bold text-green-800 mb-1">💡 활용 팁</p>
              <p className="text-sm text-green-900">{region.tip}</p>
            </div>
          )}
        </div>
      )}

      {/* Checklist Tab */}
      {tab === "checklist" && (
        <div className="p-4 max-w-2xl mx-auto pb-10">
          {/* Progress */}
          <div className="bg-white rounded-xl shadow-md p-4 mb-4 border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-gray-700">전체 진행률</span>
              <span className="font-bold text-blue-700 text-lg">{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
              <div
                className="h-3 rounded-full transition-all duration-500"
                style={{ width: `${progress}%`, background: progress === 100 ? "#22c55e" : progress > 60 ? "#3b82f6" : "#f59e0b" }}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">{checkedItems} / {totalItems} 개 완료</span>
              {criticalUnchecked > 0 ? (
                <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-md font-bold shadow-sm">
                  🚨 필수 {criticalUnchecked}개 미확인
                </span>
              ) : (
                <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-md font-bold shadow-sm">
                  ✅ 필수 확인 완료
                </span>
              )}
            </div>
          </div>

          {/* Property Type Filter */}
          <div className="flex gap-2 mb-4">
            {["주택", "토지", "상가·오피스텔"].map((t) => (
              <button
                key={t}
                onClick={() => setPropertyType(t)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 transition-all ${
                  propertyType === t ? "bg-orange-600 text-white border-orange-600 shadow" : "bg-white text-gray-600 border-gray-300 hover:bg-gray-50"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          {propertyType !== "주택" && (
            <div className="mb-4 bg-orange-50 border border-orange-200 rounded-lg p-3 text-xs text-orange-800 shadow-sm">
              {propertyType === "토지"
                ? "🌿 토지 거래 시 지목·농취증 발급 가능 여부·개발행위허가 및 맹지 여부를 중점적으로 확인하세요."
                : "🏪 상가·오피스텔은 취득세 4.6%·부가세 환급 가능 여부·주택수 산입 여부가 핵심입니다."}
            </div>
          )}

          {/* Sections List */}
          <div className="space-y-4">
            {SECTION_KEYS.map((sKey) => {
              const section = checklistData[sKey];
              const c = COLOR_MAP[section.color];
              const done = section.items.filter((i) => checks[i.id]).length;
              
              return (
                <div key={sKey} className={`bg-white rounded-xl border-2 ${c.border} shadow-sm overflow-hidden`}>
                  <div className={`${c.tag} text-white px-4 py-2.5 flex items-center justify-between`}>
                    <span className="font-bold text-sm tracking-wide">{section.icon} {sKey.replace("_", " / ")}</span>
                    <span className="text-xs bg-white bg-opacity-30 px-2 py-0.5 rounded-full font-bold">
                      {done} / {section.items.length}
                    </span>
                  </div>
                  <div className="divide-y divide-gray-100">
                    {section.items.map((item) => (
                      <div
                        key={item.id}
                        onClick={() => toggleCheck(item.id)}
                        className={`flex flex-col sm:flex-row sm:items-center gap-3 px-4 py-3 cursor-pointer hover:bg-gray-50 transition-colors ${
                          checks[item.id] ? "bg-gray-50 opacity-75" : ""
                        }`}
                      >
                        <div className="flex flex-1 items-start gap-3">
                          <div className={`mt-0.5 w-5 h-5 rounded-md border-2 flex-shrink-0 flex items-center justify-center transition-all ${
                            checks[item.id]
                              ? `${c.tag} border-transparent`
                              : "border-gray-300 bg-white"
                          }`}>
                            {checks[item.id] && <span className="text-white text-xs font-bold">✓</span>}
                          </div>
                          <div>
                            <span className={`text-sm leading-snug ${checks[item.id] ? "line-through text-gray-400" : "text-gray-800"}`}>
                              {item.text}
                            </span>
                            {item.critical && !checks[item.id] && (
                              <span className="inline-block ml-2 text-[10px] bg-red-100 text-red-600 px-1.5 py-0.5 rounded font-bold align-middle">필수</span>
                            )}
                          </div>
                        </div>
                        
                        {/* URL Button (Only renders if item.url exists) */}
                        {item.url && (
                          <div className="pl-8 sm:pl-0 shrink-0">
                            <a 
                              href={item.url} 
                              target="_blank" 
                              rel="noreferrer" 
                              onClick={(e) => e.stopPropagation()} 
                              className={`inline-block text-[11px] px-3 py-1.5 rounded-full font-bold transition-all border
                                ${checks[item.id] 
                                  ? "bg-gray-100 text-gray-500 border-gray-200 hover:bg-gray-200" 
                                  : "bg-blue-50 text-blue-600 border-blue-200 hover:bg-blue-100 hover:shadow-sm"
                                }`
                              }
                            >
                              사이트 이동 🌐
                            </a>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          <button
            onClick={() => {
               if(window.confirm('정말 모든 체크리스트를 초기화하시겠습니까?')) {
                 setChecks({});
               }
            }}
            className="w-full mt-6 py-3 rounded-xl border-2 border-gray-300 text-gray-600 text-sm font-bold hover:bg-gray-100 transition-all shadow-sm"
          >
            🔄 전체 진행 상황 초기화
          </button>
        </div>
      )}
    </div>
  );
}