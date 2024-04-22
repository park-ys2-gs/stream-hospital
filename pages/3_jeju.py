import pandas as pd
import streamlit as st
import pickle
import os

st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Jeju", page_icon="🍊")
st.title('제주도 추천 서비스🍊')

path = os.path.dirname(__file__)
with open (path+'/indices_1.pkl', 'rb') as f:
    indices_1 = pickle.load(f)
with open (path+'/cosine_sim_1.pkl', 'rb') as f:
    cosine_sim_1 = pickle.load(f)
with open(path+'/final_downtown_review.pkl', 'rb') as f:
    final_downtown_review = pickle.load(f)


def get_recommendations(rest, cosine_sim=cosine_sim_1):
    # 식당명 통해 전체 데이터 기준 그 식당 index값을 얻기
    idx = indices_1[rest]  # indices_1 필요

    # 코사인 유사도 매트릭스에서 idx에 해당하는 데이터 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))  # cosine_sim_1 필요

    # 코사인 유사도 기준 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 자기 자신 제외 5개의 추천 식당 슬라이싱
    sim_scores = sim_scores[1:6]  # [0:6]이면 본인을 포함하기에 X

    # 추천 식당명 5개 인덱스 정보 추출
    rest_indices = [i[0] for i in sim_scores]

    # 추천 식당과 유사도 반환
    recommendations = [(final_downtown_review['식당명'].iloc[i], "{:.3f}".format(sim_scores[j][1])) for j, i in enumerate(rest_indices)]
    # final_downtown_review 필요

    return recommendations

# 사용자로부터 식당명 입력받기
# user_input = input("식당명을 입력하세요: ")
user_input = st.text_input("식당명을 입력하세요: ")
if user_input:
    recommendations = get_recommendations(user_input)
    for rec in recommendations:
        # print("추천 식당:", rec[0], '&', "유사도:", rec[1])
        st.write("추천 식당:", rec[0], '&', "유사도:", rec[1])

# 갑순이네