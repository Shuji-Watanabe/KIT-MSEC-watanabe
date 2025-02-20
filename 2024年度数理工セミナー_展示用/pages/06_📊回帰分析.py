import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import lib.DataLoad as dl

results_keys_dict = { "names":"変数名"
                    ,"coef":"偏回帰係数"
                    ,"se":"標準誤差"
                    ,"T":"T値"
                    ,"pval":"p値"
                    ,"CI[2.5%]":"下限"
                    ,"CI[97.5%]":"上限"
                    ,"r2":"決定係数"
                    ,"adj_r2":"自由度調整済決定係数"}


# サイドバーを初期状態で表示する
st.set_page_config(initial_sidebar_state="expanded")

title_text="回帰分析"
#-------------title begin-----------------------------------------------------
st.title(title_text)
#-------------title end-------------------------------------------------------

#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
"""
このページでは，線形回帰分析を行い，その結果を表示します．
線形回帰分析には，pythonのライブラリ[pingouin](https://pingouin-stats.org/build/html/index.html)
を使用しています．
"""
#-------------header end-------------------------------------------------------

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
tmp_sidebar_text  = f"{title_text}のオプション"
tmp_data_path     = "sample_datas"
tmp_data_dict     = { "擬似データ１":"sampledata01.csv"
                     ,"擬似データ２":"sampledata02.csv"}   

##  自作関数
read_data_df = dl.data_load_form(sidebar_text=tmp_sidebar_text
                                , cd_path=tmp_cd_path
                                , data_path= tmp_data_path
                                , data_dict = tmp_data_dict)
##------  共通：データの取得 End   ------------------------------

if not 'filename' in st.session_state:
    st.sidebar.divider()
#===============================================================================================    

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
#===============================================================================================
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
    st.sidebar.divider()
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
    st.divider()


    from lib import display
    lr_expr_latex = display.make_lr_expr(names_list=names_list
                                            ,coef_list=coef_list
                                            ,response_value=Response_Val_index_str)

    st.write("#### 得られた線形回帰式")
    st.latex(lr_expr_latex)    
    st.divider()
                