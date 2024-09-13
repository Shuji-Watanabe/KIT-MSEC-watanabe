import streamlit as st
import pandas as pd
import numpy as np

"""## ヒストグラム"""
tub_dict = {"デモデータによる分析体験":0,"ユーザーデータによる分析":1}
selected_cbox = st.radio(label="選択", options = tub_dict.keys(),horizontal=True)
"""___"""


#===============================================================================================
###  デモデータによる分析体験
tub_counta = 0
if tub_dict[selected_cbox] == 0 :
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[0]:
    f"""### {tub_title }"""
    """
    ### 1. 分析データの選択
    """
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
    with input_col[1]:
        index_str = st.multiselect("データ列の選択",keys_list,key="mselect 02")

    disp_col = st.columns([1,4])
    with disp_col[0]:
        if not index_str:
            st.error("データを選択してください")
            st.stop()
        else :
            st.success(f'準備完了', icon="✅")
            data_df = read_data_df[index_str]
            data_len = data_df.shape[0]
    with disp_col[1]:
        if st.checkbox("データの確認",key="cbox 01"):
            st.dataframe(data_df)

    """___"""


    """
    ### 2. 基本統計量の計算
    """
    if st.button("計算の実行",key="button 01"):
        with st.spinner('作成中'):
            st.write("作成中")
    else:
        """___"""


#===============================================================================================
###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[1]:
    f"""### {tub_title }"""
    """
    ### 1. 分析データのアップロード
    """
    uploaded_files = st.file_uploader("CSVファイルをアップロードしてください．")    
    if not uploaded_files:
        st.error('データがアップロードされていません', icon="⚠️")
        st.stop()
    else:
        read_data_df = pd.read_csv(uploaded_files,encoding='shift_jis')

    """___"""
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("データの選択",keys_list,key="mselect 03")
    with input_col[1]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
    with input_col[1]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else :
            """"""
            st.success(f'準備完了', icon="✅")
            data_df = read_data_df[index_str]
            data_len = data_df.shape[0]
    st.write("")
    if st.checkbox("データの確認",key="cbox 02"):
        st.dataframe(data_df)
    """___"""




    """
    ### 2. 基本統計量の計算
    """
    if st.button("計算の実行",key="button 01"):
        with st.spinner('作成中'):
            st.write("作成中")
    else:
        """___"""