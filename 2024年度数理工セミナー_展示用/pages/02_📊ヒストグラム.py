import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import lib.DataLoad as dl

title_text = "ヒストグラム"

#-------------title begin-----------------------------------------------------
st.title(title_text)
#-------------title end-------------------------------------------------------

#-------------header begin-----------------------------------------------------
st.header(":beginner: 概要",divider="rainbow")
"""ここでは，データのヒストグラムを作成します．"""
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
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

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


# ヒストグラムの作成
ax = data_df.plot.hist(bins=bin_num,rwidth=0.9,alpha=0.5)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import streamlit as st
from scipy.stats import norm

st.sidebar.divider()
st.sidebar.write(":arrow_forward:　グラフに関するオプション")
add_legend_cb = st.sidebar.checkbox("凡例の表示",value=True)
# ヒストグラムの描画（色を取得するために一旦プロット）
ax = data_df.plot.hist(  bins=bin_num
                       , rwidth=0.9
                       , alpha=0.5
                       , density=True
                       , edgecolor='black'
                       , legend=add_legend_cb)
# ヒストグラムの色を取得
handles, labels = ax.get_legend_handles_labels()
colors = [h.get_facecolor() for h in handles] 
# st.write(colors)

add_norm_cb = st.sidebar.checkbox("正規分布のグラフを描画",value=False)
with st.sidebar.expander("描画される正規分布について"):
    ("ヒストグラムに使用しているデータの平均と標準偏差を使用した正規分布を重ねてプロットします．")
if add_norm_cb :
    # 各列のヒストグラムの色を取得して正規分布をプロット
    for i, col in enumerate(data_df.columns):
        a = data_df[col].mean()
        b = data_df[col].std()
        x = np.linspace(data_df[col].min(), data_df[col].max(), 100)
        y = norm.pdf(x, loc=a, scale=b)
        plt.plot(x, y, color=colors[i], linewidth=2, label=f'{col} ( $N({a:.1f}$, ${b:.1f}^2)$)')

    if add_legend_cb:
        plt.legend()

st.pyplot(ax.figure)

