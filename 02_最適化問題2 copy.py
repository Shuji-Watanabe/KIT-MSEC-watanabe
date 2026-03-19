import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import interp1d, make_interp_spline
from scipy.optimize import fsolve

# ---------------------------------
# 定数
# ---------------------------------
G = 9.80665
EPS_Y = 1e-10
NUM_POINTS = 1000
DEFAULT_INTERP_LABEL = "キュービック補間"

# ---------------------------------
# Streamlit UI
# ---------------------------------
st.title("最適化問題２")

st.header("初期パラメータの設定", divider="violet")
with st.expander("設定の確認・変更"):
    """ ##### 原点と座標軸
    原点＝始点，x軸の向き：右向き正，y軸の向き：下向き正
    """

    """ ##### 終点の位置の設定 """
    input_cols = st.columns([1] * 4)

    with input_cols[0]:
        a = st.number_input(
            "終点の $x$ 座標 $\\rm [m]$",
            min_value=float(0.001),
            value=float(np.pi),
            format="%.3f",
            step=0.001,
        )
        a = float(a)

    with input_cols[1]:
        b = st.number_input(
            "終点の $y$ 座標 $\\rm [m]$",
            min_value=float(0.001),
            value=float(2.0),
            format="%.3f",
            step=0.001,
        )
        b = float(b)

    f""" ##### 分割数
    $x=0$ から $x={a:.3f}$ の間を $N$ 分割します．（初期設定は等分割）
    """

    if "N" not in st.session_state:
        st.session_state.N = 10
    if "saved_datasets" not in st.session_state:
        st.session_state.saved_datasets = []

    N_col = st.columns([1, 1, 1])
    with N_col[0]:
        N_input = st.number_input(
            "分割数 N",
            min_value=1,
            max_value=20,
            value=int(st.session_state.N),
            step=1,
        )

    with N_col[2]:
        if st.session_state.N != N_input:
            if st.button("分割数$N$を更新しますか?"):
                st.session_state.N = int(N_input)
                st.session_state.saved_datasets = []
                with N_col[1]:
                    st.success("更新完了")
            else:
                with N_col[1]:
                    st.write(f"$N={st.session_state.N}$を使用")

    """ ##### 補間方法 """
    interp_label = st.radio(
        "補間方法を選択",
        ["線形補間", "キュービック補間"],
        index=1,
        horizontal=True,
    )

N = int(st.session_state.N)

# ---------------------------------
# コア関数
# ---------------------------------
def nonuniform_nodes(a, N, gamma_nodes=1.0):
    """区間 [0, a] を N 分割した節点を返す．
    gamma_nodes=1 なら等分割，それ以外では非一様分割になる．"""
    u = np.linspace(0, 1, N + 1)
    return a * u**gamma_nodes


def resolve_interp_method(interp_label, num_nodes):
    """UIの補間法表示を内部表現へ変換する．
    節点数が少なく cubic が使えないときは linear に自動変更する．"""
    if interp_label == "線形補間":
        return "linear"
    if num_nodes < 4:
        return "linear"
    return "cubic"


def path_time_from_samples(xs, ys, g=G, eps=EPS_Y):
    """細かい点列 (xs, ys) に沿って移動時間を数値評価する．
    各微小区間で ds / sqrt(2gy) を足し合わせる形で近似している．"""
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    dx = np.diff(xs)
    dy = np.diff(ys)
    ds = np.hypot(dx, dy)

    y_mid = 0.5 * (ys[:-1] + ys[1:])
    y_mid = np.maximum(y_mid, eps)

    v_mid = np.sqrt(2 * g * y_mid)
    return np.sum(ds / v_mid)


def linear_segment_time(x0, y0, x1, y1, g=G, eps=EPS_Y):
    """線形補間された1区間の移動時間を返す．
    区間内では y(x) が一次関数なので，時間積分を解析的に計算する．"""
    dx = float(x1 - x0)
    dy = float(y1 - y0)
    ds = np.hypot(dx, dy)

    y0s = max(float(y0), eps)
    y1s = max(float(y1), eps)

    if abs(dy) < 1e-14:
        yref = max(0.5 * (y0s + y1s), eps)
        return ds / np.sqrt(2 * g * yref)

    return (2.0 * ds / (np.sqrt(2 * g) * dy)) * (np.sqrt(y1s) - np.sqrt(y0s))


def travel_time_linear_exact(yk, xk, g=G, eps=EPS_Y):
    """折れ線経路の移動時間を区間ごとに厳密計算する．
    線形補間を使うときの評価関数で，数値積分誤差を抑えやすい．"""
    xk = np.asarray(xk, dtype=float)
    yk = np.asarray(yk, dtype=float)

    total = 0.0
    for i in range(len(xk) - 1):
        total += linear_segment_time(xk[i], yk[i], xk[i + 1], yk[i + 1], g=g, eps=eps)
    return total


def interpolate_path(xk, yk, interp_method="linear", degree=3, num_points=NUM_POINTS):
    """節点列 (xk, yk) を補間し，曲線上の点列を返す．
    描画用と，cubic 時間評価用の両方で使う関数である．"""
    xk = np.asarray(xk, dtype=float)
    yk = np.asarray(yk, dtype=float)

    if interp_method == "linear":
        f = interp1d(xk, yk, kind="linear")
    elif interp_method == "quadratic":
        f = make_interp_spline(xk, yk, k=2)
    elif interp_method == "cubic":
        if len(xk) < 4:
            f = interp1d(xk, yk, kind="linear")
        else:
            f = make_interp_spline(xk, yk, k=3)
    elif interp_method == "bspline":
        f = make_interp_spline(xk, yk, k=degree)
    else:
        raise ValueError(f"Unknown interp_method: {interp_method}")

    xs = np.linspace(xk[0], xk[-1], num_points)
    ys = f(xs)
    ys = np.maximum(ys, 0.0)
    return xs, ys

def travel_time_original(yk, xk, g=G, eps=EPS_Y):
    xk = np.asarray(xk, dtype=float)
    yk = np.asarray(yk, dtype=float)

    dx = np.diff(xk)
    dy = np.diff(yk)
    ds = np.hypot(dx, dy)

    denom = g * (yk[:-1] + yk[1:])
    denom = np.maximum(denom, eps)

    v = np.sqrt(denom)
    return np.sum(ds / v)

def travel_time_numeric_cubic(
    yk,
    xk,
    g=G,
    degree=3,
    num_points=NUM_POINTS,
    eps=EPS_Y,
):
    """cubic 補間した曲線の移動時間を数値評価する．
    補間後の曲線を細かく刻み，ds / sqrt(2gy) の和で近似している．"""
    xs, ys = interpolate_path(
        xk,
        yk,
        interp_method="cubic",
        degree=degree,
        num_points=num_points,
    )
    return path_time_from_samples(xs, ys, g=g, eps=eps)


# def travel_time(yk, xk, interp_method, g=G, num_points=NUM_POINTS, eps=EPS_Y):
#     """補間法に応じて移動時間を切り替えて返す．
#     linear では区間厳密計算，cubic では補間後の数値評価を使う．"""
#     if interp_method == "linear":
#         return travel_time_linear_exact(yk, xk, g=g, eps=eps)
#     return travel_time_numeric_cubic(yk, xk, g=g, num_points=num_points, eps=eps)
def travel_time(
    yk,
    xk,
    interp_method,
    objective_label="改良モデル（物理的に正しい）",
    g=G,
    num_points=NUM_POINTS,
    eps=EPS_Y,
):
    # 👉 元の式を選んだ場合
    if objective_label == "元の式（比較用）":
        return travel_time_original(yk, xk, g=g, eps=eps)

    # 👉 従来の処理
    if interp_method == "linear":
        return travel_time_linear_exact(yk, xk, g=g, eps=eps)
    return travel_time_numeric_cubic(yk, xk, g=g, num_points=num_points, eps=eps)

def compute_gradient(yk, xk, interp_method):
    """移動時間の y 方向微分を有限差分で近似する．
    差分幅を少し大きめに取り，数値ノイズに強くしている．"""
    N_local = len(xk) - 1
    grad = np.zeros_like(yk, dtype=float)

    for i in range(1, N_local):
        h = 1e-4 * max(1.0, abs(float(yk[i])))

        ykp = np.array(yk, dtype=float)
        ykm = np.array(yk, dtype=float)

        ykp[i] += h
        ykm[i] = max(1e-8, ykm[i] - h)

        Tp = travel_time(ykp, xk, interp_method=interp_method)
        Tm = travel_time(ykm, xk, interp_method=interp_method)

        grad[i] = (Tp - Tm) / (2.0 * h)

    return grad


def steepest_descent_time_momentum(
    a,
    b,
    N,
    interp_method,
    yk=None,
    gamma_nodes=1.5,
    kappa=2.0,
    delta=0.2,
    alpha=0.05,
    beta=0.01,
    momentum=0.2,
    max_iter=5000,
    tol=1e-6,
):
    """移動時間を減らすように節点を更新する．
    更新後に時間が悪化した場合は step を小さくしてやり直す．"""
    xk = nonuniform_nodes(a, N, gamma_nodes)

    if yk is None:
        yk = b * (xk / a)
    else:
        yk = np.array(yk, dtype=float)

    v = np.zeros_like(yk)
    u = xk / a

    lr_factor = 1 / (1 + np.exp(-kappa * (u - delta)))
    lr_factor[0] = 0.0
    lr_factor[-1] = 0.0

    T_old = travel_time(yk, xk, interp_method=interp_method)

    for k in range(max_iter):
        grad = compute_gradient(yk, xk, interp_method=interp_method)

        # 勾配を少し丸める
        g_norm = np.linalg.norm(grad[1:-1])
        if g_norm > 10.0:
            grad[1:-1] *= 10.0 / g_norm

        base_step = alpha / (1.0 + beta * k)
        step = base_step
        accepted = False

        while step > 1e-8:
            update = step * lr_factor * grad
            v_trial = momentum * v + update

            y_trial = yk.copy()
            y_trial[1:-1] -= v_trial[1:-1]
            y_trial[1:-1] = np.maximum(y_trial[1:-1], 1e-8)
            y_trial[0], y_trial[-1] = 0.0, b

            T_new = travel_time(y_trial, xk, interp_method=interp_method)

            if T_new <= T_old:
                accepted = True
                yk = y_trial
                v = v_trial
                T_old = T_new
                break

            step *= 0.5

        if not accepted:
            break

        if np.linalg.norm(step * grad[1:-1]) < tol:
            break
    st.write(f"** 最適化回数={k}回 **")
    return xk, yk


def solve_theta(a, b):
    """終点 (a, b) を通るサイクロイドの終端パラメータ theta を求める．
    非線形方程式を fsolve で数値的に解いている．"""
    func = lambda th: (th - np.sin(th)) / (1 - np.cos(th)) - a / b
    return fsolve(func, np.pi)[0]


def exact_cycloid(a, b, num=NUM_POINTS):
    """終点 (a, b) を結ぶサイクロイドの座標列を返す．
    可視化用にも数値評価用にも使えるよう点列として出力する．"""
    theta1 = solve_theta(a, b)
    th = np.linspace(0, theta1, num)
    R = b / (1 - np.cos(theta1))
    x = R * (th - np.sin(th))
    y = R * (1 - np.cos(th))
    return x, y


def exact_cycloid_time_theory(a, b, g=G):
    """サイクロイドの理論式から厳密な移動時間を返す．
    時間は T = theta1 * sqrt(R / g) で与えられる．"""
    theta1 = solve_theta(a, b)
    R = b / (1 - np.cos(theta1))
    return theta1 * np.sqrt(R / g)


def exact_cycloid_time_numeric(a, b, g=G, num_points=NUM_POINTS):
    """サイクロイドを細かい点列にして数値評価する．
    理論値との差を見ることで数値誤差の目安を確認できる．"""
    xc, yc = exact_cycloid(a, b, num=num_points)
    return path_time_from_samples(xc, yc, g=g)


def add_path_trace(fig, xk, yk, interp_method, name, line_style=None, marker_size=7):
    """補間曲線と節点を図に追加する．
    表示される曲線が，現在選んだ補間法に対応するようにしている．"""
    xs, ys = interpolate_path(xk, yk, interp_method=interp_method, num_points=NUM_POINTS)

    if line_style is None:
        line_style = {}

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            name=name,
            line=line_style,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=xk,
            y=yk,
            mode="markers",
            name=f"{name} の節点",
            marker=dict(size=marker_size),
            showlegend=False,
        )
    )

# ---------------------------------
# UI用データ準備
# ---------------------------------
xk = nonuniform_nodes(a, N, gamma_nodes=1.0)
interp_method = resolve_interp_method(interp_label, len(xk))

if interp_label == "キュービック補間" and len(xk) < 4:
    st.warning("キュービック補間には少なくとも4個の節点が必要なため，現在は線形補間で計算しています．")

""" ##### 目的関数の選択 """
objective_label = st.radio(
    "目的関数",
    ["改良モデル（物理的に正しい）", "元の式（比較用）"],
    index=0,
    horizontal=True,
)

col2_0 = st.columns([2, 1])
with col2_0[0]:
    mode = st.radio("モード選択", ["手動最適化", "自動最適化"], horizontal=True)

with col2_0[1]:
    code_input = st.text_input("解答表示のパスワード")

# ---------------------------------
# 手動最適化モード
# ---------------------------------
if mode == "手動最適化":
    st.markdown("### 各通過点の y 座標入力")

    Col_num = 5
    data_col = st.columns([1, 1, 1, 1, 2])

    with data_col[-1]:
        if st.session_state.saved_datasets:
            idx = st.selectbox(
                "保存済みデータを選択",
                list(range(len(st.session_state.saved_datasets))),
                format_func=lambda i: f"データ {i}",
                key="select_dataset",
            )
            selected_y = st.session_state.saved_datasets[idx]["y"]
        else:
            selected_y = None

    yk = []
    Input_cols = st.columns(Col_num)

    for j in range(len(xk)):
        if j == 0:
            Input_cols = st.columns(Col_num)
            with Input_cols[0]:
                st.number_input(
                    f"$y_{{{j}}}$",
                    value=float(0.0),
                    min_value=float(0.0),
                    max_value=float(0.0),
                    key=f"manual_y_{j}",
                )
            yk.append(0.0)

        elif j == len(xk) - 1:
            Input_cols = st.columns(Col_num)
            with Input_cols[0]:
                st.number_input(
                    f"$y_{{{j}}}$",
                    value=float(b),
                    min_value=float(b),
                    max_value=float(b),
                    format="%.4f",
                    step=0.01,
                    key=f"manual_y_{j}",
                )
            yk.append(float(b))

        else:
            if j == 1:
                Input_cols = st.columns(Col_num)

            default = selected_y[j] if selected_y is not None else b * (xk[j] / a)

            with Input_cols[(j - 1) % Col_num]:
                yj = st.number_input(
                    f"$y_{{{j}}}$",
                    value=float(default),
                    min_value=float(0.0),
                    format="%.4f",
                    step=0.01,
                    key=f"manual_y_{j}",
                )
            yk.append(float(yj))

    T_manual = travel_time(np.array(yk, dtype=float), xk, interp_method=interp_method)

    with data_col[0]:
        if st.button("保　　存"):
            st.session_state.saved_datasets.append({"y": yk.copy()})
            with data_col[3]:
                st.success("処理完了")

    with data_col[1]:
        if st.button("リセット"):
            for j in range(1, len(xk) - 1):
                st.session_state.pop(f"manual_y_{j}", None)
            st.session_state.saved_datasets = []
            with data_col[3]:
                st.success("処理完了")

    with data_col[2]:
        if st.button("更　　新"):
            with data_col[3]:
                st.success("処理完了")

    if st.session_state.saved_datasets:
        col1, col2 = st.columns([1, 1])

        with col2:
            times = [
                travel_time(np.array(d["y"], dtype=float), xk, interp_method=interp_method)
                for d in st.session_state.saved_datasets
            ]
            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=list(range(len(times))),
                    y=times,
                    mode="lines+markers",
                    name="保存時間",
                )
            )
            fig2.update_layout(
                title=f"保存データの移動時間（{interp_label}）",
                xaxis_title="データ番号",
                yaxis_title="移動時間 T",
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col1:
            fig = go.Figure()

            add_path_trace(
                fig,
                xk,
                np.array(yk, dtype=float),
                interp_method=interp_method,
                name="手動解",
                line_style=dict(width=3),
            )

            if code_input == "5963":
                xc, yc = exact_cycloid(a, b)
                fig.add_trace(
                    go.Scatter(
                        x=xc,
                        y=yc,
                        mode="lines",
                        name="厳密解 (Cycloid)",
                        line=dict(color="orange", dash="dash", width=3),
                    )
                )

            fig.update_layout(
                title=f"手動解 (T = {T_manual:.4f} 秒, {interp_label})",
                xaxis_title="x",
                yaxis_title="y",
                yaxis_autorange="reversed",
                legend=dict(
                    x=1,
                    y=1,
                    xanchor="right",
                    yanchor="top",
                    bgcolor="rgba(255,255,255,0.5)",
                    bordercolor="black",
                    borderwidth=1,
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        yk_default = [0.0] + [b * (x / a) for x in xk[1:-1]] + [b]
        st.session_state.saved_datasets.append({"y": yk_default})

# ---------------------------------
# 自動最適化モード
# ---------------------------------
elif mode == "自動最適化":
    st.markdown("### 自動最適化（手動最適化の結果を初期値に使用）")

    if st.session_state.saved_datasets:
        best = min(
            st.session_state.saved_datasets,
            key=lambda d: travel_time(np.array(d["y"], dtype=float), xk, interp_method=interp_method),
        )
        yk_init = np.array(best["y"], dtype=float)
    else:
        yk_init = np.array([0.0] + [b * (x / a) for x in xk[1:-1]] + [b], dtype=float)

    if st.button("Start Optimization"):

        # 安定性重視なら，最適化は linear にして表示だけ現在の補間法にする方法もある
        optimize_interp_method = interp_method

        xk_opt, yk_opt = steepest_descent_time_momentum(
            a,
            b,
            N,
            interp_method=optimize_interp_method,
            yk=yk_init,
            gamma_nodes=1,
            kappa=2.0,
            delta=0.2,
            alpha=1.5,
            beta=0.01,
            momentum=0.2,
            max_iter=50000,
            tol=1e-12,
        )

        # T_init = travel_time(yk_init, xk, interp_method=interp_method)
        # T_auto = travel_time(yk_opt, xk_opt, interp_method=interp_method)
        T_init = travel_time(
            yk_init, xk, interp_method=interp_method, objective_label=objective_label
        )
        T_auto = travel_time(
            yk_opt, xk_opt, interp_method=interp_method, objective_label=objective_label
        )
        xc, yc = exact_cycloid(a, b, num=NUM_POINTS)
        T_exact_num = exact_cycloid_time_numeric(a, b)
        T_exact_theory = exact_cycloid_time_theory(a, b)

        fig = go.Figure()

        add_path_trace(
            fig,
            xk,
            yk_init,
            interp_method=interp_method,
            name="初期解",
            line_style=dict(width=3),
        )

        add_path_trace(
            fig,
            xk_opt,
            yk_opt,
            interp_method=interp_method,
            name="最適化経路",
            line_style=dict(width=3),
        )

        if code_input == "5963":
            fig.add_trace(
                go.Scatter(
                    x=xc,
                    y=yc,
                    mode="lines",
                    name="厳密解 (Cycloid)",
                    line=dict(color="orange", dash="dash", width=3),
                )
            )

        fig.update_layout(
            title=f"自動最適化結果（{interp_label}）",
            xaxis_title="x",
            yaxis_title="y",
            yaxis_autorange="reversed",
        )
        st.plotly_chart(fig, use_container_width=True)

        """#### 移動時間"""
        Result_col = st.columns(2)
        with Result_col[0]:
            st.write(f"初期経路: {T_init:.4f} 秒")
            st.write(f"サイクロイド（数値評価）: {T_exact_num:.4f} 秒")
        with Result_col[1]:
            st.write(f"自動最適化経路: {T_auto:.4f} 秒")
            st.write(f"サイクロイド（理論値）: {T_exact_theory:.4f} 秒")