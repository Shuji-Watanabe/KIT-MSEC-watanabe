import streamlit as st
import pandas as pd
import numpy as np
import os 
path = os.getcwd()

#### データの作成とその表示
def data_download(index, data_array,ntri=10):
    if index == 2:
        df = pd.DataFrame(data=data_array,columns=[tmp_col_name])
        freq, _ = np.histogram(data_array, bins=ntri+1, range=(0, ntri))
        tmp_index = [ num for num in range(0,ntri+1,1)]
        tmp_df = pd.DataFrame({'number of trials':tmp_index,'freq': freq, 'rfreq': freq / ntri})
        # st.dataframe(tmp_df)
        ax = tmp_df.plot(x='number of trials',y='rfreq')
        # ax = tmp_df["rfreq"].plot.bar()
    else:
        bin_num = int(1 + np.log2(len(data_array)))
        df = pd.DataFrame(data=data_array,columns=[tmp_col_name])
        ax = df.plot.hist(bins=bin_num,rwidth=0.9)
    return df, ax 

def disp_function(index,tmp_array,ntri=10):
    if st.button("生成されたデータの表示"):
            data_df , ax  = data_download(index,tmp_array,ntri)
            tmp_result_col = st.columns([2,1])
            with tmp_result_col[0]:
                st.pyplot(ax.figure) 
            with tmp_result_col[1]:
                st.dataframe(data_df)
                data_file = data_df.to_csv().encode('shift_jis')
                st.download_button(label="結果のダウンロード",data=data_file ,file_name="download_data.csv",mime="text/csv")

##### 本文
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

"""  """
"""  """

### サンプルデータの生成 ###
st.header("2. 分析用デモデータの生成",divider="rainbow")
np.set_printoptions(precision=5)

# type_dict = {"一様分布に従うデータ":0
#              ,"正規分布に従うデータ":1
#              ,"二項分布":2
#              }

type_dict = {"一様分布に従うデータ":0
             ,"正規分布に従うデータ":1
             }

type_keys = type_dict.keys()
selected_type = st.selectbox(label="生成するデータの分布をしていしてください．",options=type_keys)
selected_type_index = type_dict[ selected_type ]
""" """
""" """


f"""#### {selected_type}の生成（1次配列）"""


if selected_type_index == 0:
    option_1_dict = {"整数値":0,"実数値":1}
    option_1_keys = option_1_dict.keys()
    selected_key = st.radio(label="__出力値の選択__",options=option_1_keys,horizontal=True)
    tmp_index=option_1_dict[selected_key]

    tmp_col = st.columns([1,1,1,1])
    with tmp_col[0]:
        tmp_col_name = str(st.text_input("データ名",value="data 1"))
    if tmp_index == 0:
        """
        $~\\text{最小値} \\le x \\le \\text{最大値}~$の範囲の整数を，一様な確率で，指定されたデータ数で生成します．
        """
        with tmp_col[1]:
            size_int = int(st.text_input(label="データ数",value=10))
        with tmp_col[2]: 
            init_num = int(st.text_input(label="最小値",value=0))
        with tmp_col[3]: 
            end_num = int(st.text_input(label="最大値",value=10))+1
        if end_num <= init_num :
            st.error("最小値＜最大値となるように入力してください．")
            st.stop()
        tmp_data_array = np.random.randint(init_num,end_num,size=size_int)

    elif tmp_index == 1:
        """
        $~\\text{最小値} \\le x \\le \\text{最大値}~$の範囲の実数を，一様な確率で，指定されたデータ数で生成します
        """
        with tmp_col[1]:
            size_int = int(st.text_input(label="データ数",value=10))
        with tmp_col[2]: 
            init_num = int(st.text_input(label="最小値",value=0))
        with tmp_col[3]: 
            end_num = int(st.text_input(label="最大値",value=10))+1
        
        if end_num <= init_num :
            st.error("最小値＜最大値となるように入力してください．")
            st.stop()
        tmp_data_array = np.random.uniform(init_num,end_num,size=size_int)
    disp_function(selected_type_index,tmp_data_array)

elif selected_type_index == 1:
    """
    指定された平均と標準偏差で得られる正規分布に従う数値を，指定されたデータ数で生成します．
    """
    tmp_col = st.columns([1,1,1,1])
    with tmp_col[0]:
        tmp_col_name = str(st.text_input("データ名",value="data 1"))
    with tmp_col[1]:
        size_int = int(st.text_input(label="データ数",value=10))
    with tmp_col[2]: 
        mean_num = float(st.text_input(label="平均",value=0))
    with tmp_col[3]: 
        std_num = float(st.text_input(label="標準偏差",value=1))
    tmp_data_array = np.random.normal(mean_num,std_num,size_int)
    disp_function(selected_type_index,tmp_data_array)

elif selected_type_index == 2:
    """
    指定された試行回数と成功確率で得られる二項分布に従う数値を，指定されたデータ数で生成します．
    """
    tmp_col = st.columns([1,1,1,1])
    with tmp_col[0]:
        tmp_col_name = str(st.text_input("データ名",value="data 1"))
    with tmp_col[1]:
        size_int = int(st.text_input(label="データ数",value=10))
    with tmp_col[2]: 
        trials_num = int(st.text_input(label="試行回数",value=10))
    with tmp_col[3]: 
        p_num = float(st.text_input(label="成功確率",value=0.5))
    if 0<= p_num <=1 :
        tmp_data_array = np.random.binomial(trials_num,p_num,size_int)
        disp_function(index=selected_type_index,tmp_array=tmp_data_array,ntri=trials_num )
    else :
        st.error("成功確率は0から1の範囲で指定してください．")

