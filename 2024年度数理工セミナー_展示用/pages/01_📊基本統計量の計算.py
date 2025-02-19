import streamlit as st
import pandas as pd
import numpy as np
import lib.Functions as Functions

#-------------title begin-----------------------------------------------------
st.title("基本統計量の計算")
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

st.sidebar.subheader("基本統計量計算のオプション")
st.sidebar.markdown(":arrow_forward: 分析に使用するデータの選択")
tub_dict = {"分析体験デモデータ":0,"ユーザーデータ":1}
selected_cbox = st.sidebar.radio(label="選択", options = tub_dict.keys(),horizontal=True)
""" """

#===============================================================================================
###  デモデータによる分析体験
tub_counta = 0
if tub_dict[selected_cbox] == 0 :
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[0]:
    st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
    """   """
    st.subheader(f"Step１: 分析データの選択", divider="green")
    input_col = st.columns([1,1])
    select_data_dict = {"デモデータ１":0}

    with input_col[0]:
        # 分析データの選択
        select_str = st.selectbox("分析するデータを選択してください",select_data_dict.keys(),key="mselect 01")

        # データの読み込み
        if select_data_dict[select_str] == 0:
            #デモデータ『hist_data01.csv』の読み込み 
            try :
                read_data_df = pd.read_csv("sample_datas/scatter_data01.csv",encoding='shift_jis')
            except:
                read_data_df = pd.read_csv("2024年第2回高大連携定例研究会/sample_datas/scatter_data01.csv",encoding='shift_jis')
        else :
            st.stop()

        # 分析データ列の選択
        keys_list = list(read_data_df.keys())
        index_str = st.selectbox("データ列を１つ選択",keys_list,key="mselect 02")

    with input_col[1]:
        data_df = read_data_df[index_str]
        st.dataframe(data_df
                        , use_container_width=True
                        , height=200)

    """___"""

    st.subheader(f"Step２: 基本統計量の計算", divider="green")

    if st.button("計算の実行",key="button 01"):
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


#===============================================================================================
###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[1]:
    st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
    """   """
    st.subheader(f"Step１: 分析データのアップロード", divider="green")
    
    disp_col0 = st.columns([1,3])
    with disp_col0[1]:
        st.warning("データをアップロードする前に，アップロードするデータに個人情報等，取扱に注意しなければならないデータが含まれていないか確認してください．")
    with disp_col0[0]:
        tmp_check = st.checkbox("確認しました")
    st.sidebar.divider()
    if tmp_check:
        st.divider()
        uploaded_files = st.sidebar.file_uploader(":arrow_forward: CSVファイルのアップロード")    
        if not uploaded_files:
            st.sidebar.error('データがアップロードされていません', icon="⚠️")
            st.stop()
    else :
        st.sidebar.write("停止中")
        st.stop()
    
    st.sidebar.divider()
    set_encode_list = ["自動","選択","入力"]
    selected_way = st.sidebar.radio(":arrow_forward: エンコードの指定方法",options=set_encode_list,horizontal=True)
    import lib.FileProcessing as FileProcessing 
    read_data_df= FileProcessing.streamlit_uploaded_csv(st_uploaded_files=uploaded_files
                                                        ,selected_type=selected_way
                                                        ,DisplayLocation="sidebar")
    st.sidebar.divider()
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.selectbox("データの選択",keys_list  ,key="mselect 03")
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
    st.divider()

    st.subheader(f"Step２: 基本統計量の計算", divider="green")
    if st.button("計算の実行",key="button 01"):
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

