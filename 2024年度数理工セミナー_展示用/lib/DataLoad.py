def data_load_form(sidebar_text, cd_path, data_path , data_encoding, data_dict):
    import streamlit as st
    import pandas as pd
    import os
    #=====使用データの設定=====================================================================
    st.sidebar.subheader(sidebar_text)
    st.sidebar.markdown(":arrow_forward: 分析に使用するデータの選択")
    tub_dict = {"分析体験デモデータ":0,"ユーザーデータ":1}
    selected_cbox = st.sidebar.radio(label="選択", options = tub_dict.keys(),horizontal=True)
    """ """
    ###  デモデータによる分析体験
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
        read_data_df = pd.read_csv( str(csv_path),encoding=data_encoding)


    ###  ユーザーデータによる分析体験
    elif tub_dict[selected_cbox] == 1 :
        tub_counta += 1
        tub_title = list(tub_dict.keys())[tub_counta]
        # with tub_list[1]:
        st.header(f""":bar_chart: {tub_title }を用いた分析""",divider="rainbow")
        """   """
        st.subheader(f"Step１: 分析データのアップロード", divider="green")
        
        disp_col0 = st.columns([1,3])
        with disp_col0[1]:
            st.warning("データをアップロードする前に，アップロードするデータに個人情報等，取扱に注意しなければならないデータが含まれていないか確認してください．")
        with disp_col0[0]:
            tmp_check = st.checkbox("確認しました")
        st.sidebar.divider()

        if tmp_check:
            st.divider()
            uploaded_files = st.sidebar.file_uploader(":arrow_forward: CSVファイルのアップロード")    
            if not uploaded_files:
                st.sidebar.error('データがアップロードされていません', icon="⚠️")
                st.stop()
        else :
            st.sidebar.write("停止中")
            st.stop()
        
        st.sidebar.divider()
        set_encode_list = ["自動","選択","入力"]
        selected_way = st.sidebar.radio(":arrow_forward: エンコードの指定方法",options=set_encode_list,horizontal=True)
        import lib.FileProcessing as FileProcessing 
        read_data_df= FileProcessing.streamlit_uploaded_csv(st_uploaded_files=uploaded_files
                                                            ,selected_type=selected_way
                                                            ,DisplayLocation="sidebar")

    return read_data_df