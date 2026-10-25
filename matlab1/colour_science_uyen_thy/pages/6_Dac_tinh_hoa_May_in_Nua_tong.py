import streamlit as st
from page_style import apply_page_style
import matplotlib.pyplot as plt
import colour
import numpy as np
import scipy.io
import os

apply_page_style()

st.markdown("## 🖨️ Đặc tính hoá máy in nửa tông (Halftone)")
st.markdown("""
Phân tích phổ phản xạ của các mẫu in nửa tông vàng (**Yellow**) và tím (**Magenta**)
sử dụng mô hình **Demichel** và đường cong tái tạo tông màu.
""")
st.markdown("---")

# ── Tìm file halftone.mat ──────────────────────────────────────────────────────
MAT_PATH = os.path.join(os.path.dirname(__file__), "..", "halftone.mat")
MAT_PATH = os.path.normpath(MAT_PATH)

@st.cache_data
def load_halftone(path):
    data = scipy.io.loadmat(path)
    W = data["W"]
    P = data["P"]
    P = np.vstack((W, P))
    yellow = P[:11, :]
    magenta = np.zeros((11, 31), np.float64)
    for i in range(11):
        magenta[i, :] = P[i * 11, :]
    return P, yellow, magenta

def rgb_from_spectrum(reflection):
    """Chuyển phổ phản xạ 31 bước (400–700nm) sang RGB uint8."""
    dict_r = {400 + i * 10: reflection[i] for i in range(31)}
    sd = colour.SpectralDistribution(dict_r)
    cmfs = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
    illuminant = colour.SDS_ILLUMINANTS["D65"]
    XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
    RGB = colour.XYZ_to_sRGB(XYZ / 100)
    RGB = np.clip(RGB, 0, 1) * 255
    return RGB.astype(np.uint8)

def gettrc(dig, R, W, Solid, n=20):
    """Tính đường cong tái tạo tông màu (TRC)."""
    R_n = R ** (1 / n)
    W_n = W ** (1 / n)
    S_n = Solid ** (1 / n)
    num = len(dig)
    c = np.zeros(num, np.float64)
    for i in range(num):
        c[i] = np.sum((S_n - R_n[i, :]) * (S_n - W_n)) / np.sum((S_n - W_n) * (S_n - W_n))
    c = 1 - c
    p = np.polyfit(dig, c, 3)
    return c, p

if not os.path.exists(MAT_PATH):
    st.error(f"❌ Không tìm thấy file `halftone.mat` tại: `{MAT_PATH}`")
    st.info("Vui lòng đặt file `halftone.mat` vào thư mục gốc của project.")
    st.stop()

P, yellow, magenta = load_halftone(MAT_PATH)

# ── Sidebar chọn mục ──────────────────────────────────────────────────────────
menu = st.sidebar.radio(
    "Chọn nội dung",
    [
        "1. Ảnh trộn màu Yellow & Magenta",
        "2. Phổ màu Yellow & Magenta",
        "3. Đường cong tái tạo tông màu",
        "4. Dự báo phổ khi trộn 2 màu",
    ],
)

wave = np.linspace(400, 700, 31)
a_target = np.linspace(0, 1, 11)

# ══════════════════════════════════════════════════════════════════════════════
if menu == "1. Ảnh trộn màu Yellow & Magenta":
    st.markdown("### Ảnh trộn màu Yellow × Magenta (11×11 mẫu)")
    st.markdown("Mỗi ô trong ảnh là màu thu được khi trộn Yellow (trục X) và Magenta (trục Y) với tỉ lệ từ 0 đến 1.")

    SIZE = 40
    image = np.zeros((SIZE * 11, SIZE * 11, 3), np.uint8)
    k = 0
    for x in range(11):
        for y in range(11):
            RGB = rgb_from_spectrum(P[k])
            image[x * SIZE:(x + 1) * SIZE, y * SIZE:(y + 1) * SIZE, :] = RGB
            k += 1
    image = image[::-1, :, :]

    _, col, _ = st.columns([1, 3, 1])
    with col:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(image)
        xticks = list(range(20, 440, 40))
        yticks = list(range(20, 440, 40))
        ax.set_xticks(xticks)
        ax.set_xticklabels([f"{v:.1f}" for v in np.linspace(0, 1, 11)], fontsize=8)
        ax.set_yticks(yticks)
        ax.set_yticklabels([f"{v:.1f}" for v in np.linspace(1, 0, 11)], fontsize=8)
        ax.set_xlabel("Yellow (tỉ lệ)", fontsize=11)
        ax.set_ylabel("Magenta (tỉ lệ)", fontsize=11)
        ax.set_title("Ảnh trộn màu Yellow × Magenta\n(Mô hình Demichel – 11×11 mẫu)", fontsize=12)
        st.pyplot(fig, clear_figure=True)

    st.info("""
**Giải thích:** Mỗi ô được tính từ phổ phản xạ đo thực tế trên máy in.  
Yellow tăng dần theo trục X (trái → phải); Magenta tăng dần theo trục Y (trên → dưới).
    """)

# ══════════════════════════════════════════════════════════════════════════════
elif menu == "2. Phổ màu Yellow & Magenta":
    st.markdown("### Phổ phản xạ màu Yellow và Magenta trên nền trắng")
    st.markdown("11 đường phổ ứng với tỉ lệ trame **a = 0, 0.1, 0.2, ..., 1.0**")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        for i in range(11):
            ax.plot(wave, yellow[i], color="#FF8800", alpha=0.6 + i * 0.04, linewidth=1.5)
        ax.set_xlim([400, 700])
        ax.set_ylim([0, 1.05])
        ax.set_xlabel("Bước sóng (nm)", fontsize=11)
        ax.set_ylabel("Phổ phản xạ", fontsize=11)
        ax.set_title("Phổ màu Yellow\n(a = 0 → 1)", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig, clear_figure=True)

    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        for i in range(11):
            ax.plot(wave, magenta[i], color="#CC00CC", alpha=0.6 + i * 0.04, linewidth=1.5)
        ax.set_xlim([400, 700])
        ax.set_ylim([0, 1.05])
        ax.set_xlabel("Bước sóng (nm)", fontsize=11)
        ax.set_ylabel("Phổ phản xạ", fontsize=11)
        ax.set_title("Phổ màu Magenta\n(a = 0 → 1)", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig, clear_figure=True)

# ══════════════════════════════════════════════════════════════════════════════
elif menu == "3. Đường cong tái tạo tông màu":
    st.markdown("### Đường cong tái tạo tông màu (TRC – Tone Reproduction Curve)")
    st.markdown("So sánh giá trị tông màu **mục tiêu** (target) và **thực tế** (actual) sau khi in.")

    n_val = st.sidebar.slider("Hệ số n (Yule-Nielsen)", 1, 40, 20)

    col1, col2 = st.columns(2)

    with col1:
        a_actual_y, p_y = gettrc(a_target, yellow, yellow[0, :], yellow[10, :], n_val)
        x_ve = np.linspace(0, 1, 101)
        y_ve = np.polyval(p_y, x_ve)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(a_target, a_actual_y, "o", color="#FF8800", markersize=8, label="Thực tế")
        ax.plot(x_ve, y_ve, color="black", linewidth=1.5, label="Fit bậc 3")
        ax.plot([0, 1], [0, 1], "--", color="#aaa", linewidth=1, label="Lý tưởng")
        ax.set_xlabel("Giá trị mục tiêu (a)", fontsize=11)
        ax.set_ylabel("Giá trị thực tế (a)", fontsize=11)
        ax.set_title("TRC – Yellow", fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig, clear_figure=True)

    with col2:
        a_actual_m, p_m = gettrc(a_target, magenta, magenta[0, :], magenta[10, :], n_val)
        y_ve_m = np.polyval(p_m, x_ve)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(a_target, a_actual_m, "o", color="#CC00CC", markersize=8, label="Thực tế")
        ax.plot(x_ve, y_ve_m, color="black", linewidth=1.5, label="Fit bậc 3")
        ax.plot([0, 1], [0, 1], "--", color="#aaa", linewidth=1, label="Lý tưởng")
        ax.set_xlabel("Giá trị mục tiêu (a)", fontsize=11)
        ax.set_ylabel("Giá trị thực tế (a)", fontsize=11)
        ax.set_title("TRC – Magenta", fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig, clear_figure=True)

    st.info(f"""
**Công thức Yule-Nielsen:**  
c = 1 - Σ[(S^(1/n) - R^(1/n)) · (S^(1/n) - W^(1/n))] / Σ[(S^(1/n) - W^(1/n))²]  
với n = {n_val}, khớp đa thức bậc 3.
    """)

# ══════════════════════════════════════════════════════════════════════════════
elif menu == "4. Dự báo phổ khi trộn 2 màu":
    st.markdown("### Dự báo phổ phản xạ khi trộn Yellow và Magenta")
    st.markdown("Sử dụng mô hình **Demichel** để dự báo phổ phản xạ tại tỉ lệ trame bất kỳ.")

    pham_vi = [round(x, 1) for x in np.linspace(0, 1, 11)]

    _, col, _ = st.columns([1, 2, 1])
    with col:
        a_mag_target = st.select_slider("Tỉ lệ trame Magenta (a_mag)", options=pham_vi, value=0.5)
        a_yel_target = st.select_slider("Tỉ lệ trame Yellow (a_yel)",  options=pham_vi, value=0.5)

        if st.button("🔮 Dự báo phổ phản xạ", use_container_width=True):
            n_val = 20
            vi_tri_mag = pham_vi.index(a_mag_target)
            vi_tri_yel = pham_vi.index(a_yel_target)
            i = vi_tri_mag * 11 + vi_tri_yel
            meas = P[i, :]

            _, p_mag = gettrc(a_target, magenta, magenta[0, :], magenta[10, :], n_val)
            _, p_yel = gettrc(a_target, yellow,  yellow[0, :],  yellow[10, :],  n_val)

            a_mag_actual = np.polyval(p_mag, a_mag_target)
            a_yel_actual = np.polyval(p_yel, a_yel_target)

            Am = a_mag_actual * (1 - a_yel_actual)
            Ay = a_yel_actual * (1 - a_mag_actual)
            Aw = (1 - a_mag_actual) * (1 - a_yel_actual)
            Ao = a_mag_actual * a_yel_actual

            overlap = P[120, :]
            WW = P[0, :]

            pred = np.zeros(31, np.float64)
            for w in range(31):
                pred[w] = (
                    Am * (magenta[10, w]) ** (1 / n_val)
                    + Ay * (yellow[10, w])  ** (1 / n_val)
                    + Ao * (overlap[w])     ** (1 / n_val)
                    + Aw * (WW[w])          ** (1 / n_val)
                ) ** n_val

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(wave, meas, "ro", markersize=6, label="Đo thực tế")
            ax.plot(wave, pred, "b-",  linewidth=2,  label="Dự báo Demichel")
            ax.set_ylim([0, 1])
            ax.set_xlim([400, 700])
            ax.set_xlabel("Bước sóng (nm)", fontsize=11)
            ax.set_ylabel("Phổ phản xạ",    fontsize=11)
            ax.set_title(
                f"Phổ phản xạ khi trộn Magenta={a_mag_target} × Yellow={a_yel_target}",
                fontsize=11,
            )
            ax.legend(fontsize=10)
            ax.grid(True, linestyle="--", alpha=0.4)
            st.pyplot(fig, clear_figure=True)

            # Sai số RMSE
            rmse = np.sqrt(np.mean((meas - pred) ** 2))
            st.metric("RMSE (sai số dự báo)", f"{rmse:.5f}")
            st.info(f"""
**Kết quả Demichel:**
- a_mag (thực tế) = {a_mag_actual:.4f} | a_yel (thực tế) = {a_yel_actual:.4f}
- Vùng Magenta thuần: Am = {Am:.4f}
- Vùng Yellow thuần:  Ay = {Ay:.4f}
- Vùng trắng:         Aw = {Aw:.4f}
- Vùng overlap (MY):  Ao = {Ao:.4f}
            """)

st.markdown("---")
st.caption("Mô hình Yule-Nielsen & Demichel | Dữ liệu halftone.mat | colour-science CIE 1931 D65")
