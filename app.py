import streamlit as st
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="내신 등급 변환기 (공식 표본 기반)", page_icon="📈")

# --- 모바일 반응형 CSS 주입 ---
st.markdown("""
    <style>
    /* 기본 타이틀 스타일 (PC 등 큰 화면) */
    .responsive-title {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    /* 모바일 화면 (화면 너비 768px 이하) 스케일링 */
    @media (max-width: 768px) {
        .responsive-title {
            font-size: 1.6rem; /* 모바일에서는 글자 크기를 축소 */
        }
    }
    </style>
    <div class="responsive-title">📈 5등급 ➔ 9등급 평균 환산기</div>
""", unsafe_allow_html=True)

st.write("2028학년도 대입제도 개편 대비 내신 등급 변환 가이드의 데이터 표본을 바탕으로 9등급 평균을 환산합니다.")

# 1. 문서 기반 기준점 데이터 설정 (1.00 ~ 5.00까지 0.05 단위, 총 81개 구간)
grade_5_points = np.round(np.linspace(1.00, 5.00, 81), 2)

# 대진대학교 문서 내 '9등급(평균)' 데이터
grade_9_avg_points = [
    1.18, 1.36, 1.51, 1.63, 1.73, 1.85, 1.95, 2.05, 2.14, 2.25,
    2.34, 2.42, 2.48, 2.61, 2.69, 2.79, 2.82, 2.97, 3.06, 3.15,
    3.21, 3.33, 3.40, 3.53, 3.60, 3.68, 3.77, 3.86, 3.97, 4.03,
    4.11, 4.20, 4.27, 4.38, 4.45, 4.54, 4.62, 4.71, 4.78, 4.86,
    4.94, 5.04, 5.14, 5.21, 5.30, 5.37, 5.46, 5.52, 5.63, 5.70,
    5.80, 5.84, 5.96, 6.05, 6.11, 6.20, 6.27, 6.37, 6.48, 6.56,
    6.65, 6.74, 6.84, 6.91, 7.01, 7.10, 7.20, 7.31, 7.38, 7.42,
    7.51, 7.60, 7.75, 7.90, 7.96, 8.07, 8.14, 8.25, 8.49, 8.64,
    8.74
]

# 2. 사용자 입력 UI
input_grade = st.number_input(
    "학생의 5등급제 내신 평균을 입력하세요 (1.00 ~ 5.00):", 
    min_value=1.00, 
    max_value=5.00, 
    value=2.50, 
    step=0.01
)

if st.button("9등급 평균으로 변환하기"):
    # 3. 문서 데이터 기반 선형 보간법 적용
    converted_9_grade = np.interp(input_grade, grade_5_points, grade_9_avg_points)
    
    # 4. 결과 출력
    st.divider()
    st.subheader("💡 환산 결과")
    
    col1, col2 = st.columns(2)
    col1.metric("입력한 5등급 평균", f"{input_grade:.2f} 등급")
    col2.metric("최종 9등급 환산 평균", f"{converted_9_grade:.2f} 등급")
    
    st.caption("※ 본 환산 결과는 대진대학교 입학팀의 전국 23개 고교 고3 표본(6,087명) 데이터를 바탕으로 산출되었습니다.")
