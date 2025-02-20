def data_load_form(sidebar_text, cd_path, data_path ,data_dict):
    import streamlit as st
    import pandas as pd
    import os
    from chardet import detect
    #=====使用データの設定=====================================================================
    st.sidebar.subheader(sidebar_text)
    st.sidebar.markdown(":arrow_forward: 分析に使用するデータの選択")
    tub_dict = {"擬似データ":0,"ユーザーデータ":1}
    selected_cbox = st.sidebar.radio(label="選択", options = tub_dict.keys(),horizontal=True)
    """ """
    ###  擬似データによる分析体験
    tub_counta = 0
    if tub_dict[selected_cbox] == 0 :
        tub_title = list(tub_dict.keys())[tub_counta]
        # with tub_list[0]:
        st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
        """   """
        st.subheader(f"Step１: 分析データの選択", divider="green")
        select_data_dict = data_dict
        # 分析データの選択      
        select_str = st.selectbox("分析するデータファイルを選択してください",select_data_dict.keys(),key="mselect 01")      
        filedir_path = os.path.join(cd_path,data_path) 
        csv_path = os.path.join(filedir_path,data_dict[select_str])
        
        # エンコーディング検出機能を使う
        with open(csv_path, "rb") as f:
            raw_data = f.read(10000)  # 最初の1万バイトを読み取る
            result = detect(raw_data)
        data_encoding = result["encoding"].lower()    
        data_encoding = data_encoding.replace("-","_") 
        read_data_df = pd.read_csv( str(csv_path) ,encoding=data_encoding)


    ###  ユーザーデータによる分析体験
    elif tub_dict[selected_cbox] == 1 :
        tub_counta += 1
        tub_title = list(tub_dict.keys())[tub_counta]
        # with tub_list[1]:
        st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
        """   """
        st.subheader(f"Step１: 分析データのアップロード", divider="green")
        tmp_dict = { "前回アップロードしたデータを使用し続ける":True
                    ,"新しいファイルをアップロードする":False}
        
        with st.form(key="reset"):
            if 'filename' in st.session_state:
                st.write(f"現在分析に使用しているファイル：{st.session_state.filename}")
                tmp_button = st.form_submit_button("データファイルをリセット")
                radio_index = 0
                # 特定の変数だけをクリア
                if tmp_button:
                    del st.session_state["filename"]
                    del st.session_state["userdata"]
                    radio_index = 1
            else:
                radio_index = 1

        select_radio = st.sidebar.radio("使用するユーザーデータについて"
                                        ,options=tmp_dict.keys()
                                        ,index = radio_index)
        if 'filename' in st.session_state:
            st.sidebar.write(f"データファイル{st.session_state.filename}")
        if  "userdata" in st.session_state and tmp_dict[select_radio]:
            read_data_df = st.session_state.userdata
        else :
            disp_col0 = st.columns([1,3])
            with disp_col0[1]:
                st.warning("データをアップロードする前に，アップロードするデータに個人情報等，取扱に注意しなければならないデータが含まれていないか確認してください．")
            with disp_col0[0]:
                tmp_check = st.checkbox("確認しました")

            if tmp_check:
                st.divider()
                uploaded_file = st.sidebar.file_uploader(":arrow_forward: CSVファイルのアップロード"
                                                         ,type="csv")    
                if not uploaded_file:
                    st.sidebar.error('データがアップロードされていません', icon="⚠️")
                    st.stop()
            else :
                st.sidebar.write("停止中")
                st.stop()

            st.sidebar.divider()
            set_encode_list = ["自動","選択","入力"]
            selected_way = st.sidebar.radio(":arrow_forward: エンコードの指定方法",options=set_encode_list,horizontal=True)
            import lib.FileProcessing as FileProcessing 
            read_data_df= FileProcessing.streamlit_uploaded_csv(st_uploaded_files=uploaded_file
                                                                ,selected_type=selected_way
                                                                ,DisplayLocation="sidebar")
            st.session_state.userdata = read_data_df
            st.session_state.filename = uploaded_file.name
    return read_data_df