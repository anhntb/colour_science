import streamlit as st
from page_style import apply_page_style
import matplotlib.pyplot as plt
import numpy as np
import colour

apply_page_style()

st.markdown("## 🌈 Biểu đồ CIE dạng Band (400–700 nm)")
st.markdown("""
Biểu đồ CIE **dạng dải màu** (band) hiển thị màu sắc của từng bước sóng ánh sáng
trong vùng nhìn thấy từ **400 nm** đến **700 nm**, được tô màu đúng với màu quang phổ thực tế.
""")
st.markdown("---")

# ── Helper: wavelength → RGB dùng CMF trực tiếp (không dùng sd_to_XYZ) ────────
@st.cache_data

def build_spectrum_lut():
    """
    Tạo bảng tra RGB cho từng bước sóng 400–700 nm
    từ hàm so màu CIE 1931 2 Degree Standard Observer.
    """
    cmfs = colour.MSDS_CMFS[
        "CIE 1931 2 Degree Standard Observer"
    ]

    wl_arr = np.arange(400, 701, 1, dtype=np.float64)
    wl_cmf = cmfs.wavelengths
    vals = cmfs.values  # Shape (N, 3)

    rgb_arr = np.zeros((len(wl_arr), 3), dtype=np.float32)

    for i, wl in enumerate(wl_arr):
        # Nội suy các hàm so màu CIE
        x_bar = np.interp(wl, wl_cmf, vals[:, 0])
        y_bar = np.interp(wl, wl_cmf, vals[:, 1])
        z_bar = np.interp(wl, wl_cmf, vals[:, 2])

        XYZ = np.array([x_bar, y_bar, z_bar], dtype=np.float64)

        # Chuẩn hóa để tránh chia cho 0
        total = np.sum(XYZ)
        if total > 0:
            XYZ = XYZ / total

        # Chuyển XYZ sang sRGB
        RGB = colour.XYZ_to_sRGB(XYZ)
        RGB = np.clip(RGB, 0.0, 1.0)

        rgb_arr[i] = RGB.astype(np.float32)

    return wl_arr, rgb_arr


@st.cache_data
def build_band_image(
    wl_start=400,
    wl_end=700,
    img_width=600,
    img_height=80
):
    wl_lut, rgb_lut = build_spectrum_lut()

    img = np.zeros(
        (img_height, img_width, 3),
        dtype=np.float32
    )

    wl_cols = np.linspace(wl_start, wl_end, img_width)

    for col_idx, wl in enumerate(wl_cols):
        # Chuyển bước sóng thành index trong LUT
        idx = int(round(wl - wl_lut[0]))
        idx = max(0, min(idx, len(rgb_lut) - 1))

        img[:, col_idx, :] = rgb_lut[idx]

    return img, wl_cols



# ── Sidebar tuỳ chọn ──────────────────────────────────────────────────────────
st.sidebar.markdown("### Tuỳ chọn hiển thị")
band_height = st.sidebar.slider("Chiều cao dải màu (px)", 30, 150, 80, 10)
show_ticks  = st.sidebar.checkbox("Hiển thị nhãn bước sóng", value=True)
tick_step   = st.sidebar.select_slider("Khoảng cách nhãn (nm)", [10, 20, 25, 50, 100], value=50)
show_cie    = st.sidebar.checkbox("Hiển thị biểu đồ CIE bên dưới", value=True)

# ── Vẽ dải màu band ───────────────────────────────────────────────────────────
with st.spinner("Đang tạo dải màu quang phổ..."):
    img, wavelengths = build_band_image(400, 700, img_width=600, img_height=band_height)

fig, ax = plt.subplots(figsize=(10, band_height / 40 + 1.4))
ax.imshow(img, aspect="auto", extent=[400, 700, 0, 1])
ax.set_xlim([400, 700])
ax.set_ylim([0, 1])
ax.set_yticks([])

if show_ticks:
    tick_positions = list(range(400, 701, tick_step))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([str(t) for t in tick_positions], fontsize=9)
    ax.set_xlabel("Bước sóng (nm)", fontsize=11)
else:
    ax.set_xticks([])

ax.set_title("Visible Spectrum — CIE Band (400–700 nm)", fontsize=13, pad=8)

# Nhãn màu đặc trưng
landmarks = {
    420: "Tím", 455: "Lam", 505: "Lục lam",
    535: "Lục", 580: "Vàng", 605: "Cam", 655: "Đỏ",
}
for wl_lm, name in landmarks.items():
    ax.axvline(wl_lm, color="white", linewidth=0.7, alpha=0.5)
    ax.text(wl_lm, 0.97, name, color="white", fontsize=7,
            ha="center", va="top", rotation=90)

plt.tight_layout()
st.pyplot(fig, clear_figure=True)

# ── Bảng màu đặc trưng ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Bảng màu đặc trưng theo bước sóng")

wl_lut, rgb_lut = build_spectrum_lut()

landmark_ranges = [
    (400, 450, "Tím (Violet)"),
    (450, 495, "Lam (Blue)"),
    (495, 530, "Lục lam (Cyan)"),
    (530, 560, "Lục (Green)"),
    (560, 590, "Vàng lục (Yellow-Green)"),
    (590, 620, "Vàng – Cam (Yellow–Orange)"),
    (620, 700, "Đỏ (Red)"),
]

cols = st.columns(4)
for idx, (wl_s, wl_e, name) in enumerate(landmark_ranges):
    wl_mid = (wl_s + wl_e) // 2
    lut_idx = max(0, min(wl_mid - 400, len(rgb_lut) - 1))
    rgb = rgb_lut[lut_idx]
    hex_c = "#{:02X}{:02X}{:02X}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    with cols[idx % 4]:
        st.markdown(f"""
        <div style='background:{hex_c};border-radius:6px;height:40px;
                    border:1px solid #555;margin-bottom:4px'></div>
        <p style='font-size:12px;color:#ccc;margin:0 0 10px 0;text-align:center'>
            <b>{wl_s}–{wl_e} nm</b><br>{name}
        </p>
        """, unsafe_allow_html=True)

# ── Biểu đồ CIE với spectrum locus 400–700 nm ────────────────────────────────
if show_cie:
    st.markdown("---")
    st.markdown("### Biểu đồ CIE 1931 – Spectrum Locus (400–700 nm)")
    st.markdown("""
    Các điểm màu trên **spectrum locus** (đường viền hình móng ngựa) được tô màu đúng
    với màu quang phổ tương ứng từ 400 đến 700 nm.
    """)

    cmfs = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
    wl_cmf = cmfs.wavelengths
    vals   = cmfs.values  # (N, 3): x̄, ȳ, z̄

    figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    axes.set_xlim([-0.05, 0.80])
    axes.set_ylim([-0.05, 0.90])
    axes.set_title("CIE 1931 – Spectrum Locus (400–700 nm highlighted)", fontsize=12)

    step = 5  # vẽ mỗi 5 nm
    for wl in range(400, 701, step):
        x_bar = np.interp(wl, wl_cmf, vals[:, 0])
        y_bar = np.interp(wl, wl_cmf, vals[:, 1])
        z_bar = np.interp(wl, wl_cmf, vals[:, 2])
        s = x_bar + y_bar + z_bar
        if s < 1e-10:
            continue
        x_pt = x_bar / s
        y_pt = y_bar / s

        lut_idx = max(0, min(wl - 400, len(rgb_lut) - 1))
        rgb_pt  = rgb_lut[lut_idx]
        hex_pt  = "#{:02X}{:02X}{:02X}".format(
            int(rgb_pt[0]*255), int(rgb_pt[1]*255), int(rgb_pt[2]*255))

        axes.plot(x_pt, y_pt, "o", color=hex_pt, markersize=6,
                  markeredgecolor="white", markeredgewidth=0.4, zorder=5)

        # Nhãn mỗi 50 nm
        if wl % 50 == 0:
            axes.annotate(f"{wl} nm", (x_pt, y_pt),
                          textcoords="offset points", xytext=(5, 3),
                          fontsize=8, color="black",
                          bbox=dict(boxstyle="round,pad=0.15", fc="white", alpha=0.75))

    figure, _ = colour.plotting.render(show=False, x_tighten=True, y_tighten=True)
    st.pyplot(figure, clear_figure=True)

st.markdown("---")
st.caption("Dải màu tính từ CMF CIE 1931 2° | Bước sóng 400–700 nm | Không gian sRGB")
