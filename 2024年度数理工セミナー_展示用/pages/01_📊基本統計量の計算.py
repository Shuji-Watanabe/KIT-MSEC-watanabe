import streamlit as st
import pandas as pd
import numpy as np


def compute_statistics(pd_dataframe):
    return{"データ数":int(pd_dataframe.count())
           ,"総和":float(pd_dataframe.sum())
           ,"平均":float(pd_dataframe.mean())
               ,"":float(pd_dataframe.max())
           ,"":float(pd_dataframe.min())
           ,"":float(pd_dataframe.median())
           ,"":float(pd_dataframe.var())   
           ,"":float(pd_dataframe.std())

           ,"四分位数":pd_dataframe.quantile([0.25,0.5,0.75]).transpose()
           }

#-------------header begin-----------------------------------------------------
st.title("基本統計量の計算")
st.header("説明",divider="rainbow")
"""
このページでは，データの基本的な統計量を計算します．計算される量は次のとおりです．
|データ数|合計値|最大値|最小値|
|---|---|---|---|
|データ数|合計値|最大値|最小値|
|分散|標準偏差|||
|中央値|第一四分位数|第二四分位数|第三四分位数|
"""
"""左側にあるサイドバーで分析に使用するデータを選択してください．選択肢は次の2つです．
- **分析体験でもデータ**\n
    事前に用意されたデータを使用し，このアプリで何ができるのか体験することができます．
- **ユーザーデータ**\n
    ユーザーが用意したデータに基づき，データ分析を行います．分析に使用するCSVファイルをアップロードしてください．
    CSVファイルは次の形式に従って作成してください．
    - データの方向は列（縦に測定値が並びます）
    - 1行目：データ名
    - 2行目以降：データ
"""
st.sidebar.markdown("分析に使用するデータの選択")
tub_dict = {"分析体験デモデータ":0,"ユーザーデータ":1}
selected_cbox = st.sidebar.radio(label="選択", options = tub_dict.keys(),horizontal=True)
""" """
#-------------header end-------------------------------------------------------


#===============================================================================================
###  デモデータによる分析体験
tub_counta = 0
if tub_dict[selected_cbox] == 0 :
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[0]:
    st.header(f"""{tub_title }を用いた分析""",divider="rainbow")
    """   """
    st.subheader(f"Step１: 分析データの選択", divider="green")
    input_col = st.columns([2,1])
    select_data_dict = {"デモデータ１":0}

    with input_col[0]:
        # 分析データの選択
        select_str = st.selectbox("分析するデータを選択してください",select_data_dict.keys(),key="mselect 01")

        # データの読み込み
        if select_data_dict[select_str] == 0:
            #デモデータ『hist_data01.csv』の読み込み 
            try :
                read_data_df = pd.read_csv("sample_datas/scatter_data01.csv",encoding='shift_jis')
            except:
                read_data_df = pd.read_csv("2024年第2回高大連携定例研究会/sample_datas/scatter_data01.csv",encoding='shift_jis')
        else :
            st.stop()

        # 分析データ列の選択
        keys_list = list(read_data_df.keys())
        index_str = st.selectbox("データ列を１つ選択",keys_list,key="mselect 02")

    with input_col[1]:
        data_df = read_data_df[index_str]
        st.dataframe(data_df
                        , use_container_width=True
                        , height=200)

    """___"""

    st.subheader(f"Step２: 基本統計量の計算", divider="green")

    if st.button("計算の実行",key="button 01"):
        ndata_int = int(data_df.count())
        sum_f = float(data_df.sum())
        mean_f = float(data_df.mean())
        var_f = float(data_df.var())
        med_f = float(data_df.median())
        stdev_f = float(data_df.std())
        max_f = float(data_df.max())
        min_f = float(data_df.min())
        quantile_list = data_df.quantile([0.25,0.5,0.75]).transpose()
        # 計算結果の表示
        disp_col1 = st.columns(4)
        disp_col1[0].metric(label="データ数",value=ndata_int)
        disp_col1[1].metric(label="合計",value=sum_f)
        disp_col1[2].metric(label="最大値",value=max_f)
        disp_col1[3].metric(label="最小値",value=min_f)
        """___"""
        disp_col2 = st.columns(4)
        disp_col2[0].metric(label="平均 ",value=f"{mean_f:4.1f}")
        disp_col2[1].metric(label="標準偏差",value=f"{stdev_f:4.1f}")
        """___"""
        disp_col3 = st.columns(4)
        disp_col3[0].metric(label="中央値 ",value=f"{med_f:4.1f}")
        disp_col3[1].metric(label="第一四分位数",value=f"{float(quantile_list[0.25]):4.1f}")
        disp_col3[2].metric(label="第二四分位数",value=f"{float(quantile_list[0.5]):4.1f}")
        disp_col3[3].metric(label="第三四分位数",value=f"{float(quantile_list[0.75]):4.1f}")
        """___"""


#===============================================================================================
###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
    # with tub_list[1]:
    st.header(f"""{tub_title }を用いた分析""",divider="rainbow")
    """   """
    st.subheader(f"Step１: 分析データのアップロード", divider="green")
    
    disp_col0 = st.columns([1,1])
    with disp_col0[0]:
        st.warning("データをアップロードする前に，アップロードするデータに個人情報等，取扱に注意しなければならないデータが含まれていないか確認してください．")
        tmp_check = st.checkbox("確認しました．")
    with disp_col0[1]:
        if tmp_check:
            uploaded_files = st.file_uploader("CSVファイルをアップロードしてください．")    
            if not uploaded_files:
                st.error('データがアップロードされていません', icon="⚠️")
                st.stop()
        else :
            st.write("停止中")
            st.stop()

    st.divider()
    disp_upload_col = st.columns([1,1])
    set_encode_list = ["自動","選択","入力"]
    with disp_upload_col[0]:
        selected_way = st.radio("エンコードの指定方法",options=set_encode_list,horizontal=True)
    with disp_upload_col[1]:
        import lib.FileProcessing as FileProcessing 
        read_data_df= FileProcessing.streamlit_uploaded_csv(st_uploaded_files=uploaded_files,selected_type=selected_way)

    st.divider()
    # 分析データ列の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([2,1])
    with input_col[0]:
        index_str = st.selectbox("データの選択",keys_list  ,key="mselect 03")
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else :
            st.success(f'準備完了', icon="✅")
    with input_col[1]:
        data_df = read_data_df[index_str]
        data_len = data_df.shape[0]
        st.write("")
        if st.checkbox("データの確認",key="cbox 02"):
            st.dataframe(data_df
                         , use_container_width=True
                         , height=200)
        st.divider()




    st.subheader(f"Step２: 基本統計量の計算", divider="green")
    if st.button("計算の実行",key="button 01"):
        with st.spinner('作成中'):
            
            # 計算結果の表示
            disp_col1 = st.columns(4)
            disp_col1[0].metric(label="データ数",value=ndata_int)
            disp_col1[1].metric(label="合計",value=sum_f)
            disp_col1[2].metric(label="最大値",value=max_f)
            disp_col1[3].metric(label="最小値",value=min_f)
            """___"""
            disp_col2 = st.columns(4)
            disp_col2[0].metric(label="平均 ",value=f"{mean_f:4.1f}")
            disp_col2[1].metric(label="標準偏差",value=f"{stdev_f:4.1f}")
            """___"""
            disp_col3 = st.columns(4)
            disp_col3[0].metric(label="中央値 ",value=f"{med_f:4.1f}")
            disp_col3[1].metric(label="第一四分位数",value=f"{float(quantile_list[0.25]):4.1f}")
            disp_col3[2].metric(label="第二四分位数",value=f"{float(quantile_list[0.5]):4.1f}")
            disp_col3[3].metric(label="第三四分位数",value=f"{float(quantile_list[0.75]):4.1f}")
            """___"""


# import streamlit as st
# import pandas as pd

# def compute_statistics(data):
#     """データの基本統計量を計算する"""
#     return {
#         "データ数": data.count(),
#         "合計": data.sum(),
#         "最大値": data.max(),
#         "最小値": data.min(),
#         "平均": data.mean(),
#         "標準偏差": data.std(),
#         "中央値": data.median(),
#         "第一四分位数": data.quantile(0.25),
#         "第二四分位数": data.quantile(0.5),
#         "第三四分位数": data.quantile(0.75),
#     }

# st.set_page_config(page_title="基本統計量の計算", layout="wide")
# st.title("📊 基本統計量の計算")

# st.sidebar.header("データの選択")
# options = {"分析体験デモデータ": 0, "ユーザーデータ": 1}
# selected_option = st.sidebar.radio("選択", options.keys())

# col_main, col_side = st.columns([3, 1])

# with col_main:
#     if selected_option == "分析体験デモデータ":
#         st.subheader("デモデータを用いた分析", divider="rainbow")
#         demo_data = {"デモデータ1": "sample_datas/scatter_data01.csv"}
#         selected_data = st.selectbox("分析するデータを選択してください", demo_data.keys())
        
#         try:
#             df = pd.read_csv(demo_data[selected_data], encoding='shift_jis')
#         except Exception as e:
#             st.error(f"データの読み込みに失敗しました: {e}")
#             st.stop()
        
#         column = st.selectbox("データ列を選択", df.columns)
#         data = df[column]
#         st.dataframe(df, use_container_width=True, height=300)
        
#         st.subheader("📊 基本統計量の計算", divider="green")
#         if st.button("計算の実行", use_container_width=True):
#             stats = compute_statistics(data)
#             for key, value in stats.items():
#                 st.metric(label=key, value=f"{value:.2f}")
    
#     else:
#         st.subheader("ユーザーデータを用いた分析", divider="rainbow")
#         with st.expander("アップロード前の確認"):
#             st.warning("個人情報が含まれていないか確認してください。")
#             confirm = st.checkbox("確認しました。")
        
#         if not confirm:
#             st.stop()
        
#         uploaded_file = st.file_uploader("CSVファイルをアップロードしてください。", type=["csv"])
#         if not uploaded_file:
#             st.error("データがアップロードされていません", icon="⚠️")
#             st.stop()
        
#         df = pd.read_csv(uploaded_file)
#         column = st.selectbox("データの選択", df.columns)
#         data = df[column]
        
#         if st.checkbox("データの確認"):
#             st.dataframe(df, use_container_width=True, height=300)
        
#         st.subheader("📊 基本統計量の計算", divider="green")
#         if st.button("計算の実行", use_container_width=True):
#             with st.spinner('計算中...'):
#                 stats = compute_statistics(data)
#                 for key, value in stats.items():
#                     st.metric(label=key, value=f"{value:.2f}")

# with col_side:
#     st.image("https://via.placeholder.com/250", caption="統計分析ツール", use_container_width=True)

