import streamlit as st

# タイトル
main_title = ":male-teacher:データ分析支援アプリ"
st.title(f"{main_title}")

#
st.subheader("はじめに",divider="rainbow")

"""
このWebアプリは，金沢工業大学　2024年度数理工セミナー（展示ブース）で使用したWebアプリです．
このWebアプリのデータはGitHubにて公開しています．

__公開場所とダウンロード方法，利用について__


"""
st.subheader("公開場所",divider="rainbow")
st.markdown("[公開場所](https://github.com/Shuji-Watanabe/KIT-MSEC-watanabe)")
st.subheader("ダウンロード方法",divider="rainbow")

import os 
cwd_path = os.getcwd()

if cwd_path == '/mount/src/kit-msec-watanabe':
    location_str = "github"
else:
    location_str = "local"


# location_str == 'github'はStreamlitのCommunity Cloudを利用する場合のファイルパス
if location_str == 'github' :
    tmp_path = "2024年度数理工セミナー_展示用/media/expl_download"
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

st.sidebar.markdown(\
"**更新情報**\n \
- Ver001:2025.2.17\n\
")