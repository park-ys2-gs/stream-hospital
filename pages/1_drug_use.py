import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import time



@st.cache_data
def load_data(file_name):
    data = pd.read_csv(file_name, encoding='cp949')
    return data


st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="msup User Info Service", page_icon="💊")
st.title('의약품사용정보조회서비스💊')

all_df = load_data("drug_use.csv")
all_df['diagYm'] = pd.to_datetime(all_df['diagYm'], format='%Y%m')

gnl_list = all_df['gnlNmCd'].unique().tolist()
select_multi_gnl = st.sidebar.multiselect('확인하고자 하는 gnl_nm_cd를 선택해 주세요. 복수선택가능', gnl_list)

sido_list = all_df['sidoCdNm'].unique().tolist()
select_multi_sido = st.sidebar.multiselect('확인하고자 하는 sido_cd_nm을 선택해 주세요. 복수선택가능', sido_list)

sggu_list = all_df['sgguCdNm'].unique().tolist()
select_multi_sggu = st.sidebar.multiselect('확인하고자 하는 sggu_cd_nm을 선택해 주세요. 복수선택가능', sggu_list)

cl_list = all_df['clCdNm'].unique().tolist()
select_multi_cl = st.sidebar.multiselect('확인하고자 하는 cl_cd_nm을 선택해 주세요. 복수선택가능', cl_list)

genre = st.radio(
    "확인하고자 하는 값을 선택해주세요.",
    ('msupUseAmt', 'totUseQty'))

df = all_df[all_df['gnlNmCd'].isin(select_multi_gnl)]
df = df[df['sidoCdNm'].isin(select_multi_sido)]
df = df[df['sgguCdNm'].isin(select_multi_sggu)]
df = df[df['clCdNm'].isin(select_multi_cl)]

# Create distplot with custom bin_size
fig = px.line(df, x='diagYm', y=genre, color='insupTpCd', markers=True)
fig.update_layout(
    title = '성분별의료기관종별사용량목록조회',
    xaxis_tickformat = '%B<br>%Y')
fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = df['diagYm'],
        ticktext = df['diagYm'].dt.strftime('%Y-%m')
    )
)
# Plot!
st.plotly_chart(fig, use_container_width=True)
if select_multi_cl == ['상급종합병원']:
    st.write("📋 '서울시' '광진구' '상급종합병원' 리스트: ['건국대학교병원']")
    convert_csv = df.to_csv().encode('cp949')
    st.download_button(
        label="📥 파일 다운로드",
        data=convert_csv,
        file_name='drug_amt_use.csv',
        mime='text/csv',
        key=None)
st.markdown("<<<개선사항>>>  \n"
            "1. 세부 선택이 없었을 경우 sum 그래프 보여주는 기능 추가.  \n"
            "ex) gnl_nm_cd를 선택하고 sido_cd_nm선택전일때 sido구분 없이 해당 gnl_nm_cd의 합을 보여줌.  \n"
            "2. 기간 선택 기능")
