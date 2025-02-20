import streamlit as st
import pandas as pd
import numpy as np
import lib.Functions as Functions


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

#-------------title begin-----------------------------------------------------
st.title("基本統計量")
#-------------title end-------------------------------------------------------

#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
#-------------header end-------------------------------------------------------
"""
このページでは，データの基本的な統計量を計算します．計算される量は次のとおりです．
"""
table_data = [ ['データ数','合計値'      ,'最大値','最小値']
              ,['分散   ','標準偏差'    ,'    ','     ']
              ,['中央値' ,'第一四分位数','第二四分位数','第三四分位数']
             ]
table_data_df = pd.DataFrame(table_data,columns=None)
st.dataframe(table_data_df
            ,use_container_width=True
            ,hide_index=True)
"""左側にあるサイドバーで分析に使用するデータを選択してください．選択肢は次の2つです．"""
leftside, rightside = st.columns([1,1])
with leftside:
    with st.expander(label="**分析体験でもデータ**"):
        """事前に用意されたデータを使用し，このアプリで何ができるのか体験することができます．"""
with rightside:
    with st.expander(label="**ユーザーデータ**"):
        """
        ユーザーが用意したデータに基づき，データ分析を行います．分析に使用するCSVファイルをアップロードしてください．
        CSVファイルは次の形式に従って作成してください．
        - データの方向は列（縦に測定値が並びます）
        - 1行目：データ名
        - 2行目以降：データ
        """

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
tmp_sidebar_text  = "基本統計量のオプション"
tmp_data_path     = "sample_datas"
tmp_data_encoding = 'shift_jis'
tmp_data_dict     = { "擬似データ１":"sampledata01.csv"
                     ,"擬似データ２":"sampledata02.csv"}   

##  自作関数
import lib.Dataload as Dl
read_data_df = Dl.data_load_form(sidebar_text=tmp_sidebar_text
                                , cd_path=tmp_cd_path
                                , data_path= tmp_data_path
                                , data_encoding=tmp_data_encoding
                                , data_dict = tmp_data_dict)
##------  共通：データの取得 End   ------------------------------

st.sidebar.divider()
#===============================================================================================    
# 分析データ列の選択
keys_list = list(read_data_df.keys())
input_col = st.columns([1,1])
with input_col[0]:
    index_str = st.selectbox("データの選択",keys_list  ,key="mselect 02")
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

st.divider()
st.subheader(f"Step２: 基本統計量の計算", divider="green")

with st.spinner('作成中'):
    output = Functions.compute_statistics(data_df)
    # 計算結果の表示
    disp_col1 = st.columns(4)
    disp_col1[0].metric(label="データ数",value=output["データ数"])
    disp_col1[1].metric(label="合計",value=output['合計'])
    disp_col1[2].metric(label="最大値",value=output['最大値'])
    disp_col1[3].metric(label="最小値",value=output['最小値'])
    st.divider()
    disp_col2 = st.columns(4)
    disp_col2[0].metric(label="平均 ",value=f"{output['平均']:4.1f}")
    disp_col2[1].metric(label="標準偏差",value=f"{output['標準偏差']:4.1f}")
    st.divider()
    disp_col3 = st.columns(4)
    disp_col3[0].metric(label="中央値 ",value=f"{output['中央値']:4.1f}")
    disp_col3[1].metric(label="第一四分位数",value=f"{float(output['四分位数'][0]):4.1f}")
    disp_col3[2].metric(label="第二四分位数",value=f"{float(output['四分位数'][1]):4.1f}")
    disp_col3[3].metric(label="第三四分位数",value=f"{float(output['四分位数'][2]):4.1f}")
    st.divider()

    # ax = pd.DataFrame(data_df).plot.box(vert=False)
    # st.pyplot(ax.figure)