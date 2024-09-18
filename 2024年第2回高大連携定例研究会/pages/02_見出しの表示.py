# ライブラリの読み込み
import streamlit as st

#st: Magic commandを利用したテキスト表示
"""
# 見出しの表示方法  

streamlitで使える見出しの表示方法を紹介します．

"""

#st: st.header を利用した見出し表示
st.header("1. st.title を利用した見出し",divider='rainbow')

#st: Magic commandを利用したテキスト表示
"""
下の見出しは `st.title` を使用して表示しています．
"""
#st: st.title を利用したテキスト表示
st.title("見出し１：titleの使用")


#st: st.title を利用したテキスト表示のソースコードを表示させる
if st.checkbox("ソースコード表示",key="titile_code_disp") :
    st.code("""
            #st: st.title を利用したテキスト表示
            st.title("見出し１：titleの使用")
            """, language="python")
    
    """
    __参考資料__  
    - `st.title`に関する詳細はこちらをご覧ください．  
        [ API reference:title ]( https://docs.streamlit.io/develop/api-reference/text/st.title )
    """
"""___"""

#st: st.header を利用した見出し表示
st.header("2. Magic commandを利用した見出し",divider='rainbow')

"""
下の見出しは Magic command を使用して表示しています．
"""
#st: Magic commandを利用したテキスト表示
"""
#  見出し２：Magic commandの使用
"""

#st: Magic command　を利用したテキスト表示のソースコードを表示させる
if st.checkbox("ソースコード表示",key="titile_magic_code_disp") :
    st.code("""
            #st: Magic commandを利用したテキスト表示
            \"\"\"
            #  見出し２：Magic commandの使用
            \"\"\"
            """
            , language="python")
    """
    この文章中のハッシュ『#』はMarkdown記法における見出しの書き方です．
    ハッシュを入力し、半角スペースを空けて文字を入力すると見出しとして表示されます．
    また，ハッシュの後に必ずハッシュの数が増えると文字が小さくなります．
    """


"""___"""
