import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import streamlit as st


@st.cache_data
def load_data(file_name):
    data = pd.read_csv(file_name)
    return data


df = load_data("hospital_info.csv")

st.title('병원정보서비스')
# 사이드바에 select box를 활용하여 조건을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('병원 정보 확인🏥')

# 여러개 선택할 수 있을 때는 multiselect를 이용하실 수 있습니다
# return : list
sido_list = df['시도'].unique().tolist()
select_multi_sido = st.sidebar.multiselect('확인하고자 하는 시도를 선택해 주세요. 복수선택가능', sido_list)
sido_df = df[df['시도'].isin(select_multi_sido)]

sggu_df = sido_df
sggu_list = sido_df['시군구'].unique().tolist()
if select_multi_sido:
    select_multi_sggu = st.sidebar.multiselect('확인하고자 하는 시군구를 선택해 주세요. 복수선택가능', sggu_list)
    sggu_df = sido_df[sido_df['시군구'].isin(select_multi_sggu)]
    if select_multi_sggu:
        st.table(sggu_df)
    else:  # 시군구 선택 안 된 상태
        st.table(sido_df)
else:  # 시도 선택 안 된 상태
    st.write('전체 데이터 {}건 중 최대 10건 출력'.format(3))
    st.table(df.head(10))