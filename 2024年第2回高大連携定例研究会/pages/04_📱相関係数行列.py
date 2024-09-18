import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import itertools


import lib.display 

"""# 相関係数行列"""

tub_dict = {"デモデータによる分析体験":0,"ユーザーデータによる分析":1}
selected_cbox = st.radio(label="選択", options = tub_dict.keys(),horizontal=True)
"""___"""


###  デモデータによる分析体験
tub_counta = 0
if tub_dict[selected_cbox] == 0 :
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[0]:
    f"""### {tub_title }"""
    """
    ### 1. 分析データの選択
    """
    
    select_data_dict = {"デモデータ１:相関係数用データ":0}
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
        index_str = st.multiselect("相関係数行列を計算するデータの選択",keys_list,key="mselect 02")
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
    ### 2. 相関係数行列の作成
    """
    if st.button("相関係数行列の作成",key="button 01"):
        with st.spinner('作成中'):
            corr_matrix_pearson = data_df.corr('pearson')
            col_user = st.columns([2,1])
            with col_user[0]:
                st.dataframe(corr_matrix_pearson)
            with col_user[1]:
                downloadfile_csv = corr_matrix_pearson.to_csv().encode('shift_jis')
                st.download_button(label="結果のダウンロード",data=downloadfile_csv ,file_name="outfile_corr_matrix.csv",mime="text/csv")
            corrs_list = []
            tmp_list_index = itertools.combinations(index_str, 2)
            for label in tmp_list_index:
                label_list = list(label)
                corrs_list.append([label_list[0],label_list[1],pd.DataFrame(corr_matrix_pearson).at[label_list[0],label_list[1]]])
                
            tmp_corrs_df = pd.DataFrame(corrs_list,columns=["label 1","label 2","corr."])
            tmp_corrs_df = tmp_corrs_df.sort_values("corr.",ascending=False)
            tmp_corrs_df["Explanetion"] = [lib.display.explanation_corr(x) for x in tmp_corrs_df["corr."] ]
            
            with st.expander("相関係数の解釈"):
                st.dataframe(tmp_corrs_df)
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
    
    st.warning('ここで計算される相関係数はピアソンの積率相関係数です．分析に使用するデータが適切かどうか，必ず確認してください．', icon="⚠️")

    """___"""
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("相関係数行列を計算するデータの選択",keys_list,key="mselect 03")
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
    ### 2. 相関係数行列の作成
    """
    if st.button("相関係数行列の作成",key="button 02"):
        with st.spinner('作成中'):
            corr_matrix_pearson = data_df.corr('pearson')
            col_user = st.columns([2,1])
            with col_user[0]:
                st.dataframe(corr_matrix_pearson)
            with col_user[1]:
                downloadfile_csv = corr_matrix_pearson.to_csv().encode('shift_jis')
                st.download_button(label="結果のダウンロード",data=downloadfile_csv ,file_name="outfile_corr_matrix.csv",mime="text/csv")
            corrs_list = []
            tmp_list_index = itertools.combinations(index_str, 2)
            for label in tmp_list_index:
                label_list = list(label)
                corrs_list.append([label_list[0],label_list[1],pd.DataFrame(corr_matrix_pearson).at[label_list[0],label_list[1]]])
                
            tmp_corrs_df = pd.DataFrame(corrs_list,columns=["label 1","label 2","corr."])
            tmp_corrs_df = tmp_corrs_df.sort_values("corr.",ascending=False)
            tmp_corrs_df["Explanetion"] = [lib.display.explanation_corr(x) for x in tmp_corrs_df["corr."] ]
            

            with st.expander("相関係数の解釈"):
                st.dataframe(tmp_corrs_df)