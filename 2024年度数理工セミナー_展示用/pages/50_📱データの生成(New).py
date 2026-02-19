import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import os 
path = os.getcwd()

#### データの作成とその表示
def generate_bernoulli_trials_sets(p: float, n: int, m: int, seed: int | None = None) -> pd.DataFrame:
    """
    成功確率 p のベルヌーイ試行を n 回行う操作を1セットとして，これを m セット行う．
    返り値：set_id（1..m）, trial_id（1..n）, outcome（0/1）
    """
    if not (0 <= p <= 1):
        raise ValueError("p は 0 以上 1 以下で指定してください。")
    if n <= 0 or m <= 0:
        raise ValueError("n と m は 1 以上で指定してください。")

    rng = np.random.default_rng(seed)
    outcomes = rng.binomial(1, p, size=(m, n))

    df = pd.DataFrame({
        "set_id": np.repeat(np.arange(1, m + 1), n),
        "trial_id": np.tile(np.arange(1, n + 1), m),
        "outcome": outcomes.reshape(-1)
    })
    return df


def data_download(index, col_name, data_array, ntri=10):
    """
    index==2: data_array は DataFrame(set_id, trial_id, outcome) を想定
      - 表示：成功回数 k=0..ntri の度数（セット数）を棒グラフ
      - 返す df：ダウンロード用に生データ（3列）を返す

    index==1: data_array は DataFrame(mean, std, data) を想定
      - 表示：data列のヒストグラム
      - 返す df：ダウンロード用に生データ（3列）を返す
    """
    if index == 2:
        df = data_array.copy()

        success_per_set = df.groupby("set_id")["outcome"].sum().to_numpy()
        freq, _ = np.histogram(success_per_set, bins=np.arange(0, ntri + 2))
        k = np.arange(0, ntri + 1)

        show_df = pd.DataFrame({
            "k": k,
            "freq": freq,
            "rfreq": freq / len(success_per_set)
        })

        ax = show_df.set_index("k")["freq"].plot.bar()
        ax.set_xlabel("成功回数 k")
        ax.set_ylabel("度数（セット数）")
        return df, ax

    elif index == 1 and isinstance(data_array, pd.DataFrame):
        # 正規分布：3列（mean, std, data）
        df = data_array.copy()

        # ヒストグラムは「データ」列で描く（列名が data である前提）
        if "data" not in df.columns:
            raise ValueError("index==1 の data_array には 'data' 列が必要です。")

        bin_num = int(1 + np.log2(len(df))) if len(df) > 1 else 1
        ax = df["data"].plot.hist(bins=bin_num, rwidth=0.9)

        return df, ax

    else:
        # 1列データ（従来通り）
        bin_num = int(1 + np.log2(len(data_array))) if len(data_array) > 1 else 1
        df = pd.DataFrame(data=data_array, columns=[col_name])
        ax = df.plot.hist(bins=bin_num, rwidth=0.9)
        return df, ax


def disp_function(index,tmp_array,col_name,ntri=10):
    if st.button("生成されたデータの表示"):
            data_df , ax  = data_download(index,col_name,tmp_array,ntri)
            tmp_result_col = st.columns([2,1])
            with tmp_result_col[0]:
                st.pyplot(ax.figure) 
            with tmp_result_col[1]:
                st.dataframe(data_df)
                data_file = data_df.to_csv().encode('utf-8')
                # data_file = data_df.to_csv().encode('shift_jis')
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

type_dict = {"一様分布":0
             ,"正規分布":1
             ,"二項分布":2
             ,"ポアソン分布":3
            #  ,"t 分布" :4
            #  ,"カイ２乗分布":5
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


    if tmp_index == 0:
        """
        $~\\text{最小値} \\le x \\le \\text{最大値}~$の範囲の$\\text{整数}$を，一様な確率で，指定されたデータ数で生成します．
        """
        tmp_col = st.columns([1,1,1,1])
        with tmp_col[0]:
            size_int = int(st.text_input(label="データ数",value=10))
        with tmp_col[1]: 
            init_num = int(st.text_input(label="最小値",value=0))
        with tmp_col[2]: 
            end_num = int(st.text_input(label="最大値",value=10))+1
        if end_num <= init_num :
            st.error("最小値＜最大値となるように入力してください．")
            st.stop()
        tmp_data_array = np.random.randint(init_num,end_num,size=size_int)

    elif tmp_index == 1:
        """
        $~\\text{最小値} \\le x \\le \\text{最大値}~$の範囲の$\\text{実数}$を，一様な確率で，指定されたデータ数で生成します
        """
        tmp_col = st.columns([1,1,1,1])
        with tmp_col[0]:
            size_int = int(st.text_input(label="データ数",value=10))
        with tmp_col[1]: 
            init_num = int(st.text_input(label="最小値",value=0))
        with tmp_col[2]: 
            end_num = int(st.text_input(label="最大値",value=10))+1
        
        if end_num <= init_num :
            st.error("最小値＜最大値となるように入力してください．")
            st.stop()
        tmp_data_array = np.random.uniform(init_num,end_num,size=size_int)
    tmp_col_name = "data"
    disp_function(index=selected_type_index, col_name=tmp_col_name, tmp_array=tmp_data_array)

elif selected_type_index == 1:
    r"""
    平均 $\mu$ と標準偏差 $\sigma$ で定まる正規分布に従う乱数データを1つのデータ列として，これを $n$ 個生成します．
    生成データは（平均，標準偏差，データ）で構成されます．
    """
    tmp_col = st.columns([1, 1, 1, 1])
    with tmp_col[0]:
        mean_num = float(st.text_input(label="平均 $\mu$", value=0))
    with tmp_col[1]:
        std_num = float(st.text_input(label="標準偏差 $\sigma$", value=1))
    with tmp_col[2]:
        size_int = int(st.text_input(label="データ数 $n$", value=10))
    tmp_col_name = "データ"
    # 生データ（3列）を作る：mean, std, data
    data = np.random.normal(mean_num, std_num, size_int)

    mean_col = [""] * size_int
    std_col  = [""] * size_int
    mean_col[0] = mean_num
    std_col[0]  = std_num

    tmp_data_array = pd.DataFrame({
        "mean": mean_col,     # 1行目だけ数値、2行目以降は空白
        "std":  std_col,      # 1行目だけ数値、2行目以降は空白
        "data": data
    })

    disp_function(index=selected_type_index, col_name=tmp_col_name, tmp_array=tmp_data_array)

elif selected_type_index == 2:
    r"""
    成功確率 $p$ のベルヌーイ試行を $n$ 回行う操作を1セットとして，これを $m$ セット行ったデータを生成します．
    生成データは（セット番号，試行番号，成功/失敗）で構成されます．
    """
    tmp_col = st.columns([1, 1, 1, 1])


    with tmp_col[0]:
        p_num = float(st.text_input(label="成功確率 $p$", value=0.5))
    with tmp_col[1]:
        trials_num = int(st.text_input(label="試行回数 $n$", value=10))
    with tmp_col[2]:
        set_num = int(st.text_input(label="セット数 $m$", value=100))

    if not (0 <= p_num <= 1):
        st.error("成功確率は0から1の範囲で指定してください．")
        st.stop()
    if trials_num <= 0 or set_num <= 0:
        st.error("試行回数とセット数は1以上で指定してください．")
        st.stop()

    # 3列の生データ（set_id, trial_id, outcome）
    tmp_data_array = generate_bernoulli_trials_sets(p=p_num, n=trials_num, m=set_num)
    # ntri に trials_num を渡す（成功回数の範囲 0..n）
    disp_function(index=selected_type_index, col_name=tmp_col_name, tmp_array=tmp_data_array, ntri=trials_num)

    
elif selected_type_index == 3:
    """
    指定された発生率（$\lambda$）をもつポアソン分布に従う乱数データを，指定した個数だけ生成します．
    """
    tmp_col = st.columns([1,1,1,1])
    with tmp_col[0]:
        tmp_col_name = str(st.text_input("データ名",value="data 1"))
    with tmp_col[1]:
        size_int = int(st.text_input(label="データ数",value=10))
    with tmp_col[2]: 
        p_num = float(st.text_input(label="発生率",value=1.2))
    tmp_data_array = np.random.poisson(p_num, size=(size_int, 1))
    disp_function(index=selected_type_index,tmp_array=tmp_data_array )

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

tmp_col = st.columns([1,1,1,1,1]) 
if selected_type_index == 1:
    with tmp_col[0]:
        size_int = int(st.text_input(label="サンプル数",value= 500,key="sample size"))
    with tmp_col[1]:
        rho = float(st.number_input(label="相関係数$~\\rho~$",min_value=-1.0,max_value=1.0,value=0.75)) 
    with tmp_col[2]: 
        d_name_x = st.text_input(label="$~\\rm X~$の名前",value="data X",key="data name of x")
        d_name_y = st.text_input(label="$~\\rm Y~$の名前",value="data Y",key="data name of y")
    with tmp_col[3]: 
        mu_x = float(st.text_input(label="$~\\rm X~$の平均",value=0,key="mean of x"))
        mu_y = float(st.text_input(label="$~\\rm Y~$の平均",value=0,key="mean of y"))
    with tmp_col[4]:
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
               ダウンロードしたデータの$~\\rm X~$と$~\\rm Y~$の平均と標準偏差，そして相関係数は指定した値と若干異なります．"""
                )