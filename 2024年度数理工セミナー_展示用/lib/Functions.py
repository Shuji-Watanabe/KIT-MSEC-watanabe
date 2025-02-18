def compute_statistics(pd_dataframe):
    """
    指定した pandas DataFrame の統計量を計算して返す関数です。
    
    引数:
        pd_dataframe (pandas.Series または pandas.DataFrameの数値列):
            統計量を計算したい対象のデータ。各統計量は数値データとして扱います。
    
    戻り値:
        dict:
            以下の統計量をキーとした辞書を返します。
            - "データ数": データの個数（非欠損値の数）
            - "最大値": データの中での最大値
            - "最小値": データの中での最小値
            - "合計": データの総和
            - "平均": データの算術平均
            - "分散": データの分散
            - "標準偏差": データの標準偏差
            - "中央値": データの中央値
            - "四分位数": 第1四分位数(25%)、第2四分位数(50%、=中央値)、第3四分位数(75%) をまとめた DataFrame（転置済み）
    """
    return {
        "データ数": int(pd_dataframe.count()),
        "最大値": float(pd_dataframe.max()),
        "最小値": float(pd_dataframe.min()),
        "合計": float(pd_dataframe.sum()),
        "平均": float(pd_dataframe.mean()),
        "分散": float(pd_dataframe.var()),
        "標準偏差": float(pd_dataframe.std()),
        "中央値": float(pd_dataframe.median()),
        "四分位数": list(pd_dataframe.quantile([0.25, 0.5, 0.75]).transpose())
    }