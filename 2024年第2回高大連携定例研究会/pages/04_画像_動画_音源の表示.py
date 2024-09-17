import streamlit as st

#st: st.title を利用したテキスト表示
st.title("メディアデータの表示方法")
#st: Magic commandを利用したテキスト表示（Markdownのリンクや箇条書きの書き方を使用）
"""
ここでは，画像データや動画，音源の表示方法を紹介します．

__参考資料__
- `st.audio`に関する詳細はこちらをご覧ください．  
    [API reference:audio](https://docs.streamlit.io/develop/api-reference/media/st.audio)
- `st.image`に関する詳細はこちらをご覧ください．  
    [API reference:image](https://docs.streamlit.io/develop/api-reference/media/st.image)
- `st.video`に関する詳細はこちらをご覧ください．  
    [API reference:data_editor](https://docs.streamlit.io/develop/api-reference/media/st.video)

"""

#### 画像の表示
#st: st.header を利用した見出し表示
st.header("1. st.image を利用した画像の表示方法",divider='rainbow')


#st: Magic commandを利用したテキスト表示
"""
`st.image` を利用し，写真や画像を表示させることができます．`st.columns`と組み合わせることで，様々なレイアウトが可能です．
"""

#ファイルパスの設定
# `try`以下はローカルネットワーク上でアプリを実行するする場合．`except`以下はStreamlitのCommunity Cloudを利用する場合．
try :
    image_path1 = "media/sample_im01.jpeg"
    image_path2 = "media/sample_im02.jpeg"
    image_path3 = "media/sample_im03.jpeg"
except :
    image_path1 = "2024年第2回高大連携定例研究会/media/sample_im01.jpeg"
    image_path2 = "2024年第2回高大連携定例研究会/media/sample_im02.jpeg"
    image_path3 = "2024年第2回高大連携定例研究会/media/sample_im03.jpeg"
    
#st: st.columnsによる画面の3分割
# 2:1:1での分割は st.columns([2,1,1]) とする．
disp_col1 = st.columns([1,1,1])
# 画面左側 に表示させる内容
with disp_col1[0]:
    #st: st.imageによる画像の表示
    st.image(image_path1,caption="夏の海")
    """説明： 旅行先の風景 """

# 画面中央 に表示させる内容
with disp_col1[1]:
    #st: st.imageによる画像の表示
    st.image(image_path2,caption="桜")
    """説明： 春の大乗寺丘陵公園 """
# 画面左側 に表示させる内容
with disp_col1[2]:
    #st: st.imageによる画像の表示
    st.image(image_path3,caption="夕日")
    """説明： 撮影場所（[クリック](https://maps.app.goo.gl/ABHsEaFuo6kxquU58)） """

if st.checkbox("ソースコード表示",key="data_show_code_disp1") :
    """"""
    st.code("""
            #ファイルパスの設定
            # try以下はローカルネットワーク上でアプリを実行するする場合．except以下はStreamlitのCommunity Cloudを利用する場合．
            try :
                image_path1 = "media/sample_im01.jpeg"
                image_path2 = "media/sample_im02.jpeg"
                image_path3 = "media/sample_im03.jpeg"
            except :
                image_path1 = "2024年第2回高大連携定例研究会/media/sample_im01.jpeg"
                image_path2 = "2024年第2回高大連携定例研究会/media/sample_im02.jpeg"
                image_path3 = "2024年第2回高大連携定例研究会/media/sample_im03.jpeg"
                
            #st: st.columnsによる画面の3分割
            # 2:1:1での分割は st.columns([2,1,1]) とする．
            disp_col1 = st.columns([1,1,1])
            # 画面左側 に表示させる内容
            with disp_col1[0]:
                #st: st.imageによる画像の表示
                st.image(image_path1,caption="夏の海")
                \"\"\"説明： 旅行先の風景 \"\"\"
            # 画面中央 に表示させる内容
            with disp_col1[1]:
                #st: st.imageによる画像の表示
                st.image(image_path2,caption="桜")
                \"\"\"説明： 春の大乗寺丘陵公園 \"\"\"
            # 画面左側 に表示させる内容
            with disp_col1[2]:
                #st: st.imageによる画像の表示
                st.image(image_path3,caption="夕日")
                \"\"\"説明： 撮影場所（[クリック](https://maps.app.goo.gl/ABHsEaFuo6kxquU58)） \"\"\"
            """
            , language="python")
    


#### 動画の表示
#st: st.header を利用した見出し表示
st.header("2. st.video を利用した動画の表示方法",divider='rainbow')

#st: Magic commandを利用したテキスト表示
"""
`st.video` を利用し，動画ファイルを利用することができます．`st.columns`と組み合わせることで，様々なレイアウトが可能です．
"""

#ファイルパスの設定
# `try`以下はローカルネットワーク上でアプリを実行するする場合．`except`以下はStreamlitのCommunity Cloudを利用する場合．
try :
    video_path1 = "media/sample_mov02.mov"
except :
    video_path1 = "2024年第2回高大連携定例研究会/media/sample_mov02.mov"


#st: st.videoによる画像の表示
st.video(data=video_path1,loop=True)

if st.checkbox("ソースコード表示",key="data_show_code_disp2") :
    """"""
    st.code("""
            #ファイルパスの設定
            # `try`以下はローカルネットワーク上でアプリを実行するする場合．`except`以下はStreamlitのCommunity Cloudを利用する場合．
            try :
                video_path1 = "media/sample_mov02.mov"
            except :
                video_path1 = "2024年第2回高大連携定例研究会/media/sample_mov02.mov"


            #st: st.videoによる画像の表示
            st.video(data=video_path1,loop=True)
            """
            , language="python")
    



#### 音声の表示
#st: st.header を利用した見出し表示
st.header("2. st.audio を利用した動画の表示方法",divider='rainbow')

#st: Magic commandを利用したテキスト表示
"""
`st.audio` を利用し，音源データや音声ファイルを利用することができます．


"""

#ファイルパスの設定
# `try`以下はローカルネットワーク上でアプリを実行するする場合．`except`以下はStreamlitのCommunity Cloudを利用する場合．
try :
    audio_path1 = "media/sample_audio01.aac"
except :
    audio_path1 = "2024年第2回高大連携定例研究会/media/sample_audio01.aac"


"""
##### 秋の夜
注意：音が小さいと思われます．必要に応じてボリュームの変更をお願い致します．
"""
#st: st.videoによる画像の表示
st.audio(data=audio_path1,start_time=10,end_time=25,loop=True)


if st.checkbox("ソースコード表示",key="data_show_code_disp3") :
    """"""
    st.code("""
            #ファイルパスの設定
            # `try`以下はローカルネットワーク上でアプリを実行するする場合．`except`以下はStreamlitのCommunity Cloudを利用する場合．
            try :
                audio_path1 = "media/sample_audio01.aac"
            except :
                audio_path1 = "2024年第2回高大連携定例研究会/media/sample_audio01.aac"
            #st: st.videoによる画像の表示
            # start timeとend timeというオプションを使用．またループ再生をオンにしている．
            st.audio(data=audio_path1,start_time=10,end_time=25,loop=True)
            """
            , language="python")
    

