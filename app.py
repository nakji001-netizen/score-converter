import streamlit as st
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(page_title="내신 등급 상호 환산기", page_icon="🔄", layout="centered")

# 2. 모바일 반응형 CSS 주입 (제목 크기 자동 조절)
st.markdown("""
    <style>
    .responsive-title {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    @media (max-width: 768px) {
        .responsive-title {
            font-size: 1.6rem;
        }
    }
    </style>
    <div class="responsive-title">🔄 내신 등급 상호 환산기 (5등급 ↔ 9등급)</div>
""", unsafe_allow_html=True)

st.write("2028학년도 대입제도 개편 대비 내신 등급 변환 가이드의 데이터 표본을 바탕으로 등급을 상호 환산합니다.")

# 3. 문서 기반 기준점 데이터 설정
# 5등급 기준점: 1.00부터 5.00까지 0.05 단위 (총 81개 구간)
grade_5_points = np.round(np.linspace(1.00, 5.00, 81), 2)

# 9등급 평균 데이터: 대진대학교 입학팀 자료에서 추출 (총 81개 구간)
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

# 4. 상호 변환을 위한 탭 구성
tab1, tab2 = st.tabs(["📊 5등급 ➔ 9등급 변환", "🔍 9등급 ➔ 5등급 역산"])

# --- 탭 1: 5등급에서 9등급으로 변환 ---
with tab1:
    st.subheader("5등급제 ➔ 9등급제")
    
    input_grade_5 = st.number_input(
        "5등급제 내신 평균을 입력하세요 (1.00 ~ 5.00):", 
        min_value=1.00, max_value=5.00, value=2.50, step=0.01, key="g5_input"
    )
    
    if st.button("9등급 평균으로 변환", key="btn_to_9"):
        # 선형 보간: 5등급 -> 9등급
        converted_9_grade = np.interp(input_grade_5, grade_5_points, grade_9_avg_points)
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("입력한 5등급 평균", f"{input_grade_5:.2f} 등급")
        col2.metric("최종 9등급 환산 평균", f"{converted_9_grade:.2f} 등급")

# --- 탭 2: 9등급에서 5등급으로 역산 ---
with tab2:
    st.subheader("9등급제 ➔ 5등급제")
    
    # 1.00 ~ 9.00까지 입력 가능하도록 허용
    input_grade_9 = st.number_input(
        "9등급제 내신 평균을 입력하세요 (1.00 ~ 9.00):", 
        min_value=1.00, max_value=9.00, value=4.11, step=0.01, key="g9_input"
    )
    
    if st.button("5등급 평균으로 역산", key="btn_to_5"):
        # 역방향 선형 보간: 9등급 -> 5등급 (x와 y 배열 위치를 바꿈)
        converted_5_grade = np.interp(input_grade_9, grade_9_avg_points, grade_5_points)
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("입력한 9등급 평균", f"{input_grade_9:.2f} 등급")
        col2.metric("최종 5등급 환산 평균", f"{converted_5_grade:.2f} 등급")
        
        # 데이터 범위를 벗어나는 입력에 대한 예외 처리 안내
        if input_grade_9 < 1.18 or input_grade_9 > 8.74:
            st.warning("⚠️ 입력하신 점수가 표본 데이터 범위(1.18 ~ 8.74)를 벗어나, 양 끝단의 최대/최소 환산값(1.00 또는 5.00)으로 고정 처리되었습니다.")

# 5. 하단 출처 및 안내 표시
st.write("---")
st.caption("※ 본 환산 결과는 대진대학교 입학팀의 2025학년도 전국 23개 고교 고3 표본(6,087명) 원점수 기반 중간석차 백분위 데이터를 바탕으로 산출되었습니다.")
