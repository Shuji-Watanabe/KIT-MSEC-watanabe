# ライブラリの読み込み
import streamlit as st

#st: Magic commandを利用したテキスト表示
"""
# 様々なテキストの表示方法  

_streamlit_ で使えるテキストの表示方法を紹介します．
_streamlit_ でテキストの修飾を行いたい場合，基本的には 
[_Markdown_ 記法](https://help.qast.jp/ja/articles/9026060-markdown記法で装飾する) 
に従った書き方で修飾が可能です．
"""

#st: st.header を利用した見出し表示
st.header("st.title を利用した見出し",divider='rainbow')

#st: Magic commandを利用したテキスト表示
"""
下の見出しは `st.title` を使用して表示しています．
"""
#st: st.title を利用したテキスト表示
st.title("文章表示のあれこれ")
#st: st.title を利用したテキスト表示のソースコードを表示させる
if st.checkbox("ソースコード表示",key="titile_code_disp") :
    title_code = """
    st.title("文章表示のあれこれ")
    """
    st.code(title_code, language="python")
    """
    この機能の説明はこちらから（[ API reference ](https://docs.streamlit.io/develop/api-reference/text/st.title)）
    """

#st: st.header を利用した見出し表示
st.header("Magic commandを利用した見出し",divider='rainbow')

#st: Magic commandを利用したテキスト表示
"""
下の見出しは
[ _Magic command_ ](https://docs.streamlit.io/develop/api-reference/write-magic/magic)
を使用して表示しています．

#  文章表示のあれこれ

これは streamlit 特有の記法です．
表示したい文章をトリプルクォーテーション（\"\"\"）で囲むことで，Webアプリ上に文字列が
表示されます．
"""

#st: Magic command　を利用したテキスト表示のソースコードを表示させる
if st.checkbox("ソースコード表示",key="titile_magic_code_disp") :
    title_magic_code ="""
    \"\"\"
    #  文章表示のあれこれ
    \"\"\"
    """
    st.code(title_magic_code, language="python")
    """
    この文章中のハッシュ『#』はMarkdown記法における見出しの書き方です．
    ハッシュを入力し、半角スペースを空けて文字を入力すると見出しとして表示されます．
    また，ハッシュの後に必ずハッシュの数が増えると文字が小さくなります．
    """