import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import itertools
import lib.display 
import os

results_keys_dict = { "names":"変数名"
                    ,"coef":"偏回帰係数"
                    ,"se":"標準誤差"
                    ,"T":"T値"
                    ,"pval":"p値"
                    ,"CI[2.5%]":"下限"
                    ,"CI[97.5%]":"上限"
                    ,"r2":"決定係数"
                    ,"adj_r2":"自由度調整済決定係数"}

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
st.sidebar.markdown(":arrow_forward: 分析に使用するデータの選択")
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
    left_side_col, right_side_col = st.columns([1,1])
    
    with left_side_col:
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
            read_data_df = pd.read_csv("2024年度数理工セミナー_展示用/sample_datas/linear_regression01.csv",encoding='shift_jis')
    else :
        st.stop()

    with right_side_col:
        st.write("読み込まれたデータの確認")
        st.dataframe(read_data_df
                    , use_container_width=True
                    , height=200)
    """___"""



    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        Response_Val_index_str = st.selectbox("目的変数として使用するデータの選択",keys_list)

        if not Response_Val_index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else:
            Response_Val_df = read_data_df[Response_Val_index_str]
            st.dataframe(Response_Val_df
                    , use_container_width=True
                    , height=200)
            keys_list_removed = [item for item in keys_list if item != Response_Val_index_str]
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
    with st.spinner('作成中'):
        import pingouin as pg
        lr_results = pg.linear_regression(X=Predictors_df,y=Response_Val_df)
        names_list = ["Intercept"] + Predictors_index_list
        coef_list = lr_results[lr_results["names"]==names_list]["coef"]


        
        disp_col1 = st.columns([2,5])
        st.sidebar.markdown(":arrow_forward: 表示桁数の設定")
        r2_digit_num = st.sidebar.number_input(label="予測精度の評価の表示桁数",min_value=0,step=1,value=3)
        ana_digit_num = st.sidebar.number_input(label="偏回帰係数に関する分析の表示桁数",min_value=0,step=1,value=3)
        with disp_col1[0]:
            st.write("#### 予測精度の評価")
            st.metric( label=results_keys_dict["r2"]
                    ,value=float(lr_results.loc[0,"r2"].round(r2_digit_num )))
            st.metric( label=results_keys_dict["adj_r2"]
                    ,value=float(lr_results.loc[0,"adj_r2"].round(r2_digit_num )))
        with disp_col1[1]:
            st.write("#### 偏回帰係数に関する分析")
            results_keys_list = list(results_keys_dict.keys())
            disp_result_df = lr_results[results_keys_list[:7]]
            disp_result_df.rename(columns=results_keys_dict, inplace=True)
            st.dataframe(data=disp_result_df.round(ana_digit_num)
                        ,hide_index = True
                        , use_container_width=True)
            st.write("＊下限：95%信頼区間の下限，　上限：95%信頼区間の上限 ")

        from lib import display
        lr_expr_latex = display.make_lr_expr(names_list=names_list
                                                ,coef_list=coef_list
                                                ,response_value=Response_Val_index_str)
        
        st.write("#### 得られた線形回帰式")
        st.latex(lr_expr_latex)    
        st.divider()
                
    st.divider()


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

    st.sidebar.divider()
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        Response_Val_index_str = st.selectbox("目的変数として使用するデータの選択",keys_list)

        if not Response_Val_index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else:
            Response_Val_df = read_data_df[Response_Val_index_str]
            st.dataframe(Response_Val_df
                    , use_container_width=True
                    , height=200)
            keys_list_removed = [item for item in keys_list if item != Response_Val_index_str]
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
    with st.spinner('作成中'):
        import pingouin as pg
        lr_results = pg.linear_regression(X=Predictors_df,y=Response_Val_df)
        names_list = ["Intercept"] + Predictors_index_list
        coef_list = lr_results[lr_results["names"]==names_list]["coef"]
        
        disp_col1 = st.columns([2,5])
        st.sidebar.markdown(":arrow_forward: 表示桁数の設定")
        r2_digit_num = st.sidebar.number_input(label="予測精度の評価の表示桁数",min_value=0,step=1,value=3)
        ana_digit_num = st.sidebar.number_input(label="偏回帰係数に関する分析の表示桁数",min_value=0,step=1,value=3)
        st.sidebar.divider()
        with disp_col1[0]:
            st.write("#### 予測精度の評価")
            st.metric( label=results_keys_dict["r2"]
                    ,value=float(lr_results.loc[0,"r2"].round(r2_digit_num )))
            st.metric( label=results_keys_dict["adj_r2"]
                    ,value=float(lr_results.loc[0,"adj_r2"].round(r2_digit_num )))
        with disp_col1[1]:
            st.write("#### 偏回帰係数に関する分析")
            results_keys_list = list(results_keys_dict.keys())
            disp_result_df = lr_results[results_keys_list[:7]]
            disp_result_df.rename(columns=results_keys_dict, inplace=True)
            st.dataframe(data=disp_result_df.round(ana_digit_num)
                        ,hide_index = True
                        , use_container_width=True)
            st.write("＊下限：95%信頼区間の下限，　上限：95%信頼区間の上限 ")
            
        from lib import display
        lr_expr_latex = display.make_lr_expr(names_list=names_list
                                                ,coef_list=coef_list
                                                ,response_value=Response_Val_index_str)
        
        st.write("#### 得られた線形回帰式")
        st.latex(lr_expr_latex)    
        st.divider()       
    st.divider()