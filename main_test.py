import pandas as pd
import streamlit as st
import mysql.connector

st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Hospital Info Search Service", page_icon="🏥")

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query("SELECT * FROM hospital_info;")
table_colum_names = ['seq', 'ykiho', 'yadmNm', 'clCd', 'clCdNm', 'sidoCd', 'sidoCdNm', 'sgguCd', 'sgguCdNm',
'emdongNm', 'postNo', 'addr', 'telno', 'hospUrl', 'estbDd', 'drTotCnt', 'mdeptGdrCnt', 'mdeptIntnCnt',
'mdeptResdntCnt', 'mdeptSdrCnt', 'detyGdrCnt', 'detyIntnCnt', 'detyResdntCnt', 'detySdrCnt', 'cmdcGdrCnt',
'cmdcIntnCnt', 'cmdcResdntCnt', 'cmdcSdrCnt', 'pnursCnt', 'XPos', 'YPos', 'distance']
all_df = pd.DataFrame(rows, columns=table_colum_names)
all_df = all_df.sort_values(by=['estbDd'], ascending=False, axis=0)
all_df = all_df[['yadmNm', 'clCdNm', 'sidoCdNm', 'sgguCdNm',
'emdongNm', 'postNo', 'addr', 'telno', 'hospUrl', 'estbDd', 'drTotCnt', 'mdeptGdrCnt', 'mdeptIntnCnt',
'mdeptResdntCnt', 'mdeptSdrCnt', 'detyGdrCnt', 'detyIntnCnt', 'detyResdntCnt', 'detySdrCnt', 'cmdcGdrCnt',
'cmdcIntnCnt', 'cmdcResdntCnt', 'cmdcSdrCnt', 'pnursCnt']]


def file_download(df, file_tag, key=None):
    convert_csv = df.to_csv().encode('cp949')
    st.download_button(
        label="전체 파일 다운로드",
        data=convert_csv,
        file_name='hospital_info_{}.csv'.format(file_tag),
        mime='text/csv',
        key=key)


st.title('병원 정보 검색 서비스🏥')


t_input = st.text_input(label="병원명 검색", key="a")  # session state key = 'a'
search_df = all_df.query('yadmNm.str.contains("{}")'.format(t_input))  ## df.query(조건식 문자열)

# 여러개 선택할 수 있을 때는 multiselect를 이용하실 수 있습니다. (return : list)
clcd_list = all_df['clCdNm'].unique().tolist()
select_multi_clcd = st.sidebar.multiselect('확인하고자 하는 clcd를 선택해 주세요. 복수선택가능', clcd_list)

# 사이드바에 select box를 활용하여 조건을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('지역 선택📍')
sido_list = all_df['sidoCdNm'].unique().tolist()
select_multi_sido = st.sidebar.multiselect('확인하고자 하는 시도를 선택해 주세요. 복수선택가능', sido_list)
sido_df = all_df[all_df['sidoCdNm'].isin(select_multi_sido)]  # 선택된 시도

# all_df, search_df, sido_df
if select_multi_clcd:
    all_df = all_df[all_df['clCdNm'].isin(select_multi_clcd)]
    search_df = search_df[search_df['clCdNm'].isin(select_multi_clcd)]
    sido_df = sido_df[sido_df['clCdNm'].isin(select_multi_clcd)]

if select_multi_sido:  # 시도 선택된 "상태"
    sggu_list = sido_df['sgguCdNm'].unique().tolist()  # 선택된 시도의 시군구 리스트
    select_multi_sggu = st.sidebar.multiselect('확인하고자 하는 시군구를 선택해 주세요. 복수선택가능', sggu_list)
    sggu_df = sido_df[sido_df['sgguCdNm'].isin(select_multi_sggu)]  # 선택된 시군구 df
    if select_multi_clcd:
        sggu_df = sggu_df[sggu_df['clCdNm'].isin(select_multi_clcd)]

    if select_multi_sggu:  # 시군구 선택된 "상태"
        emdong_list = sggu_df['emdongNm'].unique().tolist()  # 선택된 시군구의 읍면동 리스트
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
        else:  # 읍면동 선택 안 된 "상태" -> 선택된 시군구 df 출력
            if st.session_state["a"] == "":
                st.write('사이드바 조건으로 선택된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(len(sggu_df)))
                st.dataframe(sggu_df.head(10))  # 선택된 시군구 df 출력
                file_download(df=sggu_df, file_tag=None)
            else:
                sggu_df2 = sggu_df.query('yadmNm.str.contains("{}")'.format(t_input))
                st.write('사이드바 조건 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(t_input, len(sggu_df2)))
                st.dataframe(sggu_df2.head(10))  # 선택된 시군구+병원명조건 df 출력
                file_download(df=sggu_df2, file_tag=t_input)
    else:  # 시군구 선택 안 된 "상태" -> 선택된 시도 df 출력
        if st.session_state["a"] == "":
            st.write('사이드바 조건으로 선택된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(len(sido_df)))
            st.dataframe(sido_df.head(10))  # 선택된 시도 df 출력
            file_download(df=sido_df, file_tag=None)
        else:
            sido_df2 = sido_df.query('yadmNm.str.contains("{}")'.format(t_input))
            st.write('사이드바 조건 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력됨)'.format(t_input, len(sido_df2)))
            st.dataframe(sido_df2.head(10))  # 선택된 시도+병원명조건 df 출력
            file_download(df=sido_df2, file_tag=t_input)
else:  # 시도 선택 안 된 "상태" -> 전체 df 출력
    if st.session_state["a"] == "":
        st.write('전국 데이터: 총 {}건 (최대 10건만 출력됨. 최근 개설일자 순.)'.format(len(all_df)))
        st.dataframe(all_df.head(10))
    else:
        st.write('전국 데이터 중 "{}"(으)로 검색된 데이터: 총 {}건 (최대 10건만 출력)'.format(t_input, len(search_df)))
        st.dataframe(search_df.head(10))
        file_download(df=search_df, file_tag=t_input)