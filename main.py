import pandas as pd
import streamlit as st

st.title('기넥신 성장 금액 계산기📈')
num1 = st.number_input("1주일 진료일수", value=4)
num2 = st.number_input("하루 기넥신 처방 환자", value=0)
num3 = st.radio("처방 용량(mg)", options=[40, 80, 240])
num4 = st.number_input("의료인 평균 처방 일수", value=60)

num3_dic = {40: 127, 80: 185, 240: 550}
result = num1*num2*num3_dic[num3]*num4*4

# 입력받은 숫자들을 출력한다.
st.write(f"1주일에 진료일수가 ({num1})일인 의료인께 하루에 환자 ({num2})명에게 기넥신 ({num3})mg을 처방해주신다면")
st.write(f"월 기넥신 월 성장 금액은 ({result:,})원.")
