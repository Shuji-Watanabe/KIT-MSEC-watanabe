# pages/06_📱画像の生成.py   (SciPy 非依存＋UI 統一版)
import io, math
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- ページ設定 ----------
st.set_page_config(page_title="確率分布ジェネレータ", page_icon="📈")
st.header("確率分布の画像生成", divider="rainbow")

"""
生成したい分布と画像フォーマットを選択し、パラメータを入力して
「画像を表示」ボタンをクリックしてください。
"""

# ---------- 分布・フォーマット選択 ----------
dist_options = ["二項分布", "ポアソン分布",
                "一様分布", "正規分布",
                "t 分布", "カイ２乗分布"]
fmt_options  = ["PNG", "TIFF", "JPEG", "SVG"]

sel_cols = st.columns([2, 1])
with sel_cols[0]:
    dist_name = st.radio("分布の種類", options=dist_options, horizontal=True)
with sel_cols[1]:
    img_fmt = st.selectbox("画像フォーマット", options=fmt_options)

st.divider()

# ---------- 共通関数 ----------
def save_fig(fig, fmt):
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt.lower(), dpi=300, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()

def pmf_binom(k, n, p):
    return math.comb(n, k) * p**k * (1-p)**(n-k)

def pmf_poisson(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)

# ---------- パラメータ入力 ----------
col1, col2, col3 = st.columns(3)
sample_size = 1000   # 連続分布ヒストグラム用サンプル

if dist_name == "二項分布":
    with col1: n = st.number_input("試行回数 n", 1, 100, 10)
    with col2: p = st.slider("成功確率 p", 0.0, 1.0, 0.5, 0.01)

elif dist_name == "ポアソン分布":
    with col1: lam = st.number_input("λ (平均)", 0.1, 100.0, 3.0, 0.1)

elif dist_name == "一様分布":
    with col1: a = st.number_input("最小値 a", value=0.0)
    with col2: b = st.number_input("最大値 b", value=1.0)

elif dist_name == "正規分布":
    with col1: mu = st.number_input("平均 μ", value=0.0)
    with col2: sigma = st.number_input("標準偏差 σ (>0)", min_value=0.0001, value=1.0)

elif dist_name == "t 分布":
    with col1: df_t = st.number_input("自由度 ν", 1, 100, 10)

elif dist_name == "カイ２乗分布":
    with col1: df_c2 = st.number_input("自由度 k", 1, 100, 5)

st.divider()

# ---------- 描画ボタン ----------
if st.button("画像を表示"):
    if dist_name == "二項分布":
        x = np.arange(n + 1)
        y = [pmf_binom(i, n, p) for i in x]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=x, y=y, color="skyblue", ax=ax)
        ax.set_title(f"Binomial(n={n}, p={p})")
        ax.set_xlabel("k"); ax.set_ylabel("PMF")

    elif dist_name == "ポアソン分布":
        k_max = int(lam + 4*np.sqrt(lam))
        x = np.arange(k_max + 1)
        y = [pmf_poisson(i, lam) for i in x]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=x, y=y, color="salmon", ax=ax)
        ax.set_title(f"Poisson(λ={lam})")
        ax.set_xlabel("k"); ax.set_ylabel("PMF")

    elif dist_name == "一様分布":
        if b <= a:
            st.error("最大値は最小値より大きくしてください。")
            st.stop()
        x = np.linspace(a, b, 400)
        pdf = np.full_like(x, 1/(b-a))
        sample = np.random.uniform(a, b, sample_size)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(sample, bins=30, stat="density",
                     color="lightgray", edgecolor="black", ax=ax)
        ax.plot(x, pdf, lw=2, color="blue")
        ax.set_title(f"Uniform({a}, {b})")

    elif dist_name == "正規分布":
        x = np.linspace(mu-4*sigma, mu+4*sigma, 400)
        pdf = (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-(x-mu)**2/(2*sigma**2))
        sample = np.random.normal(mu, sigma, sample_size)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(sample, bins=30, stat="density",
                     color="lightgray", edgecolor="black", ax=ax)
        ax.plot(x, pdf, lw=2, color="darkgreen")
        ax.set_title(f"Normal(μ={mu}, σ={sigma})")

    elif dist_name == "t 分布":
        x = np.linspace(-5, 5, 400)
        g1 = math.gamma((df_t+1)/2); g2 = math.gamma(df_t/2)
        pdf = (g1/(np.sqrt(df_t*np.pi)*g2)) * (1 + x**2/df_t)**(-(df_t+1)/2)
        sample = np.random.standard_t(df_t, sample_size)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(sample, bins=30, stat="density",
                     color="lightgray", edgecolor="black", ax=ax)
        ax.plot(x, pdf, lw=2, color="purple")
        ax.set_title(f"t(df={df_t})")

    elif dist_name == "カイ２乗分布":
        x = np.linspace(0, df_c2*4, 400)
        g = math.gamma(df_c2/2)
        pdf = (1/(2**(df_c2/2)*g)) * x**(df_c2/2-1) * np.exp(-x/2)
        sample = np.random.chisquare(df_c2, sample_size)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(sample, bins=30, stat="density",
                     color="lightgray", edgecolor="black", ax=ax)
        ax.plot(x, pdf, lw=2, color="orange")
        ax.set_title(f"Chi-square(df={df_c2})")

    # ---------- 表示 & ダウンロード ----------
    st.pyplot(fig)

    img_bytes = save_fig(fig, img_fmt)
    st.download_button(
        label=f"{img_fmt} 形式でダウンロード",
        data=img_bytes,
        file_name=f"{dist_name}.{img_fmt.lower()}",
        mime=f"image/{img_fmt.lower()}"
    )
