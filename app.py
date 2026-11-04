st.subheader("📊 수집 데이터 목록 (작성자 익명화 완료)")

# 자바스크립트 컴포넌트를 쓰지 않고 HTML로 직접 변환하여 브라우저 로딩 에러 원천 차단
html_table = df_show.to_html(index=False, classes="custom-table")
st.markdown(
    f"""
    <style>
        .custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        .custom-table th {{
            background-color: #f0f2f6;
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        .custom-table td {{
            padding: 8px 10px;
            border: 1px solid #eee;
        }}
        .custom-table tr:nth-child(even) {{
            background-color: #fafafa;
        }}
    </style>
    {html_table}
    """,
    unsafe_allow_html=True
)
