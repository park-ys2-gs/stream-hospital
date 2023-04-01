import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import streamlit as st
import time


@st.cache_data
def load_data(file_name):
    data = pd.read_csv(file_name)
    return data


def clear_text():
    st.session_state["a"] = ""

df = load_data("hospital_info.csv")

st.title('병원정보서비스')

t_input = st.text_input(label="병원명 바로 검색", key="a")

search_df = df.query('병원이름.str.contains("{}")'.format(t_input))  ## df.query(조건식 문자열)
if t_input:
    st.write('검색된 데이터 전체 {}건 (최대10건만 출력됨)'.format(len(search_df)))
    st.table(search_df.head(10))
    st.button("clear text input", on_click=clear_text)

# 사이드바에 select box를 활용하여 조건을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('병원 정보 확인🏥')

# 여러개 선택할 수 있을 때는 multiselect를 이용하실 수 있습니다. (return : list)
sido_list = df['시도'].unique().tolist()
select_multi_sido = st.sidebar.multiselect('확인하고자 하는 시도를 선택해 주세요. 복수선택가능', sido_list)
sido_df = df[df['시도'].isin(select_multi_sido)]  # 선택된 시도

if select_multi_sido:  # 시도 선택된 "상태"
    sggu_list = sido_df['시군구'].unique().tolist()  # 선택된 시도의 시군구 리스트
    select_multi_sggu = st.sidebar.multiselect('확인하고자 하는 시군구를 선택해 주세요. 복수선택가능', sggu_list)
    sggu_df = sido_df[sido_df['시군구'].isin(select_multi_sggu)]  # 선택된 시군구 df

    if select_multi_sggu:  # 시군구 선택된 "상태"
        emdong_list = sggu_df['읍면동명'].unique().tolist()  # 선택된 시군구의 읍면동 리스트
        select_multi_emdong = st.sidebar.multiselect('확인하고자 하는 읍면동을 선택해 주세요. 복수선택가능', emdong_list)
        emdong_df = sggu_df[sggu_df['읍면동명'].isin(select_multi_emdong)]  # 선택된 읍면동 df

        if select_multi_emdong:  # 읍면동 선택된 "상태"
            st.write('선택된 데이터 전체 {}건 (최대10건만 출력됨)'.format(len(emdong_df)))
            st.table(emdong_df)  # 선택된 읍면동 df 출력
        else:  # 읍면동 선택 안 된 "상태" -> 선택된 시군구 df 출력
            st.write('선택된 데이터 전체 {}건 (최대10건만 출력됨)'.format(len(sggu_df)))
            st.table(sggu_df)
    else:  # 시군구 선택 안 된 "상태" -> 선택된 시도 df 출력
        st.write('선택된 데이터 전체 {}건 (최대10건만 출력됨)'.format(len(sido_df)))
        st.table(sido_df)
else:  # 시도 선택 안 된 "상태" -> 전체 df 출력
    st.write('데이터 전체 {}건 (최대10건만 출력됨)'.format(len(df)))
    st.table(df.head(10))
