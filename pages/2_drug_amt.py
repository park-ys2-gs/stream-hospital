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


st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Drug Amt Criteria Info Service", page_icon="💰")
st.title('약가기준정보조회서비스💰')

df = load_data("drug_amt.csv")
st.write('KIMS와 차별점이 있을까?')
st.dataframe(df.head(10))

convert_csv = df.to_csv().encode('cp949')
st.download_button(
    label="파일 다운로드",
    data=convert_csv,
    file_name='drug_amt_criteria.csv',
    mime='text/csv',
    key=None)
