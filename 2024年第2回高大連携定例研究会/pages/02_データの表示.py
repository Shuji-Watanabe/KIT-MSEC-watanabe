# ライブラリの読み込み
import streamlit as st
import pandas as pd
import numpy as np

#st: st.title を利用したテキスト表示
st.title("データの表示方法")

"""
ここでは，pandasを使用したデータ分析を念頭に，
Series（１列のみで構成されるデータ）と
DataFrame（行と列で構成されるデータ）を
`st.dataframe` で表示する方法を説明します．
なお，numpyのarray形式のデータもこの方法で表示することができます．

__参考資料__
- pandasのSeriesとDataFrameの取り扱いについてはこちらをご覧ください．  
    [Pandas Seriesを徹底解説！](https://ai-inter1.com/python-series/#st-toc-h-6)  
    [Pandas DataFrameを徹底解説！](https://ai-inter1.com/python-series/#st-toc-h-6)
- `st.dataframe`に関する詳細はこちらをご覧ください．  
    [API reference:dataframe](https://docs.streamlit.io/develop/api-reference/data/st.dataframe)
"""

#st: st.header を利用した見出し表示
st.header("Series形式のデータの表示",divider='rainbow')


### 表示用データの作成 ###
# 1行のリスト作成
data_1d_list = [1, 2, 3]
# リストをSeries形式へ変換
data_1d_df = pd.Series(data=data_1d_list
                       ,name="1列目"
                       ,index=["1行目","2行目","3行目"])

#st: Series形式のデータの表示
st.dataframe(data_1d_df)


# 3行３列のリストを作成
data_list = [[1  , 2  , 3],
             [11 , 12 , 13],
             [101, 102, 103]]
# 2次元的なリストをDataFrame形式へ変換
data_2d_df = pd.DataFrame( 
                        data=data_list
                        ,columns=["１列目","２列目","3列目"]
                        ,index=["1行目","2行目","3行目"]
                        )

st.header("DataFrame形式のデータの表示",divider='rainbow')
#st: DataFrame形式のデータの表示
st.dataframe(data_2d_df)

if st.checkbox("ソースコード表示",key="data_show_code_disp") :
    """"""
    st.code(data_list, language="python")


d1 = np.arange(1, 5, 1)
d2 = np.arange(11, 15, 1)
x = [d1,d2]
st.dataframe(x)