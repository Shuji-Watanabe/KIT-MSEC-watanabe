import streamlit as st
import pandas as pd
import numpy as np
import os 
path = os.getcwd()

"""# データの取得と生成"""
"""
ここでは，このWebアプリで使用しているデータのダウンロードと，
分析実習等で使用するためのデモデータの生成を行います．
データ生成において，次のサイトの内容を参考にしています，

- 相関のある2つのデータの生成  
    [Qiita:相関のある2つの擬似乱数の生成（Pythonサンプルつき）](https://qiita.com/horiem/items/30a8783604ae67cdd63e)
- 乱数の生成  
    [Oeconomicus.jp:【Python】Numpyで一様分布や正規分布、二項分布、ポアソン分布に従う乱数を発生させる](https://oeconomicus.jp/2021/06/python-numpy-random/#outline__1)

___
"""


if path == '/mount/src/kit-msec-watanabe':
    tmp_file_path = "2024年第2回高大連携定例研究会/sample_datas/"
else:
    tmp_file_path = "sample_datas/"



### 使用データのダウンロード ###
st.header("1. 使用データのダウンロード",divider="rainbow")

pages_dict = {"基本統計量の計算":"scatter_data01.csv"
              ,"ヒストグラム":"hist_data01.csv"
             ,"散布図 散布図行列":"scatter_data01.csv"
             ,"相関係数行列":"scatter_data01.csv"
             ,"Map機能":"GPS_Data.csv"
            }

pages_keys = pages_dict.keys()

selected_key = st.selectbox(label="ダウンロードしたいデータを使用しているプログラムを選択",options=pages_keys,key="select 01")
if not selected_key :
    st.error("項目を適切に選択してください．")
else :
    file_path = tmp_file_path + pages_dict[selected_key]
    tmp_col = st.columns([2,1])
    with tmp_col[0]:
        f"""
        {selected_key}で使用したデータをダウンロードします．
        """
    with tmp_col[1]:
        data_file = open(str(file_path))
        st.download_button(label="結果のダウンロード",data=data_file ,file_name="download_datafile.csv",mime="text/csv")

### サンプルデータの生成 ###