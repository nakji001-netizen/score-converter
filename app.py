import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="내신 등급 변환기", page_icon="📈")

st.title("📈 5등급 ➔ 9등급 평균 환산기")
st.write("5등급제 내신 평균을 누적 백분율로 추정한 뒤, 9등급제 평균으로 변환합니다.")

# 1. 기준 백분율 설정 (x: 등급, y: 백분율)
# 5등급 기준점 (1.0~5.0)
grade_5_points = [1.0, 2.0, 3.0, 4.0, 5.0]
percentile_5_points = [0.0, 10.0, 34.0, 66.0, 100.0] 

# 9등급 기준점 (백분율을 바탕으로 등급을 역산하기 위해 x, y 위치 변경)
percentile_9_points = [0.0, 4.0, 11.0, 23.0, 40.0, 60.0, 77.0, 89.0, 96.0, 100.0]
grade_9_points = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 9.0] 

# 2. 사용자 입력 UI
input_grade = st.number_input(
    "학생의 5등급제 내신 평균을 입력하세요 (1.00 ~ 5.00):", 
    min_value=1.00, 
    max_value=5.00, 
    value=2.50, 
    step=0.01
)

if st.button("변환하기"):
    # 3. 선형 보간법(Linear Interpolation)을 통한 계산
    # Step A: 5등급 평균 -> 추정 백분율 계산
    estimated_percentile = np.interp(input_grade, grade_5_points, percentile_5_points)
    
    # Step B: 추정 백분율 -> 9등급 평균 계산
    converted_9_grade = np.interp(estimated_percentile, percentile_9_points, grade_9_points)
    
    # 4. 결과 출력
    st.divider()
    st.subheader("💡 환산 결과")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("입력한 5등급 평균", f"{input_grade:.2f} 등급")
    col2.metric("추정 누적 백분율", f"상위 {estimated_percentile:.1f} %")
    col3.metric("최종 9등급 환산", f"{converted_9_grade:.2f} 등급")
    
    st.info("※ 본 결과는 각 등급 경계의 누적 백분율을 선형 보간하여 추정한 값이므로, 실제 원점수 기반 백분율과는 약간의 오차가 있을 수 있습니다.")