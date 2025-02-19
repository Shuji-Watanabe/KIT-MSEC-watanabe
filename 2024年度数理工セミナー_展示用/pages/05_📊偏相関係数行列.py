import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import itertools
import lib.display 
import os


#-------------title begin-----------------------------------------------------
st.title("偏相関係数行列の作成")
#-------------title end-------------------------------------------------------
#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
#-------------header end-------------------------------------------------------
"""
このページでは，偏相関係数行列を求め，その結果を表示します．
偏相関係数の計算には，pythonのライブラリ[pingouin](https://pingouin-stats.org/build/html/index.html)
を使用しています．
"""

#=    sidebar begin   ===
st.sidebar.subheader("偏相関係数行列のオプション")
st.sidebar.write("どのようなデータを用いてデータ分析を行うか選択してください．")
tub_dict = {"分析体験デモデータ":0,"ユーザーデータ":1}
selected_cbox = st.sidebar.radio(label="選択", options = tub_dict.keys(),horizontal=True)
#=    sidebar   end   ===


###  デモデータによる分析体験
tub_counta = 0
if tub_dict[selected_cbox] == 0 :
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[0]:
    #-------------header begin-----------------------------------------------------
    st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
    """   """
    #-------------header end-------------------------------------------------------
    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step１: 分析データの選択", divider="green")
    #-------------subheader end------------------------------------------------
    
    select_data_dict = {"デモデータ１:相関係数用データ":0}
    # 分析データの選択
    select_str = st.selectbox("分析に使用するデータを選択してください．",select_data_dict.keys(),key="mselect 01")
    # データの読み込み
    if select_data_dict[select_str] == 0:
        #デモデータ『hist_data01.csv』の読み込み 
        try :
            ## github
            read_data_df = pd.read_csv("sample_datas/scatter_data01.csv",encoding='shift_jis')
        except:
            ##Local
            read_data_df = pd.read_csv("22024年度数理工セミナー_展示用/sample_datas/scatter_data01.csv",encoding='shift_jis')
    else :
        st.stop()
    """___"""



    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("相関係数行列を作成するデータの選択",keys_list)

        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        elif len(index_str) == 1 :
            """"""
            st.error("データを2つ以上選択してください")
            st.stop() 
           
    data_df = read_data_df[index_str]
    data_len = data_df.shape[0]
    
    with input_col[1]:
        st.dataframe(data_df
                , use_container_width=True
                , height=200)
    st.success(f'準備完了', icon="✅")
    st.divider()

    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step２: 偏相関係数行列の作成", divider="green")
    #-------------subheader end------------------------------------------------
    if st.button("偏相関係数行列の作成",key="button 01"):
        with st.spinner('作成中'):
            import pingouin as pg
            partial_corr_matrix = pg.pcorr(data_df)
            col_user = st.columns([2,1])
            
            st.dataframe(partial_corr_matrix
                         , use_container_width=True)
            corrs_list = []
            tmp_list_index = itertools.combinations(index_str, 2)
            for label in tmp_list_index:
                label_list = list(label)
                corrs_list.append([label_list[0],label_list[1],pd.DataFrame(partial_corr_matrix).at[label_list[0],label_list[1]]])
                
            tmp_corrs_df = pd.DataFrame(corrs_list,columns=["label 1","label 2","corr."])
            tmp_corrs_df = tmp_corrs_df.sort_values("corr.",ascending=False)
            tmp_corrs_df["Explanetion"] = [lib.display.explanation_corr(x) for x in tmp_corrs_df["corr."] ]
            
            with st.expander("偏相関係数の解釈"):
                st.dataframe(tmp_corrs_df)
    else:
        """___"""


#===============================================================================================
###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[1]:
    #-------------header begin-----------------------------------------------------
    st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
    #-------------header end-------------------------------------------------------
    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step１: 分析データのアップロード", divider="green")
    #-------------subheader end------------------------------------------------


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


    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("偏相関係数行列を作成するデータの選択",keys_list,key="mselect 02")
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        elif len(index_str) == 1 :
            """"""
            st.error("データを2つ以上選択してください")
            st.stop() 
           
    data_df = read_data_df[index_str]
    data_len = data_df.shape[0]

    with input_col[1]:
        st.dataframe(data_df
                        , use_container_width=True
                        , height=200)
    st.success(f'準備完了', icon="✅")
    st.divider()

    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step２: 偏相関係数行列の作成", divider="green")
    #-------------subheader end------------------------------------------------
    if st.button("偏相関係数行列の作成",key="button 01"):
        with st.spinner('作成中'):
            import pingouin as pg
            partial_corr_matrix = pg.pcorr(data_df)
            col_user = st.columns([2,1])
            
            st.dataframe(partial_corr_matrix
                         , use_container_width=True)
            corrs_list = []
            tmp_list_index = itertools.combinations(index_str, 2)
            for label in tmp_list_index:
                label_list = list(label)
                corrs_list.append([label_list[0],label_list[1],pd.DataFrame(partial_corr_matrix).at[label_list[0],label_list[1]]])
                
            tmp_corrs_df = pd.DataFrame(corrs_list,columns=["label 1","label 2","corr."])
            tmp_corrs_df = tmp_corrs_df.sort_values("corr.",ascending=False)
            tmp_corrs_df["Explanetion"] = [lib.display.explanation_corr(x) for x in tmp_corrs_df["corr."] ]
            
            with st.expander("偏相関係数の解釈"):
                st.dataframe(tmp_corrs_df)
    else:
        """___"""