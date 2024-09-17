import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

# タイトル
st.title('ある日の散歩道')


#地図の初期設定
map = folium.Map(location=[36.53183045, 136.6286506],zoom_start = 18) 


#地図上に表示する情報の取得
try :
    df = pd.read_csv('sample_datas/Raw_Data.csv')
except:
    df = pd.read_csv('2024年第2回高大連携定例研究会/sample_datas/Raw_Data.csv')

df_key_list = df.keys()

# dfから１行ずつデータを取得し，その情報を地図上のマーカーに記載
for i, row in df.iterrows():
     # 地図へのマーカーの追加
    if i == 0 :
        # ポップアップに関する変数の作成
        pop=f"Start <br>　時間…{row[df_key_list[0]]:,} s <br>　速さ…{row[df_key_list[3]]:,}m/s"
        folium.Marker(
            # 緯度と経度を指定
            location=[row[df_key_list[1]], row[df_key_list[2]]],
            # ポップアップの指定
            popup=folium.Popup(pop, max_width=200),
            # アイコンの指定(アイコン、色)
            icon=folium.Icon(icon="flag",icon_color="white", color="red")
        ).add_to(map)
    elif i==len(df)-1:
        pop=f"End <br>　時間…{row[df_key_list[0]]:,} s <br>　速さ…{row[df_key_list[3]]:,}m/s"
        folium.Marker(
            # 緯度と経度を指定
            location=[row[df_key_list[1]], row[df_key_list[2]]],
            # ポップアップの指定
            popup=folium.Popup(pop, max_width=200),
            # アイコンの指定(アイコン、色)
            icon=folium.Icon(icon="flag",icon_color="white", color="blue")
        ).add_to(map)
    else :
        pop=f"<br>　時間…{row[df_key_list[0]]:,} s <br>　速さ…{row[df_key_list[3]]:,}m/s"
        folium.Marker(
            # 緯度と経度を指定
            location=[row[df_key_list[1]], row[df_key_list[2]]],
            # ポップアップの指定
            popup=folium.Popup(pop, max_width=200),
            # アイコンの指定(アイコン、色)
            icon=folium.Icon(icon="flag",icon_color="white", color="gray")
        ).add_to(map)

linedata_list = df[[df_key_list[1],df_key_list[2]]].values.tolist()
line1 = folium.PolyLine(linedata_list , weight=5, color="#0000ff").add_to(map)

folium_static(map)