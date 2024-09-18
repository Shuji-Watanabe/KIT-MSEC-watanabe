# ライブラリの読み込み
import streamlit as st

"""
# 文章の表示  
"""
"""
streamlitで使えるテキストの表示方法を紹介します．
streamlitでテキストの修飾を行いたい場合，基本的には 
[Markdown記法](https://help.qast.jp/ja/articles/9026060-markdown記法で装飾する) 
に従った書き方で修飾が可能です．
"""

#st: st.header を利用した見出し表示（後述）
st.header("1. st.write を利用した文章の表示",divider='rainbow')
"""
基本的な文章表示方法の一つが`st.write`による表示方法です．
その一例を示します．

`st.write`は文字列以外にも，DataFrameの表示や画像の表示，図の表示など様々な表示に使用できます．

__参考資料__
- st.writeに関する詳細はこちらをご覧ください．  
    [ API reference:write ](https://docs.streamlit.io/develop/api-reference/write-magic/st.write)
- f文字列に関する詳細はこちらをご覧ください．  
    [ note.nkmk.me: Pythonのf文字列（フォーマット済み文字列リテラル）の使い方](https://note.nkmk.me/python-f-strings/)
___
"""

#st: st.write を利用した文章表示（短文の場合）
st.write("これは`st.write`を使用した文章表示です．")
if st.checkbox("ソースコード表示",key="code_disp1") :
    st.code("""
            #st: st.write を利用した文章表示（短文の場合）
            st.write("これは`st.write`を使用した文章表示です．")
            """, language="python")
"""___"""

#st: st.writeを利用した文章表示（比較的長い場合）
st.write("""
         比較的長い文章の場合はトリプルクォーテーション(\"\"\")で囲むと改行しながら文章を入力できるため，修正等がしやすいです．
         
         Markdown記法に従って記述してください．
         
         トリプルクォーテーションの中に文字列としてトリプルクォーテーションを入れる場合
         バックスラッシュ『\\』によるエスケープが必要です.
         トリプルクォーテーションの中で『\\\\"\\\\"\\\\"』と入力すると，
         『\"\"\"』が文字列として扱われます．
         シングルクォーテーション中にシングルクォーテーションを
         入れる場合も同様です．
        """)
if st.checkbox("ソースコード表示",key="code_disp2") :
    st.code("""
            #st: st.writeを利用した文章表示（比較的長い場合）
            st.write(\"\"\"
                    比較的長い文章の場合はトリプルクォーテーション(\"\"\")で囲むと改行しながら文章を入力できるため，修正等がしやすいです．
            
                    Markdown記法に従って記述してください．

                    トリプルクォーテーションの中に文字列としてトリプルクォーテーションを入れる場合
                    バックスラッシュ『\\』によるエスケープが必要です.
                    トリプルクォーテーションの中で『\\"\\"\\"』と入力すると，
                    『\"\"\"』が文字列として扱われます．シングルクォーテーション中にシングルクォーテーションを
                    入れる場合も同様です．
                    \"\"\")
            """, language="python")
"""___"""

"""
応用的な話ですが，文字列中に計算結果などを入れたい場合はf文字列を使用します．
"""
# result に数値を格納します．
result = 1.4142

#st: st.writeを利用した文章表示（f文字列（f-strings、フォーマット文字列、フォーマット済み文字列リテラルとも呼ばれる））
st.write(f"計算結果は ${result}$ です")
if st.checkbox("ソースコード表示",key="code_disp3") :
    st.code("""
            # result に数値を格納します．
            result = 1.4142

            #st: st.writeを利用した文章表示（f文字列（f-strings、フォーマット文字列、フォーマット済み文字列リテラルとも呼ばれる））
            st.write(f"計算結果は ${result}$ です")
            """, language="python")
"""___"""

#st: st.header を利用した見出し表示（後述）
st.header("2. Magic command を利用した文章の表示",divider='rainbow')

"""
`st.write()`を使用せず，トリプルクォーテーションで囲むだけでも，文章を表示させることができます．これはMagic commandと呼ばれており
streamlit特有の記法です．その一例を以下に示します．

__参考資料__  
- Magic commandの詳細はこちらをご覧下さい．  
    [ API reference:Magic command ](https://docs.streamlit.io/develop/api-reference/write-magic/magic)
- st.writeやMagic commandの他にもテキスト表示に使用できる機能があります．それらの詳細はこちらをご覧下さい．  
    [ API reference:Text elements](https://docs.streamlit.io/develop/api-reference/text)
___
"""

#st: Magic commandを利用した文章表示
"""
このWebアプリの文章の大半は，このMagic commandを利用して表示しています．
数式を含む長文が利用できるため，教材作成において非常に有効な手段だと思います．なお，数式はLatex記法で書きます．
$$
    L =\\sqrt{x^2+y^2}
$$
"""
if st.checkbox("ソースコード表示",key="code_disp4") :
    st.code("""
            #st: Magic commandを利用した文章表示
            \"\"\"
            このWebアプリの文章の大半は，このMagic commandを利用して表示しています．
            数式を含む長文が利用できるため，教材作成において非常に有効な手段だと思います．なお，数式はLatex記法で書きます．
            $$
                L =\\sqrt{x^2+y^2}
            $$
            \"\"\"
            """, language="python")

"""___"""
#計算結果を反映させた文章
import math
x=3
y=4
#st: Magic commandを利用した文章表示（f文字列）
f"""
f文字列と組み合わせることで，計算結果を反映させるような文章の作成も可能です．
$$
    L =\\sqrt{{x^2+y^2}}=\\sqrt{{{x}^2+{y}^2}}=\\sqrt{{{x**2+y**2}}}={math.sqrt(x**2+y**2)}
$$

注意：f文字列中に文字列として中カッコを入れる際は，二重の中カッコを使用します．
"""
if st.checkbox("ソースコード表示",key="code_disp5") :
    st.code("""
            #計算結果を反映させた文章
            import math
            x=3
            y=4
            #st: Magic commandを利用した文章表示（f文字列）
            f\"\"\"
            f文字列と組み合わせることで，計算結果を反映させるような文章の作成も可能です．
            $$
                L =\\sqrt{{  x^2+y^2  }}=\\sqrt{{  {x}^2+{y}^2  }}=\\sqrt{{  {x**2+y**2}  }} = {math.sqrt(x**2+y**2)}
            $$
            注意：f文字列中に文字列として中カッコを入れる際は，二重の中カッコを使用します．
            \"\"\"
            """, language="python")

"""___"""
