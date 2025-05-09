import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
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
    tmp_file_path = "/mount/src/kit-msec-watanabe/sample_datas"
else:
    tmp_file_path = "sample_datas"

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
    file_path = os.path.join(tmp_file_path, pages_dict[selected_key])
    st.write(file_path)
    tmp_col = st.columns([2,1])
    with tmp_col[0]:
        f"""
        {selected_key}で使用したデータをダウンロードします．
        """
    with tmp_col[1]:
        # data_file = open(file_path)
        st.write(file_path)
        st.download_button(label="結果のダウンロード",data=file_path ,file_name="download_datafile.csv",mime="text/csv")

"""  """
"""  """



### サンプルデータの生成 : １次配列###
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
selected_type = st.selectbox(label="生成するデータの分布をしていしてください．",options=type_keys, key="makedata1")
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


"""___"""
### サンプルデータの生成 : ２次配列###
st.header("3. 分析用デモデータの生成",divider="rainbow")
np.set_printoptions(precision=5)

type_dict = {"正規分布に従うデータ":1}

type_keys = type_dict.keys()
selected_type = st.selectbox(label="生成するデータの分布をしていしてください．",options=type_keys, key="makedata2")
selected_type_index = type_dict[ selected_type ]
""" """
""" """


f"""#### {selected_type}の生成（2次配列）"""
"""

平均 $~\\mu_{\\rm x}~$，標準偏差$~\\sigma_{\\rm x}~$の正規分布に従うサンプル数$~n~$のデータ$~X~$と，
相関係数が$~\\rho~$となるような，
平均 $~\\mu_{\\rm y}~$，標準偏差$~\\sigma_{\\rm y}~$に正規分布に従うサンプル数$~n~$のデータ$~Y~$を生成します．
___
"""

tmp_col = st.columns([1,1,1,1]) 
if selected_type_index == 1:
    with tmp_col[0]:
        size_int = int(st.text_input(label="サンプル数",value= 500,key="sample size"))
        rho = float(st.number_input(label="相関係数$~\\rho~$",min_value=-1.0,max_value=1.0,value=0.75)) 
    with tmp_col[1]: 
        d_name_x = st.text_input(label="$~\\rm X~$の名前",value="data X",key="data name of x")
        d_name_y = st.text_input(label="$~\\rm Y~$の名前",value="data Y",key="data name of y")
    with tmp_col[2]: 
        mu_x = float(st.text_input(label="$~\\rm X~$の平均",value=0,key="mean of x"))
        mu_y = float(st.text_input(label="$~\\rm Y~$の平均",value=0,key="mean of y"))
    with tmp_col[3]:
        std_x = float(st.text_input(label="$~\\rm X~$の標準偏差",value=1,key="std of x"))
        std_y = float(st.text_input(label="$~\\rm Y~$の標準偏差",value=1,key="std of y"))

        tmp_config_list = [f"データ数={size_int}"
                           ,f"相関係数={rho}"
                           ,f"データ『{d_name_x}』の平均 = {mu_x }"
                           ,f"データ『{d_name_x}』の標準偏差 = {std_x}"
                           ,f"データ『{d_name_y}』の平均 = {mu_y }"
                           ,f"データ『{d_name_x}』の標準偏差 = {std_y}"
                           ,"注意：左のデータの平均，標準偏差と若干異なる値を取ります．"
                           ] 
        tmp_config_df = pd.DataFrame(data=tmp_config_list,columns=["設定"])
        
    if st.button("生成されたデータの表示",key="button 2"):
        tmp_col = st.columns([1,1,1])
        tmp_x_array = np.random.normal(loc=0,scale=1,size=size_int)
        tmp_error_array = np.random.normal(loc=0,scale=1,size=size_int)
        tmp_y_array = rho * tmp_x_array  + (1 - rho ** 2) ** 0.5 * tmp_error_array

        tmp_x_name = str("Normalized ") + d_name_x
        tmp_y_name = str("Normalized ") + d_name_y
        df_normal = pd.DataFrame({f"{tmp_x_name}":tmp_x_array,f"{tmp_y_name}":tmp_y_array})


        out_x_array = mu_x + std_x*tmp_x_array
        out_y_array= mu_y + std_y*tmp_y_array
        df = pd.DataFrame({f"{d_name_x}":out_x_array,f"{d_name_y}":out_y_array})

        plt.clf()
        with tmp_col[0]:
            fig = sns.jointplot(x=f"{tmp_x_name}", y=f"{tmp_y_name}", color="C0",data=df_normal)
            st.pyplot(fig)

        plt.clf()
        with tmp_col[1]:
            bin_num = int(1 + np.log2(size_int))
            ax1 = df[d_name_x].plot.hist(bins=bin_num,rwidth=0.9,color="blue")
            st.pyplot(ax1.figure)  
            
        plt.clf()
        with tmp_col[2]:
            bin_num = int(1 + np.log2(size_int))
            ax2 = df[d_name_y].plot.hist(bins=bin_num,rwidth=0.9,color="orange")
            st.pyplot(ax2.figure)
            
            df_out = pd.concat([df_normal,df,tmp_config_df], axis=1)
            data_file = df_out.to_csv(index = False).encode('shift_jis')
            st.download_button(label="結果のダウンロード",data=data_file ,file_name="download_data.csv",mime="text/csv")
        st.info("""
                標準正規分布に従うデータ$~\\rm X~$を用いて，指定された相関係数となるようにデータ$~\\rm Y~$を生成しています．
                その後，指定された平均と標準偏差の正規分布となるようにデータ$~\\rm X~$と$~\\rm Y~$をそれぞれ正規化の逆の変換で生成しているため
                ダウンロードしたデータ$~\\rm X~$と$~\\rm Y~$の平均と標準偏差が指定の値と若干異な．"""
                )
        

st.header("4. 一様分布の複数列データ生成", divider="rainbow")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    row_num = int(st.text_input("データ数（行数）", value=10, key="row_num_multi"))
with col2:
    col_num = int(st.text_input("列数", value=3, key="col_num_multi"))
with col3:
    min_val = float(st.text_input("最小値", value=0, key="min_val_multi"))
with col4:
    max_val = float(st.text_input("最大値", value=10, key="max_val_multi"))

base_name = st.text_input("列名のベース（例：data → data1, data2...）", value="data", key="base_name_multi")

if max_val <= min_val:
    st.error("最小値 < 最大値となるように入力してください。")
    st.stop()

if st.button("データ生成（複数列）", key="generate_multi_uniform"):
    data = np.random.uniform(min_val, max_val, size=(row_num, col_num))
    col_names = [f"{base_name}{i+1}" for i in range(col_num)]
    df_multi = pd.DataFrame(data, columns=col_names)

    st.dataframe(df_multi)

    # グラフ表示：3列ずつ横並び
    for i in range(0, col_num, 3):
        sub_cols = st.columns(3)
        for j in range(3):
            if i + j < col_num:
                with sub_cols[j]:
                    fig, ax = plt.subplots()
                    df_multi[col_names[i + j]].plot.hist(bins=10, rwidth=0.9, ax=ax)
                    ax.set_title(col_names[i + j])
                    st.pyplot(fig)

    data_file = df_multi.to_csv(index=False).encode("shift_jis")
    st.download_button(label="CSVダウンロード", data=data_file, file_name="multi_uniform_data.csv", mime="text/csv")


st.header("5. 正規分布の複数列データ生成", divider="rainbow")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    row_num = int(st.text_input("データ数（行数）", value=10, key="row_num_normal"))
with col2:
    col_num = int(st.text_input("列数", value=3, key="col_num_normal"))
with col3:
    mean_val = float(st.text_input("平均", value=0, key="mean_val_normal"))
with col4:
    std_val = float(st.text_input("標準偏差", value=1, key="std_val_normal"))

base_name_norm = st.text_input("列名のベース（例：data → data1, data2...）", value="data", key="base_name_normal")

if std_val <= 0:
    st.error("標準偏差は0より大きくしてください。")
    st.stop()

if st.button("データ生成（正規分布, 複数列）", key="generate_multi_normal"):
    data = np.random.normal(mean_val, std_val, size=(row_num, col_num))
    col_names = [f"{base_name_norm}{i+1}" for i in range(col_num)]
    df_multi = pd.DataFrame(data, columns=col_names)

    st.dataframe(df_multi)

    # グラフ表示：3列ずつ横並び
    for i in range(0, col_num, 3):
        sub_cols = st.columns(3)
        for j in range(3):
            if i + j < col_num:
                with sub_cols[j]:
                    fig, ax = plt.subplots()
                    df_multi[col_names[i + j]].plot.hist(bins=10, rwidth=0.9, ax=ax)
                    ax.set_title(col_names[i + j])
                    st.pyplot(fig)

    data_file = df_multi.to_csv(index=False).encode("shift_jis")
    st.download_button(label="CSVダウンロード", data=data_file, file_name="multi_normal_data.csv", mime="text/csv")
