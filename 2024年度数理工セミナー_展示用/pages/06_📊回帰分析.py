import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import itertools
import lib.display 
import os


#-------------title begin-----------------------------------------------------
st.title("回帰分析")
#-------------title end-------------------------------------------------------
#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
#-------------header end-------------------------------------------------------
"""
このページでは，線形回帰分析を行い，その結果を表示します．
線形回帰分析には，pythonのライブラリ[pingouin](https://pingouin-stats.org/build/html/index.html)
を使用しています．
"""

#=    sidebar begin   ===
st.sidebar.subheader("線形回帰分析のオプション")
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
    
    select_data_dict = {"デモデータ１:回帰分析用データ":0}
    # 分析データの選択
    select_str = st.selectbox("分析に使用するデータを選択してください．",select_data_dict.keys(),key="mselect 01")
    # データの読み込み
    if select_data_dict[select_str] == 0:
        #デモデータ『hist_data01.csv』の読み込み 
        try :
            ## github
            read_data_df = pd.read_csv("sample_datas/linear_regression01.csv",encoding='shift_jis')
        except:
            ##Local
            read_data_df = pd.read_csv("2024年第2回高大連携定例研究会/sample_datas/linear_regression01.csv",encoding='shift_jis')
    else :
        st.stop()
    """___"""



    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        Response_Var_index_str = st.selectbox("目的変数として使用するデータの選択",keys_list)

        if not Response_Var_index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else:
            Response_Var_df = read_data_df[Response_Var_index_str]
            st.dataframe(Response_Var_df
                    , use_container_width=True
                    , height=200)
            keys_list_removed = [item for item in keys_list if item != Response_Var_index_str]
            with input_col[1]:
                Predictors_index_list = st.multiselect("説明変数として使用するデータの選択",keys_list_removed)

                if not Predictors_index_list:
                    """"""
                    st.error("データを選択してください")
                    st.stop()
                Predictors_df = read_data_df[Predictors_index_list]
                st.dataframe(Predictors_df
                        , use_container_width=True
                        , height=200)

    
    st.success(f'準備完了', icon="✅")
    st.divider()
    #-------------subheader begin----------------------------------------------
    st.subheader(f"Step２: 線形回帰分析の実行", divider="green")
    #-------------subheader end------------------------------------------------
    if st.button("計算の実行",key="button 01"):
        with st.spinner('作成中'):
            import pingouin as pg
            lr_results = pg.linear_regression(X=Predictors_df,y=Response_Var_df)
            col_user = st.columns([2,1])
            st.write("#### 計算結果（オリジナル）")
            st.dataframe(lr_results.round(5)
                         , use_container_width=True)
            st.write("#### 計算結果（解説）")
            st.write("##### 1) モデル")
            # LaTeX文字列を作成する
            terms = []
            for i, item in enumerate(Predictors_index_list):
                coeff = lr_results.loc[item, 'coef']
                # 小数第3位までの絶対値
                formatted_coeff = f"{abs(coeff):.3f}"
                
                # 1つ目の項目は符号なし（負の場合は先頭に '-' を付ける）
                if i == 0:
                    sign = "-" if coeff < 0 else ""
                else:
                    # 2つ目以降は正の場合は " + ", 負の場合は " - "
                    sign = " - " if coeff < 0 else " + "
                
                # 各項目の項を生成 (例: "1.23\,(item1)")
                term = f"{sign}{formatted_coeff}\\,({item})"
                terms.append(term)

                # 連結して最終的な文字列を作成
                exp_latex = "Response_Var_index_str = " + "".join(terms)
                st.markdown(f"${exp_latex}$")
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
    st.stop()
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