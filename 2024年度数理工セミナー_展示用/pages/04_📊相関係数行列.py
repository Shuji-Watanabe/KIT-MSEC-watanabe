import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import itertools
import lib.display 
import lib.DataLoad as dl

# サイドバーを初期状態で表示する
st.set_page_config(initial_sidebar_state="expanded")

title_text="相関係数行列"
#-------------title begin-----------------------------------------------------
st.title(title_text)
#-------------title end-------------------------------------------------------

#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
"""ここでは，データから相関係数行列を作成します．"""
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
tmp_data_encoding = 'shift_jis'
tmp_data_dict     = { "擬似データ１":"sampledata01.csv"
                     ,"擬似データ２":"sampledata02.csv"}   

##  自作関数
read_data_df = dl.data_load_form(sidebar_text=tmp_sidebar_text
                                , cd_path=tmp_cd_path
                                , data_path= tmp_data_path
                                , data_dict = tmp_data_dict)
##------  共通：データの取得 End   ------------------------------
#===============================================================================================    
# 分析データ列の選択
keys_list = list(read_data_df.keys())
input_col = st.columns([1,1])
with input_col[0]:
    index_str = st.multiselect("データの選択",keys_list  ,key="mselect 02")
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
#===============================================================================================

if not 'filename' in st.session_state:
    st.sidebar.divider()
#-------------subheader begin----------------------------------------------
st.subheader(f"Step２: データの相関係数行列", divider="green")
#-------------subheader end------------------------------------------------
ToF_dict = {"非表示":False,"表示":True}
with st.spinner('作成中'):
    # 相関行列を計算（ピアソン相関）
    corr_matrix_pearson = data_df.corr('pearson')
    col_user = st.columns([2,1])

    st.sidebar.divider()
    corr_digit_num = st.sidebar.number_input(":arrow_forward: 表示される数値の桁数"
                                             ,min_value=0
                                             ,max_value=4
                                             ,step=1
                                             ,value=2)
    st.dataframe(corr_matrix_pearson.round(corr_digit_num)
                    , use_container_width=True)


disp_Interpretation=st.sidebar.radio(":arrow_forward: 相関の解釈を表示"
                                     , options=ToF_dict.keys()
                                     , horizontal=True)
if ToF_dict[disp_Interpretation]:
    st.write("計算された相関係数から，変数間の相関関係を分析した結果は次の通りです．")
    corrs_list = []
    tmp_list_index = itertools.combinations(index_str, 2)
    for label in tmp_list_index:
        label_list = list(label)
        corrs_list.append([label_list[0],label_list[1],pd.DataFrame(corr_matrix_pearson).at[label_list[0],label_list[1]]])
        
    tmp_corrs_df = pd.DataFrame(corrs_list,columns=["label 1","label 2","corr."])
    tmp_corrs_df = tmp_corrs_df.sort_values("corr.",ascending=False)
    tmp_corrs_df["Explanetion"] = [lib.display.explanation_corr(x) for x in tmp_corrs_df["corr."] ]
    st.dataframe(tmp_corrs_df
                ,hide_index=True
                ,use_container_width=True)


disp_heatmap=st.sidebar.radio(":arrow_forward: ヒートマップを表示"
                                     , options=ToF_dict.keys()
                                     , horizontal=True)

if ToF_dict[disp_heatmap]:
    import seaborn as sns
    import matplotlib.pyplot as plt
    import japanize_matplotlib
    
    ### seabornのヒートマップのオプション
    # https://matplotlib.org/2.0.2/examples/color/colormaps_reference.htmlより
    cmap_list = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

    selected_color = st.sidebar.radio(":arrow_forward: ヒートマップの色の選択",options=cmap_list,horizontal=True)
    reverse_ck = st.sidebar.checkbox("色を反転させる",value=False)
    if reverse_ck:
        selected_color = selected_color + "_r"
    # ヒートマップを作成
    plt.figure(figsize=(4, 4))  # サイズ指定
    sns.heatmap(corr_matrix_pearson 
                , annot=True
                , fmt=f".{corr_digit_num}f"
                , cmap=selected_color
                , center=0
                , vmin=-1
                , vmax=1)
    # Streamlit で表示
    st.pyplot(plt)

st.page_link("00_Data_Analysis_Apps.py", label="Home", icon="🏠")