def display_URL_QRCode():
    import os
    import socket

    path = os.getcwd()
    data_path = path+"/基本データ"


    # ホストIPアドレスを取得
    def get_host_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # GoogleのDNSサーバーに接続（IPアドレスは実際には送信されない）
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"  # デフォルト（ローカル）
        finally:
            s.close()
        return ip

    # ポート番号を取得
    port = os.environ.get("STREAMLIT_SERVER_PORT", "8501")
    host_ip = get_host_ip()
    network_url = f"http://{host_ip}:{port}"

    # Network URL を表示
    from qrcode import QRCode
    qr = QRCode()
    qr.add_data(network_url)
    qr.make()  # QRコードを生成
    qr_image = qr.make_image()  # QRコードの画像を生成
    return network_url, qr_image


def explanation_corr(val):
    if  0 <= val :
        tmp_str = "正"
    else :
        tmp_str = "負"
        
    if 0.7 <= abs(val) <= 1.0:
        exp_str = f"強い{tmp_str}の相関がある"
    elif 0.4 <= abs(val) < 0.7:
        exp_str = f"中程度の{tmp_str}の相関がある"
    elif 0.2 <= abs(val) < 0.4:
        exp_str = f"弱いの{tmp_str}の相関がある"
    elif 0.0 <= abs(val) < 0.2:
        exp_str = f"ほぼ相関はない"
    return exp_str

def make_lr_expr(names_list,response_value,coef_list):
    ## １．数式の生成
    # LaTeX文字列を作成する
    terms = []
    for i, item in enumerate(names_list):
        # 小数第3位までの絶対値
        formatted_coeff = f"{abs(coef_list[i]):.3f}"
        # 1つ目の項目は符号なし（負の場合は先頭に '-' を付ける）
        if i == 0:
            sign = "-" if coef_list[i] < 0 else ""
        else:
            # 2つ目以降は正の場合は " + ", 負の場合は " - "
            sign = " - " if coef_list[i]  < 0 else " + "
        # 各項目の項を生成 (例: "1.23\,(item1)")
        if i == 0:
            term = f"{sign}{formatted_coeff}"
        else:
            term = f"{sign}{formatted_coeff}\\big(\\text{{{str(item)}の値}}\\big)"
        terms.append(term)
    # 連結して最終的な文字列を作成
    exp_latex = f"\\big(\\text{{{response_value}の値}}\\big)"" = " + "".join(terms)
    return exp_latex