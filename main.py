# https://github.com/streamlit/streamlit/issues/4195#issuecomment-998909519
# Simpler, effective method to clear value of text_input #4195
import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd
import numpy as np
import sklearn
import shap
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)



@st.cache
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="CHDM LNG", page_icon="🧮")
st.title('CHDM LNG 사용량 계산기📈')
st.sidebar.title("예측값 입력✅")
num1 = st.sidebar.number_input("var1", value=4)
num2 = st.sidebar.number_input("var2", value=0)
num3 = st.sidebar.number_input("var3", value=4)
num4 = st.sidebar.slider('var4', 10, 100, 50)

predict_button = st.sidebar.button("예측하기(버튼뺄수있음)", type="primary")
if predict_button:
    plt.switch_backend("Agg")

    # a classic housing price dataset
    X, y = shap.datasets.california(n_points=1000)

    X100 = shap.utils.sample(X, 100)  # 100 instances for use as the background distribution
    with open('saved_model', 'rb') as f:
        mod = pickle.load(f)
    # LinearExplainer 사용
    explainer = shap.LinearExplainer(mod, X100)
    shap_values = explainer.shap_values(X100)

    # Plotly Express를 사용하여 인터랙티브한 플롯 생성
    fig = shap.summary_plot(shap_values, X100, plot_type="bar")
    st.pyplot(fig)


    # prediction = mod.predict(np.array([[num1, num2, num3, num4]]))
    # st.subheader('Results')
    # st.write("Prediction: ", round(prediction[0], 2))
    #
    # X = np.array([[num1, num2, num3, num4]])
    # explainer = shap.Explainer(mod.predict, X)
    # shap_values = explainer(X)
    # fig, ax = plt.subplots()
    # shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    # shap_plot = st.pyplot(fig)
    #
    # # Streamlit에 플롯 렌더링
    # st.write("SHAP Values Summary Plot")
    # st.pyplot(shap_plot)

    # explainer = shap.Explainer(f)
    # X = np.array([[num1, num2, num3, num4]])
    # shap_values = explainer.shap_values(X)
    # # shap force plot 표시
    # st.subheader('Interpretation Plot')
    # df = pd.DataFrame(X, columns=['Column1', 'Column2', 'Column3', 'Column4'])
    # st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], df.iloc[0,:]))

    # ===
    # a classic housing price dataset
    # X, y = shap.datasets.california(n_points=1000)
    # X100 = shap.utils.sample(X, 100)  # 100 instances for use as the background distribution
    # # a simple linear model
    # model = sklearn.linear_model.LinearRegression()
    # model.fit(X, y)