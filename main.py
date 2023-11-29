# https://github.com/streamlit/streamlit/issues/4195#issuecomment-998909519
# Simpler, effective method to clear value of text_input #4195
import streamlit as st
import pickle
import numpy as np
import sklearn


st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="CHDM LNG", page_icon="🧮")
st.title('CHDM LNG 사용량 계산기📈')
st.sidebar.title("예측값 입력✅")
num1 = st.sidebar.number_input("var1", value=4)
num2 = st.sidebar.number_input("var2", value=0)
num3 = st.sidebar.number_input("var3", value=4)
num4 = st.sidebar.slider('var4', 10, 100, 50)

predict_button = st.sidebar.button("예측하기(버튼뺄수있음)", type="primary")
if predict_button:
    with open('saved_model', 'rb') as f:
        mod = pickle.load(f)
    predict = mod.predict(np.array([[num1, num2, num3, num4]]))
    st.write(f"Prediction of LNG usages:{1}")

