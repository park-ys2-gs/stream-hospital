import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import streamlit as st


@st.cache_data
def load_data(file_name):
    data = pd.read_csv(file_name)
    return data

st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Hospital Info Search Service", page_icon="📋")
st.title('병원 개폐업정보 서비스📋')

all_df = load_data("hospital_info.csv")
st.write("월 별 개폐업 정보")

# 사이드바에 select box를 활용하여 조건을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('기준년월 선택📍')
ym_list = all_df['기준년월'].unique().tolist()
select_ym = st.sidebar.selectbox('확인하고자 하는 기준년월을 선택해 주세요.', ym_list)

ym_df = all_df[all_df['기준년월'].isin([select_ym])]  # 선택된 기준년월
st.write('{}년 {}월 기준 개폐업 데이터: 총 {}건 (최대 10건만 출력)'.format(str(select_ym)[:4], str(select_ym)[4:], len(ym_df)))
st.table(ym_df.head(10))
st.write("""
---------
<시별통계>
인천|3건|2건|자세히
속초|1건|1건|자세히
<급별통계>
상급|2건|1건|자세히
중급|0건|0건|자세히
""")