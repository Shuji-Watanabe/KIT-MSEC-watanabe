import streamlit as st

# タイトル
main_title = ":male-teacher:データ分析支援アプリ"
st.title(f"{main_title}")


## URLとQRコードの表示
st.subheader("Network URL 情報", divider="rainbow")

from lib import display
from io import BytesIO
network_url, qr_image = display.display_URL_QRCode()
# メモリ上に画像を保存
img_bytes = BytesIO()
qr_image.save(img_bytes, format="PNG")  # 画像フォーマットを指定
img_bytes.seek(0)  # ストリームを先頭に移動


left_col, right_col = st.columns([2,1])
with left_col:
    st.write("現在のアプリのNetwork URL:")
    st.code(network_url)
with right_col:
    st.image(img_bytes, caption="QR Code", use_container_width=True)
#
st.subheader("このアプリについて",divider="rainbow")

"""
このWebアプリは，金沢工業大学　2024年度数理工セミナー（展示ブース）で使用したWebアプリです．
このWebアプリのデータはGitHubにて公開しています．
"""

left_col, right_col = st.columns([1,2])
with left_col:
    st.subheader("公開場所",divider="green")
    st.markdown("[公開場所](https://github.com/Shuji-Watanabe/KIT-MSEC-watanabe)")
with right_col:
    st.subheader("ソースコードのダウンロード方法",divider="green")

    # プログラムの実行場所の取得
    from lib import FileProcessing as fp
    location_str = fp.location()
    st.session_state.location_str = location_str


    # location_str == 'github'はStreamlitのCommunity Cloudを利用する場合のファイルパス
    if location_str == "streamlit_Community_Cloud" :
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