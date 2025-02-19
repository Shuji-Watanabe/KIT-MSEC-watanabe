import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


#-------------header begin-----------------------------------------------------
st.header("ヒストグラムの作成", divider="rainbow")
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
    st.header(f"""{tub_title }を用いた分析""",divider="rainbow")
    """   """
    st.subheader(f"Step１: 分析データの選択", divider="green")

    select_data_dict = {"デモデータ１：正規分布に従うデータ":0}
    # 分析データの選択
    select_str = st.selectbox("分析に使用するデータを選択してください．",select_data_dict.keys(),key="mselect 01")


    # データの読み込み
    if select_data_dict[select_str] == 0:
        #デモデータ『hist_data01.csv』の読み込み 
        try :
            read_data_df = pd.read_csv("sample_datas/hist_data01.csv",encoding='shift_jis')
        except:
            read_data_df = pd.read_csv("2024年度数理工セミナー_展示用/sample_datas/hist_data01.csv",encoding='shift_jis')

    else :
        st.stop()
    
    """___"""
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("ヒストグラムを作成するデータの選択",keys_list)
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
    if st.checkbox("データの確認",key="cbox 01"):
        st.dataframe(data_df
                        , use_container_width=True
                        , height=200)
    """___"""



    st.subheader(f"Step２: ヒストグラムの作成", divider="green")
    """
    ##### 〜 各種設定 〜
    """
    bins_dict = {"Sturges’ Rule":1,
                 "Scott’s Rule":2,
                  "ユーザー設定":99}
    options_col = st.columns([2,1])
    with options_col[0]:
        select_bins_str =st.radio(label="bin数（階級の数）の設定方法",options=bins_dict.keys(),horizontal=True,key="radio 01")
        select_bins_num = bins_dict[select_bins_str]

    if select_bins_num == 1 :
        bin_num = int(1 + np.log2(len(data_df.to_numpy())))
        with options_col[1]:
            f"""
                \\
                    {select_bins_str} で得られたbin数 = {bin_num} 
            """
    elif select_bins_num == 2 : 
        bin_num = int(3.5 * np.std(data_df.to_numpy()) / (len(data_df.to_numpy()) ** (1/3)))
        with options_col[1]:
            f"""
                \\
                    {select_bins_str} で得られたbin数 = {bin_num} 
            """
    elif select_bins_num == 99:
        with options_col[1]:
            bin_num = st.number_input("ビン数を設定",min_value=1,value=int(1 + np.log2(len(data_df.to_numpy()))))
    # ヒストグラムの作成
    ax = data_df.plot.hist(bins=bin_num,rwidth=0.9)
    st.pyplot(ax.figure)
    

#===============================================================================================
###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta +=1 
    tub_title = list(tub_dict.keys())[tub_counta]
    st.header(f"""{tub_title }を用いた分析""",divider="rainbow")
    """   """
    st.subheader(f"Step１: 分析データのアップロード", divider="green")

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
    input_col = st.columns([2,1])
    with input_col[0]:
        index_str = st.selectbox("データの選択",keys_list  ,key="mselect 03")
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else :
            st.success(f'準備完了', icon="✅")
    with input_col[1]:
        data_df = read_data_df[index_str]
        data_len = data_df.shape[0]
        st.write("")
        if st.checkbox("データの確認",key="cbox 02"):
            st.dataframe(data_df
                         , use_container_width=True
                         , height=200)
        st.divider()

    st.divider()


    """ """

    # ヒストグラムの作成
    st.subheader(f"Step２: ヒストグラムの作成", divider="green")
    """
    ##### 〜 各種設定 〜
    """
    bins_dict = {"Sturges’ Rule":1,
                 "Scott’s Rule":2,
                  "ユーザー設定":99}
    options_col = st.columns([2,1])
    with options_col[0]:
        select_bins_str =st.radio(label="bin数（階級の数）の設定方法",options=bins_dict.keys(),horizontal=True,key="radio 02")
        select_bins_num = bins_dict[select_bins_str]

    if select_bins_num == 1 :
        bin_num = int(1 + np.log2(len(data_df.to_numpy())))
        with options_col[1]:
            f"""
                \\
                    {select_bins_str} で得られたbin数 = {bin_num} 
            """
    elif select_bins_num == 2 : 
        bin_num = int(3.5 * np.std(data_df.to_numpy()) / (len(data_df.to_numpy()) ** (1/3)))
        with options_col[1]:
            f"""
                \\
                    {select_bins_str} で得られたbin数 = {bin_num} 
            """
    elif select_bins_num == 99:
        with options_col[1]:
            bin_num = st.number_input("ビン数を設定",min_value=1,value=int(1 + np.log2(len(data_df.to_numpy()))))
    # ヒストグラムの作成
    ax = data_df.plot.hist(bins=bin_num,rwidth=0.9)
    st.pyplot(ax.figure)