import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns


"""# 散布図行列"""
tub_dict = {"デモデータによる分析体験":0,"ユーザーデータによる分析":1}
selected_cbox = st.radio(label="選択", options = tub_dict.keys(),horizontal=True)
"""___"""

# tub_list = st.tabs(tub_dict.keys())

###  デモデータによる分析体験
tub_counta = 0
tub_title = list(tub_dict.keys())[tub_counta]
if tub_dict[selected_cbox] == 0 :
    f"""### {tub_title }"""
    """
    ### 1. 分析データの選択
    """
    
    select_data_dict = {"デモデータ1":0}
    # 分析データの選択
    select_str = st.selectbox("分析に使用するデータを選択してください．",select_data_dict.keys(),key="mselect 01")


    # データの読み込み
    if select_data_dict[select_str] == 0:
        #デモデータ『hist_data01.csv』の読み込み         
        try :
            read_data_df = pd.read_csv("sample_datas/scatter_data01.csv",encoding='shift_jis')
        except:
            read_data_df = pd.read_csv("2024年第2回高大連携定例研究会/sample_datas/scatter_data01.csv",encoding='shift_jis')
    else :
        st.stop()

    """___"""
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("散布図（散布図行列）を作成するデータの選択",keys_list)
    with input_col[1]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        elif len(index_str) == 1 :
            """"""
            st.error("データを2つ以上選択してください")
            st.stop() 
        else :
            """"""
            st.success(f'準備完了', icon="✅")
            data_df = read_data_df[index_str]
            data_len = data_df.shape[0]
    st.write("")
    if st.checkbox("データの確認",key="cbox 01"):
        st.dataframe(data_df)
    """___"""


    """
    ### 2. 散布図（散布図行列）の作成
    """
    if st.button("散布図の作成",key="button 01"):
        with st.spinner('作成中'):
            fig = sns.pairplot(data = data_df)
            st.pyplot(fig)



###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
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
        index_str = st.multiselect("散布図（散布図行列）を作成するデータの選択",keys_list,key="mselect 02")
    with input_col[1]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        elif len(index_str) == 1 :
            """"""
            st.error("データを2つ以上選択してください")
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
    ### 2. 散布図（散布図行列）の作成
    """
    if st.button("散布図の作成",key="button 02"):
        with st.spinner('作成中'):
            fig = sns.pairplot(data = data_df)
            st.pyplot(fig)