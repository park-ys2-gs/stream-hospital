import pandas as pd
import streamlit as st


@st.cache_data
def load_data(file_name):
    data = pd.read_csv(file_name, encoding='cp949')
    return data


def file_download(df, file_tag, key=None):
    convert_csv = df.to_csv().encode('cp949')
    st.download_button(
        label="전체 파일 다운로드",
        data=convert_csv,
        file_name='hospital_info_{}.csv'.format(file_tag),
        mime='text/csv',
        key=key)


st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Hospital Info Search Service", page_icon="🏥")
st.title('병원 정보 검색 서비스🏥')

all_df = load_data("hospital_info.csv")
all_df.sort_values(by=['estbDd'], axis=0)
t_input = st.text_input(label="병원명 검색", key="a")  # session state key = 'a'
search_df = all_df.query('yadmNm.str.contains("{}")'.format(t_input))  ## df.query(조건식 문자열)

# 여러개 선택할 수 있을 때는 multiselect를 이용하실 수 있습니다. (return : list)
clcd_list = all_df['clCdNm'].unique().tolist()
select_multi_clcd = st.sidebar.multiselect('확인하고자 하는 clcd를 선택해 주세요. 복수선택가능', clcd_list)

# 사이드바에 select box를 활용하여 조건을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('지역 선택📍')
sido_list = all_df['sidoCdNm'].unique().tolist()
select_multi_sido = st.sidebar.multiselect('확인하고자 하는 시도를 선택해 주세요. 복수선택가능', sido_list)
sido_df = all_df[all_df['sidoCdNm'].isin(select_multi_sido)]  # 선택된 sidoCdNm

# all_df, search_df, sido_df
if select_multi_clcd:
    all_df = all_df[all_df['clCdNm'].isin(select_multi_clcd)]
    search_df = search_df[search_df['clCdNm'].isin(select_multi_clcd)]
    sido_df = sido_df[sido_df['clCdNm'].isin(select_multi_clcd)]

if select_multi_sido:  # sidoCdNm 선택된 "상태"
    sggu_list = sido_df['sgguCdNm'].unique().tolist()  # 선택된 sidoCdNm의 sgguCdNm 리스트
    select_multi_sggu = st.sidebar.multiselect('확인하고자 하는 시군구를 선택해 주세요. 복수선택가능', sggu_list)
    sggu_df = sido_df[sido_df['sgguCdNm'].isin(select_multi_sggu)]  # 선택된 sgguCdNm df
    if select_multi_clcd:
        sggu_df = sggu_df[sggu_df['clCdNm'].isin(select_multi_clcd)]

    if select_multi_sggu:  # sgguCdNm 선택된 "상태"
        emdong_list = sggu_df['emdongNm'].unique().tolist()  # 선택된 sgguCdNm의 읍면동 리스트
        select_multi_emdong = st.sidebar.multiselect('확인하고자 하는 읍면동을 선택해 주세요. 복수선택가능', emdong_list)
        emdong_df = sggu_df[sggu_df['emdongNm'].isin(select_multi_emdong)]  # 선택된 읍면동 df
        if select_multi_clcd:
            emdong_df = emdong_df[emdong_df['clCdNm'].isin(select_multi_clcd)]

        if select_multi_emdong:  # 읍면동 선택된 "상태"
            if st.session_state["a"] == "":
                st.write('사이드바 조건으로 선택된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(len(emdong_df)))
                st.dataframe(emdong_df.head(10))  # 선택된 읍면동 df 출력
                file_download(df=emdong_df, file_tag=None)
            else:
                emdong_df2 = emdong_df.query('yadmNm.str.contains("{}")'.format(t_input))
                st.write('사이드바 조건 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(t_input, len(emdong_df2)))
                st.dataframe(emdong_df2.head(10))  # 선택된 읍면동+병원명조건 df 출력
                file_download(df=emdong_df2, file_tag=t_input)
        else:  # 읍면동 선택 안 된 "상태" -> 선택된 sgguCdNm df 출력
            if st.session_state["a"] == "":
                st.write('사이드바 조건으로 선택된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(len(sggu_df)))
                st.dataframe(sggu_df.head(10))  # 선택된 sgguCdNm df 출력
                file_download(df=sggu_df, file_tag=None)
            else:
                sggu_df2 = sggu_df.query('yadmNm.str.contains("{}")'.format(t_input))
                st.write('사이드바 조건 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(t_input, len(sggu_df2)))
                st.dataframe(sggu_df2.head(10))  # 선택된 sgguCdNm+병원명조건 df 출력
                file_download(df=sggu_df2, file_tag=t_input)
    else:  # sgguCdNm 선택 안 된 "상태" -> 선택된 sidoCdNm df 출력
        if st.session_state["a"] == "":
            st.write('사이드바 조건으로 선택된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(len(sido_df)))
            st.dataframe(sido_df.head(10))  # 선택된 sidoCdNm df 출력
            file_download(df=sido_df, file_tag=None)
        else:
            sido_df2 = sido_df.query('yadmNm.str.contains("{}")'.format(t_input))
            st.write('사이드바 조건 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(t_input, len(sido_df2)))
            st.dataframe(sido_df2.head(10))  # 선택된 sidoCdNm+병원명조건 df 출력
            file_download(df=sido_df2, file_tag=t_input)
else:  # sidoCdNm 선택 안 된 "상태" -> 전체 df 출력
    if st.session_state["a"] == "":
        st.write('전국 데이터: 총 {}건 (최대 10건만 출력됨)'.format(len(all_df)))
        st.dataframe(all_df.head(10))
    else:
        st.write('전국 데이터 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력)'.format(t_input, len(search_df)))
        st.dataframe(search_df.head(10))
        file_download(df=search_df, file_tag=t_input)