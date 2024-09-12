import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


"""## クロス集計"""

tub_dict = {"デモデータによる分析体験":0,"ユーザーデータによる分析":1}
selected_cbox = st.radio(label="選択", options = tub_dict.keys(),horizontal=True)
"""___"""

# tub_list = st.tabs(tub_dict.keys())

###  デモデータによる分析体験
tub_counta = 0
if tub_dict[selected_cbox] == 0 :
    tub_title = list(tub_dict.keys())[tub_counta]
# with tub_list[0]:
    f"""### {tub_title }"""
    """
    #### 1. 分析データの選択
    """
    select_data_dict = {"デモデータ1 降水量のデータ":0}
    select_str = st.selectbox("分析に使用するデータを選択してください．",select_data_dict.keys())

    check_num  = 0
    if select_data_dict[select_str] == 0:
        try :
            data_df = pd.read_csv("sample_datas/cross_data01.csv",encoding='shift_jis')
        except:
            data_df = pd.read_csv("2024年第2回高大連携定例研究会/sample_datas/cross_data01.csv",encoding='shift_jis')

        check_num = 1


    if check_num == 1:
        st.write("データの表示")
        st.dataframe(data_df )
    """___"""


    
    """
    #### 2. クロス集計(多重クロス集計)の実行
    """
    keys_list = list(data_df.keys())
    input_col = st.columns([1,1,1])
    with input_col[0]:
        index_list = st.multiselect("表側として利用するデータを選択",keys_list,key="1" )
    with input_col[1]:
        columns_list = st.multiselect("表頭として利用するデータを選択",keys_list,key="2" ) 
    with input_col[2]:
        values_list = st.multiselect("集計するデータを選択",keys_list,key="3" ) 


    if st.button("クロス集計の実行",key="button 1"):
        # エラーチェック
        if not index_list:
            st.error('表側となるデータが指定されていません', icon="⚠️")
            st.stop()
        if not columns_list:
            st.error('表頭となるデータが指定されていません', icon="⚠️")
            st.stop() 
        if not values_list:
            st.error('集計されるデータが指定されていません', icon="⚠️")
            st.stop()

        if len(set(index_list) & set(columns_list)) != 0:
            st.error('同じデータを表側，表頭で用いています．表側，表頭は別のデータを用いるように設定を変更してください．', icon="⚠️")
            st.stop()
        if len(set(index_list) & set(values_list)) != 0:
            st.error('同じデータを表側，集計で用いています．表側，集計は別のデータを用いるように設定を変更してください．', icon="⚠️")
            st.stop()
        if len(set(columns_list) & set(values_list)) != 0:
            st.error('同じデータを表頭，集計で用いています．表頭，集計は別のデータを用いるように設定を変更してください．', icon="⚠️")
            st.stop()

        """#### 集計結果"""
        cross_df = data_df.pivot_table(index=index_list,columns=columns_list,values=values_list)
        st.table(cross_df )
        downloadfile_csv = cross_df.to_csv().encode('shift_jis')
        st.download_button(label="集計結果のダウンロード",data=downloadfile_csv ,file_name="outfile_cross.csv",mime="text/csv")


### ユーザーデータによる分析
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
# with tub_list[1]:
    f"""### {tub_title }"""
    """
    #### 1. 分析データのアップロード
    """
    uploaded_files = st.file_uploader("CSVファイルをアップロードしてください．")    
    if not uploaded_files:
        st.error('データがアップロードされていません', icon="⚠️")
        st.stop()
    
    else :
        data_df = pd.read_csv(uploaded_files,encoding='shift_jis')
        check_num = 1

    if check_num == 1:
        st.write("データの表示")
        st.dataframe(data_df )
    """___"""


    
    """
    #### 2. クロス集計(多重クロス集計)の実行
    """
    keys_list = list(data_df.keys())
    input_col = st.columns([1,1,1])
    with input_col[0]:
        index_list = st.multiselect("表側として利用するデータを選択",keys_list ,key="4")
    with input_col[1]:
        columns_list = st.multiselect("表頭として利用するデータを選択",keys_list ,key="5") 
    with input_col[2]:
        values_list = st.multiselect("集計するデータを選択",keys_list ,key="6") 


    if st.button("クロス集計の実行",key="button 2"):
        # エラーチェック
        if not index_list:
            st.error('表側となるデータが指定されていません', icon="⚠️")
            st.stop()
        if not columns_list:
            st.error('表頭となるデータが指定されていません', icon="⚠️")
            st.stop() 
        if not values_list:
            st.error('集計されるデータが指定されていません', icon="⚠️")
            st.stop()

        if len(set(index_list) & set(columns_list)) != 0:
            st.error('同じデータを表側，表頭で用いています．表側，表頭は別のデータを用いるように設定を変更してください．', icon="⚠️")
            st.stop()
        if len(set(index_list) & set(values_list)) != 0:
            st.error('同じデータを表側，集計で用いています．表側，集計は別のデータを用いるように設定を変更してください．', icon="⚠️")
            st.stop()
        if len(set(columns_list) & set(values_list)) != 0:
            st.error('同じデータを表頭，集計で用いています．表頭，集計は別のデータを用いるように設定を変更してください．', icon="⚠️")
            st.stop()

        """#### 集計結果"""
        cross_df = data_df.pivot_table(index=index_list,columns=columns_list,values=values_list)
        st.table(cross_df )
        downloadfile_csv = cross_df.to_csv().encode('shift_jis')
        st.download_button(label="集計結果のダウンロード",data=downloadfile_csv ,file_name="outfile_cross.csv",mime="text/csv")