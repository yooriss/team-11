import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

# 페이지 설정
st.set_page_config(page_title="부산튜브 시민 반응 분석", layout="wide")

st.title("🌊 부산광역시 공식 유튜브('부산튜브') 시민 반응 분석")
st.markdown("본 대시보드는 YouTube Data API를 통해 실제 콘텐츠 반응 데이터를 수집하고 확인하는 대시보드입니다.")

# -----------------------------------------------------------------------------
# 1. API 키 불러오기 (보안 규정 준수: Secrets 활용)
# -----------------------------------------------------------------------------
api_key = st.secrets.get("YOUTUBE_API_KEY", "")

# -----------------------------------------------------------------------------
# 2. 사이드바 (수집 옵션 설정)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ 수집 옵션 설정")

# Secrets에 키가 없을 때를 대비한 수동 입력창
if not api_key:
    api_key = st.sidebar.text_input("YouTube Data API 키 입력", type="password")

# 분석할 유튜브 영상 ID (기본값: 부산시 공식 유튜브 영상 예시)
# 유튜브 영상 주소가 https://www.youtube.com/watch?v=abcde 라면 ID는 'abcde' 입니다.
video_id = st.sidebar.text_input("유튜브 동영상 ID 입력", value="tXJ3sA0vF5I")
max_comments = st.sidebar.slider("수집할 댓글 수", min_value=10, max_value=100, value=20, step=10)

# -----------------------------------------------------------------------------
# 3. 유튜브 댓글 수집 함수 (API 연동 및 개인정보 익명화)
# -----------------------------------------------------------------------------
def fetch_comments(api_key, video_id, max_results):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_results, 100),
            textFormat="plainText"
        )
        response = request.execute()

        comments_list = []
        user_idx = 1

        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            
            # 과제 규정 준수: 작성자 개인정보 익명화 처리 (user_001 형식)
            comments_list.append({
                "작성자 ID": f"user_{user_idx:03d}",
                "댓글 내용": snippet["textDisplay"],
                "좋아요 수": snippet["likeCount"],
                "작성일": snippet["publishedAt"][:10]
            })
            user_idx += 1

        return pd.DataFrame(comments_list)

    except Exception as e:
        st.error(f"데이터 수집 중 오류가 발생했습니다: {e}")
        return None

# -----------------------------------------------------------------------------
# 4. 데이터 수집 실행 및 화면 표시
# -----------------------------------------------------------------------------
st.subheader("📋 데이터 수집 실행")

if st.button("🚀 댓글 데이터 수집하기"):
    if not api_key:
        st.warning("⚠️ YouTube API 키를 등록하거나 사이드바에 입력해주세요.")
    else:
        with st.spinner("유튜브에서 실시간 댓글을 수집하고 있습니다..."):
            df = fetch_comments(api_key, video_id, max_comments)
            
            if df is not None and not df.empty:
                st.session_state["collected_df"] = df
                st.success(f"성공적으로 {len(df)}개의 댓글 데이터를 수집했습니다!")

# 수집된 데이터가 있으면 화면에 표시 (중간 점검 필수 요건)
if "collected_df" in st.session_state:
    df_result = st.session_state["collected_df"]
    
    # 핵심 지표 표시
    col1, col2 = st.columns(2)
    col1.metric("총 수집 댓글 수", f"{len(df_result)}개")
    col2.metric("평균 좋아요 수", f"{df_result['좋아요 수'].mean():.1f}회")
    
    st.write("---")
    st.subheader("📊 수집된 댓글 데이터 목록 (익명화 완료)")
    st.table(df_result)
    
    # CSV 다운로드 버튼 제공
    csv_data = df_result.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="💾 수집 데이터 CSV 파일로 저장하기",
        data=csv_data,
        file_name="busan_youtube_comments.csv",
        mime="text/csv"
    )
