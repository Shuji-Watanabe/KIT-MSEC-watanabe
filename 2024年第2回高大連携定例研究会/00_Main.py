import streamlit as st

# タイトル
main_title = "データ分析体験アプリ＆探究で使えそうな機能"
st.markdown(f"### {main_title}")

#
st.subheader("はじめに",divider="rainbow")

"""
このWebアプリは，金沢工業大学　数理工教育研究センター高大連携研究会　2024年度第2回定例研究会の発表で使用したWebアプリです．
このWebアプリのデータはGitHubにて公開しています．

__公開場所とダウンロード方法，利用について__


"""
st.subheader("公開場所",divider="rainbow")
st.markdown("[公開場所](https://github.com/Shuji-Watanabe/KIT-MSEC-watanabe)")
st.subheader("ダウンロード方法",divider="rainbow")

import os 
path = os.getcwd()
if path == '/mount/src/kit-msec-watanabe':
    location_str = "github"
else:
    location_str = "local"


# location_str == 'github'はStreamlitのCommunity Cloudを利用する場合のファイルパス
if location_str == 'github' :
    tmp_path = "2024年第2回高大連携定例研究会/media/expl_download"
else :
    tmp_path = "media/expl_download"

col = st.columns([1,1,1])
with col[0]:
    image_path = tmp_path + "/expl_download.001.jpeg"
    st.image(image_path,caption="操作１")
with col[1]:
    image_path = tmp_path + "/expl_download.002.jpeg"
    st.image(image_path,caption="操作２")
with col[2]:
    image_path = tmp_path + "/expl_download.003.jpeg"
    st.image(image_path,caption="操作３")