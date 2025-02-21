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
st.title("データの生成")
"""
ここでは，分析の演習で使用するためのデモデータの生成を行います．
"""
st.divider()

### サンプルデータの生成 : １次配列###
st.header(":desktop_computer: 分析データの生成：１次配列",divider="rainbow")
np.set_printoptions(precision=5)

type_dict = {"一様分布に従うデータ":0
             ,"正規分布に従うデータ":1
             }

type_keys = type_dict.keys()
selected_type = st.selectbox(label="生成するデータの分布をしていしてください．",options=type_keys, key="makedata1")
selected_type_index = type_dict[ selected_type ]
""" """
""" """


f"""#### {selected_type}の生成（$n$行$1$列）"""


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
st.header(f":desktop_computer: 相関がある２つデータの生成",divider="rainbow")
np.set_printoptions(precision=5)

type_dict = {"正規分布に従うデータ":1}

type_keys = type_dict.keys()
selected_type = "正規分布に従うデータ"
selected_type_index = type_dict[ selected_type ]
""" """
""" """
"""
- **データ$~X~$** \n
    平均 $~\\mu_{\\rm x}~$，標準偏差$~\\sigma_{\\rm x}~$の正規分布に従うサンプル数$~n~$のデータ
- **データ$~Y~$** \n
    平均 $~\\mu_{\\rm y}~$，標準偏差$~\\sigma_{\\rm y}~$に正規分布に従うサンプル数$~n~$のデータ
- **データ$~X~,\ ~Y~$の関係** \n
    相関係数=$~\\rho~$
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