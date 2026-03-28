import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns

# ページ設定
st.set_page_config(page_title="確率分布の画像生成", layout="wide")

"""# 確率分布の画像生成"""

"""
このページでは、確率分布のグラフを生成し、指定された範囲の積分（塗りつぶし）と確率分布表を表示します。
"""

# 分布の種類
distributions = {
    "正規分布": "normal",
    "カイ2乗分布": "chi2", 
    "t分布": "t"
}

selected_dist = st.selectbox(
    "確率分布を選択してください",
    list(distributions.keys()),
    key="dist_select"
)

# 共通パラメータ
col_params = st.columns(2)
with col_params[0]:
    x_min = float(st.number_input("x軸の最小値", value=-4.0, key="x_min"))
    x_max = float(st.number_input("x軸の最大値", value=4.0, key="x_max"))
    num_points = int(st.number_input("プロット点数", value=1000, min_value=100, max_value=5000, key="num_points"))

with col_params[1]:
    lower_bound = float(st.number_input("積分下限", value=-1.0, key="lower_bound"))
    upper_bound = float(st.number_input("積分上限", value=1.0, key="upper_bound"))

# 分布ごとのパラメータ
if selected_dist == "正規分布":
    col_normal = st.columns(2)
    with col_normal[0]:
        mu = float(st.number_input("平均 μ", value=0.0, key="mu_normal"))
    with col_normal[1]:
        sigma = float(st.number_input("標準偏差 σ", value=1.0, min_value=0.1, key="sigma_normal"))
    
    # 正規分布の計算
    x = np.linspace(x_min, x_max, num_points)
    y = stats.norm.pdf(x, mu, sigma)
    
    # 積分範囲の計算
    if lower_bound < upper_bound:
        area = stats.norm.cdf(upper_bound, mu, sigma) - stats.norm.cdf(lower_bound, mu, sigma)
    else:
        area = 0.0
    
    # グラフ作成
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'b-', linewidth=2, label=f'正規分布 (μ={mu}, σ={sigma})')
    
    # 積分範囲の塗りつぶし
    if lower_bound < upper_bound:
        mask = (x >= lower_bound) & (x <= upper_bound)
        ax.fill_between(x[mask], y[mask], alpha=0.3, color='red', 
                       label=f'積分範囲: P({lower_bound} ≤ X ≤ {upper_bound}) = {area:.4f}')
    
    ax.set_xlabel('x')
    ax.set_ylabel('確率密度')
    ax.set_title('正規分布')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 確率分布表
    st.subheader("正規分布の確率分布表")
    table_data = {
        "確率": ["P(X ≤ -2σ)", "P(X ≤ -1σ)", "P(X ≤ 0)", "P(X ≤ 1σ)", "P(X ≤ 2σ)", "P(X ≤ 3σ)"],
        "値": [0.0228, 0.1587, 0.5000, 0.8413, 0.9772, 0.9987]
    }
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True)

elif selected_dist == "カイ2乗分布":
    col_chi2 = st.columns(1)
    with col_chi2[0]:
        df_chi2 = float(st.number_input("自由度 k", value=5.0, min_value=1.0, key="df_chi2"))
    
    # カイ2乗分布の計算
    x = np.linspace(0, x_max, num_points)
    y = stats.chi2.pdf(x, df_chi2)
    
    # 積分範囲の計算
    if lower_bound < upper_bound and lower_bound >= 0:
        area = stats.chi2.cdf(upper_bound, df_chi2) - stats.chi2.cdf(lower_bound, df_chi2)
    else:
        area = 0.0
    
    # グラフ作成
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'g-', linewidth=2, label=f'カイ2乗分布 (k={df_chi2})')
    
    # 積分範囲の塗りつぶし
    if lower_bound < upper_bound and lower_bound >= 0:
        mask = (x >= lower_bound) & (x <= upper_bound)
        ax.fill_between(x[mask], y[mask], alpha=0.3, color='red',
                       label=f'積分範囲: P({lower_bound} ≤ X ≤ {upper_bound}) = {area:.4f}')
    
    ax.set_xlabel('x')
    ax.set_ylabel('確率密度')
    ax.set_title('カイ2乗分布')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 確率分布表
    st.subheader("カイ2乗分布の確率分布表")
    critical_values = [0.1, 0.05, 0.025, 0.01, 0.005]
    table_data = {
        "有意水準 α": critical_values,
        "上側確率": [f"P(X > χ²_{alpha:.3f}) = {alpha}" for alpha in critical_values]
    }
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True)

elif selected_dist == "t分布":
    col_t = st.columns(1)
    with col_t[0]:
        df_t = float(st.number_input("自由度 ν", value=10.0, min_value=1.0, key="df_t"))
    
    # t分布の計算
    x = np.linspace(x_min, x_max, num_points)
    y = stats.t.pdf(x, df_t)
    
    # 積分範囲の計算
    if lower_bound < upper_bound:
        area = stats.t.cdf(upper_bound, df_t) - stats.t.cdf(lower_bound, df_t)
    else:
        area = 0.0
    
    # グラフ作成
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'r-', linewidth=2, label=f't分布 (ν={df_t})')
    
    # 標準正規分布との比較
    y_normal = stats.norm.pdf(x, 0, 1)
    ax.plot(x, y_normal, 'b--', linewidth=1, alpha=0.7, label='標準正規分布')
    
    # 積分範囲の塗りつぶし
    if lower_bound < upper_bound:
        mask = (x >= lower_bound) & (x <= upper_bound)
        ax.fill_between(x[mask], y[mask], alpha=0.3, color='red',
                       label=f'積分範囲: P({lower_bound} ≤ X ≤ {upper_bound}) = {area:.4f}')
    
    ax.set_xlabel('x')
    ax.set_ylabel('確率密度')
    ax.set_title('t分布')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 確率分布表
    st.subheader("t分布の確率分布表")
    critical_values = [0.1, 0.05, 0.025, 0.01, 0.005]
    table_data = {
        "有意水準 α": critical_values,
        "上側確率": [f"P(X > t_{alpha:.3f}) = {alpha}" for alpha in critical_values]
    }
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True)

# グラフの表示
st.pyplot(fig)

# 積分結果の表示
if lower_bound < upper_bound:
    st.success(f"積分結果: P({lower_bound} ≤ X ≤ {upper_bound}) = {area:.6f}")
else:
    st.warning("積分範囲が正しく設定されていません。下限 < 上限 となるように設定してください。")

# 統計情報の表示
st.subheader("統計情報")
col_stats = st.columns(3)

with col_stats[0]:
    if selected_dist == "正規分布":
        st.metric("平均", f"{mu:.2f}")
        st.metric("分散", f"{sigma**2:.2f}")
    elif selected_dist == "カイ2乗分布":
        st.metric("平均", f"{df_chi2:.2f}")
        st.metric("分散", f"{2*df_chi2:.2f}")
    elif selected_dist == "t分布":
        st.metric("平均", "0.00")
        st.metric("分散", f"{df_t/(df_t-2):.2f}" if df_t > 2 else "∞")

with col_stats[1]:
    if selected_dist == "正規分布":
        st.metric("歪度", "0.00")
        st.metric("尖度", "3.00")
    elif selected_dist == "カイ2乗分布":
        st.metric("歪度", f"{np.sqrt(8/df_chi2):.2f}")
        st.metric("尖度", f"{12/df_chi2 + 3:.2f}")
    elif selected_dist == "t分布":
        st.metric("歪度", "0.00")
        st.metric("尖度", f"{6/(df_t-4) + 3:.2f}" if df_t > 4 else "∞")

with col_stats[2]:
    if selected_dist == "正規分布":
        st.metric("モード", f"{mu:.2f}")
        st.metric("中央値", f"{mu:.2f}")
    elif selected_dist == "カイ2乗分布":
        mode = max(0, df_chi2 - 2)
        st.metric("モード", f"{mode:.2f}")
        st.metric("中央値", f"{df_chi2:.2f}")
    elif selected_dist == "t分布":
        st.metric("モード", "0.00")
        st.metric("中央値", "0.00")

# ダウンロード機能
st.subheader("データのダウンロード")
csv_data = pd.DataFrame({
    'x': x,
    '確率密度': y
})
csv_string = csv_data.to_csv(index=False).encode('shift_jis')
st.download_button(
    label="確率密度データをCSVでダウンロード",
    data=csv_string,
    file_name=f"{selected_dist}_probability_density.csv",
    mime="text/csv"
) 