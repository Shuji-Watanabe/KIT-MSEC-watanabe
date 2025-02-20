import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

###------- 共通:カレントディレクトリ情報の取得 Begin -------
from lib import Dataload_form as Df
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




#-------------title begin-----------------------------------------------------
st.title("ヒストグラムの作成")
#-------------title end-------------------------------------------------------

#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
#-------------header end-------------------------------------------------------

"""ここでは，データのヒストグラムを作成します．"""

##------  共通：データの取得 Begin ------------------------------
tmp_sidebar_text  = "ヒストグラム作成のオプション"
tmp_data_path     = "sample_datas/hist_data01.csv"
tmp_data_encoding = 'shift_jis'

##  自作関数
read_data_df = Df.data_load_form(sidebar_text=tmp_sidebar_text
                            , cd_path=tmp_cd_path
                            , data_path= tmp_data_path
                            , data_encoding=tmp_data_encoding)
##------  共通：データの取得 End   ------------------------------

st.sidebar.divider()
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


## Step 2 #### 
st.subheader(f"Step２: ヒストグラムの作成", divider="green")
bins_dict = {"Sturges’ Rule":1,"Scott’s Rule":2,"ユーザー設定":99}
select_bins_str =st.sidebar.radio(label=":arrow_forward: bin数（階級の数）の設定方法"
                                    ,options=bins_dict.keys()
                                    ,horizontal=True,key="radio 01")
select_bins_num = bins_dict[select_bins_str]
if select_bins_num == 1 :
    bin_num = int(1 + np.log2(len(data_df.to_numpy())))
elif select_bins_num == 2 : 
    bin_num = int(3.5 * np.std(data_df.to_numpy()) / (len(data_df.to_numpy()) ** (1/3)))
elif select_bins_num == 99:
    bin_num = st.sidebar.number_input("ビン数を設定",min_value=1,value=int(1 + np.log2(len(data_df.to_numpy()))))

st.sidebar.write(f"{select_bins_str} で得られたbin数 = {bin_num}")
st.sidebar.divider()

# ヒストグラムの作成
ax = data_df.plot.hist(bins=bin_num,rwidth=0.9,alpha=0.5)
st.pyplot(ax.figure)