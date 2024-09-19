# ライブラリの読み込み
import streamlit as st

"""
# streamlitの始め方
"""
"""
ここではstreamlitを始めるために必要な手順とその方法について，紹介します．
以下の説明は，プログラムのエディターやpythonを開発・実行する環境がすでに
整っていることを前提としております．

今回の説明はvscodeを使用した場合の説明です．

"""


"""  """
"""  """

st.header("1. streamlitをインストールする",divider="rainbow")
"""
#### インストールコマンド  
vscodeのターミナル上で次のコマンドを実行
"""
st.code("""
pip install stramlit
""")

"""  """

st.header("2. streamlitアプリを作成する",divider="rainbow")
"""
#### アプリ作成の流れ  
"""
st.write("""#### 1. vscodeにてpythonのソースファイルを作成する  
[Python Japan:Visual Studio Code でPython入門 【Windows編】 〉 VSCodeでPythonを実行](https://www.python.jp/python_vscode/windows/run/write_source.html)
""")
st.write("""#### 2. 作成したソースファイルに書く内容  
次のように，ライブラリ `streamlit` をインポートする．一般的に`streamlit`は`st`で呼び出します．
""")
st.code("""import streamlit as st""")

st.write("""#### 3. ソースコードの保存  
Webアプリ作成のためのコードが書き終えたら，保存をお願いします．
""")
st.code("""
    # 例
    # test.pyというファイルに次を書き，保存してください．
    import streamlit as st

    st.write("Hello World！")
        """)

st.write("""#### 4. ファイルの実行  
vscodeのターミナルで，streamlitのソースファイルがある場所に移動し，次のように実行します．  

    streamlit run test.py  

自動的にWebブラウザが起動し，Webアプリが立ち上がります．
このとき，ターミナルに  

    You can now view your Streamlit app in your browser.  

    Local URL:  _XXXXXXX_  
    Network URL: _YYYYYYY_  

と表示されるはずです． _XXXXXXX_ や _YYYYYYY_ を利用することで，
同一ネットワーク上にあるPCから，このアプリが利用できます．
         """)
"""
__参考資料__
- vscodeのインストール方法(Windows)  
    [みやしもブログ：VSCodeのインストール方法・日本語化の手順を解説する](https://miyashimo-studio.jp/blog/detail/vscode-install/)
- vscodeのインストール＋pythonのインストール方法(Windows)  
    [Visual Studio CodeをインストールしてPython開発環境を準備する(Windows編)](https://sukkiri.jp/technologies/processors/python/visual-studioをインストールしてpython開発環境を準備するwindows編.html)
- pythonのバージョンについて  
    pythonはそのバージョンごとにインストールできるライブラリが異なるのでご注意ください．
    本発表のアプリ開発には, _python 3.12.0_ を使用しています．
- pipのバージョンについて  
    pythonのライブラリをインストールする際，パッケージ管理システムpipを利用します．
    本発表のアプリ開発には, _pip 24.2_ を使用しています．pipの利用については，
    次のリンク先の『3.3. packageのインストール』をご覧ください．  
    [Qiita:[python] pip/VSCode開発環境の構築 (windows11)](https://qiita.com/flcn-x/items/ac6e222004a827f582ea)
- streamlitのバージョンについて  
    streamlitは現在も活発な開発が行われており，バージョンごとに使えるオプションが異なります．
    streamlitのAPI referenceで紹介されている機能は，概ね最新版のものです．
    本発表のアプリ開発には, _streamlit 1.38.0_ を使用しています．
- streamlitの基本的な使い方について  
    streamlitのAPI referenceで詳しい説明がなされています．導入については，
    _Get started_に記載してあります．
    [streamlit API reference](https://docs.streamlit.io)
- streamlit Community Cloud を利用した一般公開について  
    streamlit Community Cloudを利用することで作成したアプリを一般公開することが可能です．
    そのための手順は次の通りです．
    1. GitHubのアカウント作成
    1. GitHubにリポジトリを作成
    1. GitHubのリポジトリにWebアプリのソースファイル等をアップロード
    1. streamlit Community Cloudのアカウント作成
    1. streamlit Community CloudでWebアプリをデプロイ
"""


st.info("""今後，情報を追加する予定""")
