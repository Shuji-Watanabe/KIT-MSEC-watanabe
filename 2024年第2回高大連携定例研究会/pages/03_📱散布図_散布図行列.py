import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns


#-------------header begin-----------------------------------------------------
st.header("散布図行列の作成", divider="rainbow")
"""
どのようなデータを用いてデータ分析を行うか選択してください．
"""
tub_dict = {"分析体験デモデータ":0,"ユーザーデータ":1}
selected_cbox = st.radio(label="選択", options = tub_dict.keys(),horizontal=True)
"""___"""
#-------------header end-------------------------------------------------------

###  デモデータによる分析体験
tub_counta = 0
tub_title = list(tub_dict.keys())[tub_counta]
if tub_dict[selected_cbox] == 0 :
    #-------------header begin-----------------------------------------------------
    st.header(f"""{tub_title }を用いた分析""",divider="rainbow")
    #-------------header end-------------------------------------------------------
    """   """
    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step１: 分析データの選択", divider="green")
    #-------------subheader end------------------------------------------------

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
    
    with input_col[1]:
        if st.checkbox("データの確認",key="cbox 01"):
            st.dataframe(data_df
                            , use_container_width=True
                            , height=200)
    """___"""

    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step２: 散布図（散布図行列）の作成", divider="green")
    #-------------subheader end------------------------------------------------
    if st.button("散布図の作成",key="button 01"):
        with st.spinner('作成中'):
            fig = sns.pairplot(data = data_df)
            st.pyplot(fig)



###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
    #-------------header begin-----------------------------------------------------
    st.header(f"""{tub_title }を用いた分析""",divider="rainbow")
    #-------------header end-------------------------------------------------------
    """ """
    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step１: 分析データのアップロード", divider="green")
    #-------------subheader end------------------------------------------------

    ## データのアップロードと読み込み
    disp_col0 = st.columns([1,1])
    with disp_col0[0]:
        st.warning("データをアップロードする前に，アップロードするデータに個人情報等，取扱に注意しなければならないデータが含まれていないか確認してください．")
        tmp_check = st.checkbox("確認しました．")
    with disp_col0[1]:
        if tmp_check:
            uploaded_files = st.file_uploader("CSVファイルをアップロードしてください．")    
            if not uploaded_files:
                st.error('データがアップロードされていません', icon="⚠️")
                st.stop()
        else :
            st.write("停止中")
            st.stop()
    
    st.divider()
    disp_upload_col = st.columns([1,1])
    set_encode_list = ["自動","選択","入力"]
    with disp_upload_col[0]:
        selected_way = st.radio("エンコードの指定方法",options=set_encode_list,horizontal=True)
    with disp_upload_col[1]:
        import lib.FileProcessing as FileProcessing 
        read_data_df= FileProcessing.streamlit_uploaded_csv(st_uploaded_files=uploaded_files,selected_type=selected_way)
    st.divider()


    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("散布図（散布図行列）を作成するデータの選択",keys_list,key="mselect 02")
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
    """ """
    with input_col[1]:
        if st.checkbox("データの確認",key="cbox 02"):
            st.dataframe(data_df
                         , use_container_width=True
                         , height=200)
    st.divider()

    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step２: 散布図（散布図行列）の作成", divider="green")
    #-------------subheader end------------------------------------------------
    if st.button("散布図の作成",key="button 02"):
        with st.spinner('作成中'):
            fig = sns.pairplot(data = data_df)
            st.pyplot(fig)