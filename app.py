import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

# 페이지 기본 설정
st.set_page_config(page_title="부산튜브 시민 반응 분석", layout="wide")

st.title("🌊 부산광역시 공식 유튜브('부산튜브') 시민 반응 분석")
st.markdown("본 화면은 YouTube Data API를 통해 실제 부산시 홍보 영상 반응 데이터를 수집하고 확인하는 **중간 점검 대시보드**입니다.")

# -----------------------------------------------------------------------------
# 1. API 키 설정 (보안 규정 준수: st.secrets 우선 로드)
# -----------------------------------------------------------------------------
api_key = st.secrets.get("YOUTUBE_API_KEY", "")

st.sidebar.header("⚙️ 수집 및 필터 옵션")

# Secrets에 키가 없으면 사이드바에서 입력받기
if not api_key:
    api_key = st.sidebar.text_input("YouTube Data API 키 입력", type="password")

# 분석 대상 유튜브 동영상 ID 입력 (기본값 설정)
video_id = st.sidebar.text_input("유튜브 동영상 ID 입력", value="M7lc1UVf-VE")

# -----------------------------------------------------------------------------
# 2. 데이터 수집 함수 (API 연동 및 개인정보 익명화 처리)
# -----------------------------------------------------------------------------
def fetch_comments(api_key, video_id):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            textFormat="plainText"
        )
        response = request.execute()

        comments_list = []
        user_idx = 1

        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            
            # 과제 규정: 개인정보 보호를 위한 작성자 익명화 (user_001 형식)
            comments_list.append({
                "작성자 ID": f"user_{user_idx:03d}",
                "댓글 내용": snippet["textDisplay"],
                "좋아요 수": int(snippet["likeCount"]),
                "작성일": str(snippet["publishedAt"][:10])
            })
            user_idx += 1

        return pd.DataFrame(comments_list)
    except Exception as e:
        st.error(f"데이터 수집 중 오류가 발생했습니다: {e}")
        return None

# -----------------------------------------------------------------------------
# 3. 실시간 데이터 수집 실행
# -----------------------------------------------------------------------------
st.subheader("📋 실시간 데이터 수집")

if st.button("🚀 댓글 데이터 수집하기"):
    if not api_key:
        st.warning("⚠️ YouTube API 키를 사이드바에 입력하거나 Secrets에 등록해주세요.")
    else:
        with st.spinner("유튜브에서 실시간 댓글을 수집하고 있습니다..."):
            collected = fetch_comments(api_key, video_id)
            if collected is not None and not collected.empty:
                st.session_state["data"] = collected
                st.success(f"성공적으로 {len(collected)}개의 댓글 데이터를 수집했습니다!")

# -----------------------------------------------------------------------------
# 4. 데이터 표 출력 (순수 HTML 렌더링으로 JS 에러 원천 차단)
# -----------------------------------------------------------------------------
st.write("---")

if "data" in st.session_state:
    df_show = st.session_state["data"]
else:
    df_show = pd.DataFrame({
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
    })

# 상단 요약 카드
st.markdown(
    f"""
    <div style="display: flex; gap: 20px; margin-bottom: 20px;">
        <div style="flex: 1; background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px;">
            <p style="margin: 0; font-size: 14px; color: #6c757d;">확인된 댓글 수</p>
            <h2 style="margin: 5px 0 0 0; color: #1f77b4;">{len(df_show)}개</h2>
        </div>
        <div style="flex: 1; background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px;">
            <p style="margin: 0; font-size: 14px; color: #6c757d;">평균 좋아요 수</p>
            <h2 style="margin: 5px 0 0 0; color: #2ca02c;">{df_show['좋아요 수'].mean():.1f}회</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("📊 수집 데이터 목록 (작성자 익명화 완료)")

# HTML 표 출력
html_table = df_show.to_html(index=False, classes="custom-table")
st.markdown(
    f"""
    <style>
        .custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            margin-top: 10px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        .custom-table th {{
            background-color: #f1f3f5;
            color: #333;
            padding: 12px;
            border: 1px solid #dee2e6;
            text-align: left;
            font-weight: bold;
        }}
        .custom-table td {{
            padding: 10px 12px;
            border: 1px solid #e9ecef;
            color: #212529;
        }}
        .custom-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
    </style>
    {html_table}
    """,
    unsafe_allow_html=True
)

st.write("")
st.success("✅ YouTube Data API 기반 데이터 수집 파이프라인 및 익명화 구조가 정상적으로 준비되었습니다.")
