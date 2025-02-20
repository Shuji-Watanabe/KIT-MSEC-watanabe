import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import japanize_matplotlib
import lib.DataLoad as dl

# サイドバーを初期状態で表示する
st.set_page_config(initial_sidebar_state="expanded")


title_text="散布図行列"
#-------------title begin-----------------------------------------------------
st.title(title_text)
#-------------title end-------------------------------------------------------

#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
"""ここでは，データから散布図行列を作成します．"""
#-------------header end-------------------------------------------------------

##------- 共通:カレントディレクトリ情報の取得 Begin -------
if "location_str" in st.session_state:
    location_str = st.session_state.location_str
else :
    from lib import FileProcessing as fp
    location_str = fp.location()
    st.session_state.location_str = location_str
if location_str == "streamlit_Community_Cloud":
    #これはプログラムのある位置が変更されたときに毎回変える
    tmp_cd_path = "2024年度数理工セミナー_展示用" 
else :
    tmp_cd_path = ""
###------- 共通:カレントディレクトリ情報の取得 End   -------

##------  共通：データの取得 Begin ------------------------------
tmp_sidebar_text  = f"{title_text}のオプション"
tmp_data_path     = "sample_datas"
tmp_data_encoding = 'shift_jis'
tmp_data_dict     = { "擬似データ１":"sampledata01.csv"
                     ,"擬似データ２":"sampledata02.csv"}   

##  自作関数
read_data_df = dl.data_load_form(sidebar_text=tmp_sidebar_text
                                , cd_path=tmp_cd_path
                                , data_path= tmp_data_path
                                , data_dict = tmp_data_dict)
##------  共通：データの取得 End   ------------------------------

if not 'filename' in st.session_state:
    st.sidebar.divider()
#===============================================================================================    
# 分析データ列の選択
keys_list = list(read_data_df.keys())
input_col = st.columns([1,1])
with input_col[0]:
    index_str = st.multiselect("データの選択",keys_list  ,key="mselect 02")
    if not index_str:
        """"""
        st.error("データを選択してください")
        st.stop()
with input_col[1]:
    data_df = read_data_df[index_str]
    data_len = data_df.shape[0]
    st.write("")
    st.dataframe(data_df
                    , use_container_width=True
                    , height=200)
st.success(f'準備完了', icon="✅") 
#===============================================================================================




#-------------subheader begin----------------------------------------------
st.subheader(f"Step２: 散布図（散布図行列）の作成", divider="green")
#-------------subheader end------------------------------------------------
if st.button("散布図の作成",key="button 01"):
    with st.spinner('作成中'):
        fig = sns.pairplot(data = data_df)
        st.pyplot(fig)


st.page_link("00_Data_Analysis_Apps.py", label="Home", icon="🏠")