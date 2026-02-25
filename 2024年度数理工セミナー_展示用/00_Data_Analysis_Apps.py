import streamlit as st

# プログラムの実行場所の取得
from lib import FileProcessing as fp
location_str = fp.location()
st.session_state.location_str = location_str

st.sidebar.markdown(\
"**更新情報**\n \
- App 1.0:2024.12.20\n\
- App 1.1:2025.2.20\n \
- App 1.2:2025.6.6\n\
- App 1.3:2026.2.19\n\
")

# タイトル
# main_title = "データ分析支援アプリ:male-teacher:"
main_title = "データ分析支援アプリ"
st.title(f"{main_title}")

# st.page_link("00_Data_Analysis_Apps.py", label="Home", icon="🏠")
st.subheader("各分析ツールへ", divider="rainbow")
st.badge("**NEW**", color="orange")
st.page_link("pages/00_📱データの生成(New).py", label="データの生成へ", icon="📱")
st.page_link("pages/00_📱図の生成(New).py", label="図の生成へ", icon="📱")
""""""
st.page_link("pages/01_📊基本統計量の計算.py", label="基本統計量の計算へ", icon="📊")
st.page_link("pages/02_📊Histogram.py", label="ヒストグラムの作成へ", icon="📊")
st.page_link("pages/03_📊散布図_散布図行列.py", label="散布図または散布図行列の作成へ", icon="📊")
st.page_link("pages/04_📊相関係数行列.py", label="相関係数行列の計算へ", icon="📊")
st.page_link("pages/05_📊偏相関係数行列.py", label="偏相関係数行列の計算へ", icon="📊")
st.page_link("pages/06_📊線形回帰分析.py", label="線形回帰分析へ", icon="📊")
""" """
""" """
## URLと2次元コードの表示
st.subheader("Network URL 情報", divider="rainbow")
from lib import display
from io import BytesIO
network_url, qr_image = display.display_URL_QRCode(location_str)
# メモリ上に画像を保存
img_bytes = BytesIO()
qr_image.save(img_bytes, format="PNG")  # 画像フォーマットを指定
img_bytes.seek(0)  # ストリームを先頭に移動

left_col, right_col = st.columns([2,1])
with left_col:
    st.write("現在のアプリのNetwork URL:")
    st.code(network_url)
with right_col:
    st.image(img_bytes, caption="2次元コード", use_container_width=True)


# アプリの説明
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



st.subheader("2024年第2回高大連携定例研究会のWebアプリ", divider="rainbow")
st.page_link("https://kit-msec-app01-ds.streamlit.app", label="2024年第2回高大連携定例研究会のWebアプリへ",icon="↪️")