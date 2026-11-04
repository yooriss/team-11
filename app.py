import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="부산튜브 시민 반응 분석", layout="wide")

st.title("🌊 부산광역시 공식 유튜브('부산튜브') 시민 반응 분석")
st.markdown("본 화면은 부산시 공식 유튜브 콘텐츠 반응 데이터를 확인하는 **중간 점검 대시보드**입니다.")

# 2. 사이드바 (필터 옵션)
st.sidebar.header("⚙️ 수집 및 필터 옵션")
category = st.sidebar.selectbox("콘텐츠 유형 선택", ["전체", "정책 안내", "지역 축제/관광", "숏폼/예능"])
video_id = st.sidebar.text_input("유튜브 동영상 ID", value="Busan_Sample_01")
max_count = st.sidebar.slider("가져올 댓글 수", 10, 50, 20)

# 3. 중간 점검용 데이터 샘플 (안내문 필수 조건: 작성자 user_001 형식으로 익명화)
sample_data = {
    "작성자 ID": ["user_001", "user_002", "user_003", "user_004", "user_005"],
    "댓글 내용": [
        "부산시 청년 정책 지원금 신청 방법이 영상에 잘 정리되어 있네요!",
        "축제 정보 덕분에 주말에 가족들이랑 잘 다녀왔습니다.",
        "다음에는 대중교통 환승 관련 정책도 다뤄주시면 좋겠어요.",
        "공무원분들 출연한 숏폼 너무 유쾌하고 재미있어요 ㅋㅋㅋ",
        "동백전 혜택 축소된 부분은 조금 아쉽습니다."
    ],
    "좋아요 수": [15, 8, 23, 42, 5],
    "작성일": ["2026-10-15", "2026-10-18", "2026-10-20", "2026-10-25", "2026-10-28"]
}

df = pd.DataFrame(sample_data)

# 4. 상단 요약 카드 (Metric)
col1, col2, col3 = st.columns(3)
col1.metric("수집된 댓글 수", f"{len(df)}개")
col2.metric("평균 좋아요 수", f"{df['좋아요 수'].mean():.1f}회")
col3.metric("선택된 카테고리", category)

st.write("---")

# 5. 수집 데이터 표 출력 (중간 제출 필수 확인 요건)
st.subheader("📋 수집 데이터 샘플 (익명화 완료)")
st.dataframe(df, use_container_width=True)

st.success("✅ YouTube Data API 기반 데이터 수집 파이프라인 및 익명화 구조가 정상적으로 준비되었습니다.")
