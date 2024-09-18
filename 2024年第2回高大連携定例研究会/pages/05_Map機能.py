import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
from streamlit_folium import st_folium

#st: st.title を利用したテキスト表示
st.title('地図表示機能の利用方法')

"""
streamlitには`st.map`という地図機能がありますが，地図情報が他社の情報を利用している関係で，
個人でライセンスを取得することが推奨されている機能となっています．
利便性を考慮し，この機能についての説明は割愛しました．

ここでは，オープソースのmap情報を利用した，地図の表示方法を紹介します．
なお，この機能を利用するためには
『folium』および『streamlit_folium』というライブラリのインストールが必要となります．

__参考資料__
- `st.map`に関する詳細はこちらをご覧ください．  
    [API reference:map](https://docs.streamlit.io/develop/api-reference/media/st.audio)
- foliumに関する詳細はこちらをご覧ください．  
    [ちょこっとプロ！：foliumで地図作成！Pythonエンジニアなら知っておくべき使い方・利点・サンプルコード8選](https://chocottopro.com/?p=664)
- streamlit_foliumとfoliumに関する詳細はこちらをご覧ください．  
    [Zenn：Streamlitで世界の太陽光発電所情報を可視化](https://zenn.dev/ta_murata_18/articles/8d63b7aae9a4b9)
- foliumと同様の地図機能を用いた情報Ⅱにおける実践例がありましたので，情報共有致します．
    文部科学省，高等学校「情報」実践事例集，[情報II(5)「地図コンテンツを活用して平和問題への理解を深めよう」](https://www.mext.go.jp/content/20220324-mxt_kouhou02-000021508_2.pdf)
"""

#st: st.header を利用した見出し表示
st.header("1. folium を利用した地図の表示方法",divider='rainbow')

# 初期表示に関する設定
map = folium.Map(location=[36.530, 136.6287],zoom_start = 15) 

# mapにアイコン等を表示を追加
folium.Marker(
    # アイコンを表示する位置の緯度と経度を指定
    location=[36.530, 136.6287],
    # ポップアップの設定
    popup=folium.Popup("KIT", max_width=200),
    # アイコンの指定(アイコン、色)
    icon=folium.Icon(icon="flag",icon_color="white", color="red")
).add_to(map)

# mapに記された情報をstreanlit上に表示
st_folium(map)

if st.checkbox("ソースコード表示",key="show_code_disp1") :
    """"""
    st.code("""
            # 初期表示に関する設定
            map = folium.Map(location=[36.530, 136.6287],zoom_start = 15) 

            # mapにアイコン等を表示を追加
            folium.Marker(
                # アイコンを表示する位置の緯度と経度を指定
                location=[36.530, 136.6287],
                # ポップアップの設定
                popup=folium.Popup("KIT", max_width=200),
                # アイコンの指定(アイコン、色)
                icon=folium.Icon(icon="flag",icon_color="white", color="red")
            ).add_to(map)

            # mapに記された情報をstreanlit上に表示
            st_folium(map)
            """
            , language="python")
    


### 散歩データの表示
#st: st.header を利用した見出し表示
st.header("2. folium の応用",divider='rainbow')

"""
ここではスマートフォンで取得した散歩中の位置情報を，地図上に示す方法を紹介します．

__参考資料__
- スマートフォンによる位置情報の取得はphyphoxを利用しました．
    [phyphox](https://phyphox.org)
\n 
\n
"""

#地図上に表示する情報の取得（GPSデータの読み込み）
try :
    df = pd.read_csv('sample_datas/GPS_Data.csv')
except:
    df = pd.read_csv('2024年第2回高大連携定例研究会/sample_datas/GPS_Data.csv')
# dfのキー（列名）を取得
df_key_list = df.keys()


# 初期表示に関する設定
map = folium.Map(location=[36.53183045, 136.6286506],zoom_start = 18) 

# dfから１行ずつ位置情報を取得し，その情報を地図上のマーカーに記載
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

"""
#### 散歩中の位置情報と移動経路

"""

#　mapに格納された情報をstreamlit上に表示
folium_static(map)

if st.checkbox("ソースコード表示",key="show_code_disp2") :
    """"""
    st.code("""
            #地図上に表示する情報の取得（GPSデータの読み込み）
            try :
                df = pd.read_csv('sample_datas/GPS_Data.csv')
            except:
                df = pd.read_csv('2024年第2回高大連携定例研究会/sample_datas/GPS_Data.csv')
            # dfのキー（列名）を取得
            df_key_list = df.keys()


            # 初期表示に関する設定
            map = folium.Map(location=[36.53183045, 136.6286506],zoom_start = 18) 

            # dfから１行ずつ位置情報を取得し，その情報を地図上のマーカーに記載
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
            """
            , language="python")

