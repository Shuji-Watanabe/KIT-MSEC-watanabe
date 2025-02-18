def streamlit_uploaded_csv(st_uploaded_files, selected_type="自動",DisplayLocation = "normal"):
    import streamlit as st
    import pandas as pd
    if selected_type == "自動":
            # 2025/02/17更新 (学生スタッフ：藤山)
            from chardet import detect
            binary_data = st_uploaded_files.read()
            encode_data = detect(binary_data)  # エンコーディングを検出
            st_uploaded_files.seek(0) # ポインタを初期位置に戻し再度読み取り可能にする
            try:
                encoding = encode_data['encoding'].lower()    
                encoding = encoding.replace("-","_")    
                read_data_df = pd.read_csv(st_uploaded_files, encoding=encode_data['encoding'])
            except:
                st.error("エンコードエラー．別の方法でエンコードを設定してください．")
                st.stop()
            if DisplayLocation == "normal":
                st.write(f"アップロードされたファイルのエンコード: {encoding}") # 確認用
            elif DisplayLocation == "sidebar":
                st.sidebar.write(f"アップロードされたファイルのエンコード: {encoding}") # 確認用

    elif selected_type == "選択" :
        encode_list = [  "utf_8"
                        , "shift_jis"
                        , "cp932"
                        , "euc_jp", "euc_jis_2004", "euc_jisx0213"
                        , "iso2022_jp", "iso2022_jp_1", "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext"
                        , "shift_jis_2004", "shift_jisx0213"
                        , "utf_32" , "utf_32_be", "utf_32_le"
                        , "utf_16", "utf_16_be", "utf_16_le"
                        , "utf_7" 
                        , "utf_8_sig"]
        if DisplayLocation == "normal":
            encoding = st.selectbox( "適切なエンコードを選択", options=encode_list)
        elif DisplayLocation == "sidebar":
            encoding = st.sidebar.selectbox( "適切なエンコードを選択", options=encode_list)
        try:
            read_data_df = pd.read_csv(st_uploaded_files, encoding=encoding)
        except:
            st.error("エンコードエラー．適切なエンコードを選択してください．")
            st.stop() 

    elif selected_type == "入力":
        if DisplayLocation == "normal":
            encoding = st.text_input("エンコードを半角英数字で入力",value="utf_8")
        elif DisplayLocation == "sidebar":
            encoding = st.sidebar.text_input("エンコードを半角英数字で入力",value="utf_8")
        try:
            read_data_df = pd.read_csv(st_uploaded_files, encoding=encoding)
        except:
            st.error("エンコードエラー．適切なエンコードを入力してください．")
            st.stop() 
    return read_data_df