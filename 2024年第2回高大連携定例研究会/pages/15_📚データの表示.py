# ライブラリの読み込み
import streamlit as st
import pandas as pd
import numpy as np

#st: st.title を利用したテキスト表示
st.title("データの表示方法")

#st: Magic commandを利用したテキスト表示（Markdownのリンクや箇条書きの書き方を使用）
"""
ここでは，PandasのSeriesやDataFrameのような配列データを表示させる方法を紹介します．
なお，numpyのarray形式のデータも同様に表示することができます．

__参考資料__
- pandasのSeriesとDataFrameの取り扱いの詳細はこちらをご覧ください．  
    [Pandas Seriesを徹底解説！](https://ai-inter1.com/python-series/#st-toc-h-6)  
    [Pandas DataFrameを徹底解説！](https://ai-inter1.com/python-series/#st-toc-h-6)
- `st.dataframe`に関する詳細はこちらをご覧ください．  
    [API reference:dataframe](https://docs.streamlit.io/develop/api-reference/data/st.dataframe)
- `st.data_editor`に関する詳細はこちらをご覧ください．  
    [API reference:data_editor](https://docs.streamlit.io/develop/api-reference/data/st.data_editor)
"""

#st: st.header を利用した見出し表示
st.header("1. 配列データの表示",divider='rainbow')


### 表示用データの作成 ###
# 1行のリスト作成
data_1d_list = [1, 2, 3]
# リストをSeries形式へ変換
data_1d_df = pd.Series(data=data_1d_list
                       ,name="1列目"
                       ,index=["1行目","2行目","3行目"])
# 3行３列のリストを作成
data_2d_list = [[1  , 2  , 3]
             ,[11 , 12 , 13]
             ,[101, 102, 103]]
# 2次元的なリストをDataFrame形式へ変換
data_2d_df = pd.DataFrame( 
                        data=data_2d_list
                        ,columns=["1列目","2列目","3列目"]
                        ,index=["1行目","2行目","3行目"]
                        )


#st: Magic commandを利用したテキスト表示
"""
配列データの表示には主に`st.dataframe`を利用します．その表示結果は次の通りです．


"""

#st: st.columnsによる画面の２分割
# 1:1での分割は st.columns([1,1]) とする．

disp_col = st.columns([1,1])

# 画面左側 に表示させる内容
with disp_col[0]:
    """##### Series形式のデータの表示"""
    #st: Series形式のデータの表示
    st.dataframe(data_1d_df)

    if st.checkbox("ソースコード表示",key="data_show_code_disp1") :
        """"""
        st.code("""
                ##表示用データの作成##
                # 1行のリスト作成(デモデータ)
                data_1d_list = [1, 2, 3]
                # リストをSeries形式へ変換
                data_1d_df = pd.Series(data=data_1d_list
                                    ,name="1列目"
                                    ,index=["1行目","2行目","3行目"])
                
                ##データの表示##
                #st: st.dataframeによるデータの表示
                st.dataframe(data_1d_df)
                """
                , language="python")
        
# 画面右側 に表示させる内容
with disp_col[1]:
    """##### DataFrame形式のデータの表示"""
    #st: DataFrame形式のデータの表示
    st.dataframe(data_2d_df)

    if st.checkbox("ソースコード表示",key="data_show_code_disp2") :
        """"""
        st.code("""
                ##表示用データの作成##
                # 3行３列のリストを作成
                data_2d_list = [[1  , 2  , 3]
                            ,[11 , 12 , 13]
                            ,[101, 102, 103]]
                # 2次元的なリストをDataFrame形式へ変換
                data_2d_df = pd.DataFrame( 
                                        data=data_2d_list
                                        ,columns=["1列目","2列目","3列目"]
                                        ,index=["1行目","2行目","3行目"]
                                        )
                
                ##データの表示##
                #st: st.dataframeによるデータの表示
                st.dataframe(data_2d_df)
                """
                , language="python")

"""___"""
#st: st.header を利用した見出し表示
st.header("2. 配列データの表示(編集可能な表示方法)",divider='rainbow')
"""
`st.data_editor`を使用することで，表示された表を編集することができます．
また，変数されたデータを利用した処理も可能です．
`st.data_editor`の使用例は次の通りです．

"""
### 表示用データの作成 ###
# 3行４列のリストを作成
data_2d_list = [
                 [0  , 0  , 0]
                ,[0  , 0  , 0]
                ,[0  , 0  , 0]
                ,[0  , 0  , 0]
             ]
# 2次元的なリストをDataFrame形式へ変換
data_2d_df = pd.DataFrame( 
                        data=data_2d_list
                        ,columns=["1列目","2列目","3列目"]
                        ,index=["1行目","2行目","3行目","4行目"]
                        )
##データの表示##
##編集後のデータを利用した計算のデモンストレーション
#st: st.columnsによる画面の3分割
# 2:1:1での分割は st.columns([2,1,1]) とする．
disp_col2 = st.columns([2,1,1])

# 画面左側 に表示させる内容
with disp_col2[0]:
    #st: data_editorによる編集可能なデータの表示
    data_2d_df_new = st.data_editor(data_2d_df)
    
# 画面中央 に表示させる内容
with disp_col2[1]:
    # f文字列（フォーマット済み文字列リテラル）を利用した計算結果の表示
    st.write( f"1列目の総和$={ data_2d_df_new['1列目'].sum() }$" )
    st.write( f"2列目の総和$={ data_2d_df_new['2列目'].sum() }$" )
    st.write( f"3列目の総和$={ data_2d_df_new['3列目'].sum() }$" )

# 画面右側 に表示させる内容
with disp_col2[2]:
    # f文字列（フォーマット済み文字列リテラル）を利用した計算結果の表示
    st.write( f"1行目の総和$={ data_2d_df_new.transpose()['1行目'].sum() }$" )
    st.write( f"2行目の総和$={ data_2d_df_new.transpose()['2行目'].sum() }$" )
    st.write( f"3行目の総和$={ data_2d_df_new.transpose()['3行目'].sum() }$" )
    st.write( f"4行目の総和$={ data_2d_df_new.transpose()['4行目'].sum() }$" )

if st.checkbox("ソースコード表示",key="data_show_code_disp3") :
    """"""
    st.code("""
            ### 表示用データの作成 ###
            # 3行４列のリストを作成
            data_2d_list = [
                            [0  , 0  , 0]
                            ,[0  , 0  , 0]
                            ,[0  , 0  , 0]
                            ,[0  , 0  , 0]
                        ]
            # 2次元的なリストをDataFrame形式へ変換
            data_2d_df = pd.DataFrame( 
                                    data=data_2d_list
                                    ,columns=["1列目","2列目","3列目"]
                                    ,index=["1行目","2行目","3行目","4行目"]
                                    )
            ##データの表示##
            #st: data_editorによる編集可能なデータの表示
            # data_2d_df_new に編集後のデータが格納される．
            data_2d_df_new = st.data_editor(data_2d_df)
            """
            , language="python")
