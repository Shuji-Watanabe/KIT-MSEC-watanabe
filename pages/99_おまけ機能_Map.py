import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

# タイトル
st.title('ある日の散歩道')


#地図の初期設定
map = folium.Map(location=[36.53183045, 136.6286506],zoom_start = 18) 


#地図上に表示する情報の取得
df = pd.read_csv('sample_datas/Raw_Data.csv')
df_key_list = df.keys()

# dfから１行ずつデータを取得し，その情報を地図上のマーカーに記載
for i, row in df.iterrows():
    # ポップアップに関する変数の作成
    pop=f"<br>　時間…{row[df_key_list[0]]:,} s <br>　速さ…{row[df_key_list[3]]:,}m/s"
     # 地図へのマーカーの追加
    folium.Marker(
        # 緯度と経度を指定
        location=[row[df_key_list[1]], row[df_key_list[2]]],
        # ポップアップの指定
        popup=folium.Popup(pop, max_width=200),
        # アイコンの指定(アイコン、色)
        icon=folium.Icon(icon="flag",icon_color="white", color="blue")
    ).add_to(map)
    
folium_static(map)