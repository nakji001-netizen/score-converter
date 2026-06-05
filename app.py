# --- 탭 2: 9등급에서 5등급으로 역산 ---
with tab2:
    st.subheader("9등급제 ➔ 5등급제")
    # 입력 범위를 1.00 ~ 9.00으로 수정
    input_grade_9 = st.number_input(
        "9등급제 내신 평균을 입력하세요 (1.00 ~ 9.00):", 
        min_value=1.00, max_value=9.00, value=4.11, step=0.01, key="g9_input"
    )
    
    if st.button("5등급 평균으로 역산", key="btn_to_5"):
        # np.interp는 입력값이 1.18 미만이면 1.00을, 8.74 초과면 5.00을 자동으로 반환합니다.
        converted_5_grade = np.interp(input_grade_9, grade_9_avg_points, grade_5_points)
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("입력한 9등급 평균", f"{input_grade_9:.2f} 등급")
        col2.metric("최종 5등급 환산 평균", f"{converted_5_grade:.2f} 등급")
        
        # 데이터 범위를 벗어났을 때 안내 문구 추가
        if input_grade_9 < 1.18 or input_grade_9 > 8.74:
            st.warning("⚠️ 입력하신 점수가 표본 데이터 범위(1.18 ~ 8.74)를 벗어나, 양 끝단의 최대/최소 환산값(1.00 또는 5.00)으로 고정 처리되었습니다.")
