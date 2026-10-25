import streamlit as st
from page_style import apply_page_style
import matplotlib.pyplot as plt
import colour
import numpy as np

apply_page_style()

st.markdown("## 👁️ Biểu đồ CIE 1931 Chromaticity Diagram")
st.markdown("""
Biểu đồ chromaticity **CIE 1931** hình móng ngựa biểu diễn toàn bộ không gian màu
mà mắt người có thể nhìn thấy được, dựa trên hàm so màu 2° Standard Observer.
""")
st.markdown("---")

# ── Tuỳ chọn ──────────────────────────────────────────────────────────────────
show_wp = st.sidebar.checkbox("Hiển thị White Point D65", value=True)
show_srgb = st.sidebar.checkbox("Hiển thị gamut sRGB", value=False)
xlim_min = st.sidebar.slider("x min", -0.2, 0.0, -0.1, 0.05)
xlim_max = st.sidebar.slider("x max", 0.6,  0.9, 0.85, 0.05)
ylim_min = st.sidebar.slider("y min", -0.2, 0.0, -0.1, 0.05)
ylim_max = st.sidebar.slider("y max", 0.7,  1.0, 0.90, 0.05)

# ── Vẽ biểu đồ ────────────────────────────────────────────────────────────────
figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
axes.set_xlim([xlim_min, xlim_max])
axes.set_ylim([ylim_min, ylim_max])
axes.set_title("CIE 1931 Chromaticity Diagram\n2 Degree Standard Observer", fontsize=13)

# White Point D65
if show_wp:
    # D65 white point xy ≈ (0.3127, 0.3290)
    axes.plot(0.3127, 0.3290, "w+", markersize=14, markeredgecolor="black", markeredgewidth=1.5)
    axes.annotate("D65", (0.3127, 0.3290), textcoords="offset points",
                  xytext=(8, 6), fontsize=9, color="black",
                  bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))

# Gamut sRGB
if show_srgb:
    R = colour.XYZ_to_xy(colour.sRGB_to_XYZ(np.array([1.0, 0.0, 0.0])))
    G = colour.XYZ_to_xy(colour.sRGB_to_XYZ(np.array([0.0, 1.0, 0.0])))
    B = colour.XYZ_to_xy(colour.sRGB_to_XYZ(np.array([0.0, 0.0, 1.0])))
    tri_x = [R[0], G[0], B[0], R[0]]
    tri_y = [R[1], G[1], B[1], R[1]]
    axes.plot(tri_x, tri_y, "k--", linewidth=1.5, label="sRGB gamut")
    axes.legend(fontsize=9)

figure, axes = colour.plotting.render(show=False, x_tighten=True, y_tighten=True)
st.pyplot(figure, clear_figure=True)

st.markdown("---")
st.markdown("""
**Ghi chú:**
- Đường cong móng ngựa bao gồm toàn bộ màu sắc có thể nhìn thấy (visible spectrum locus)
- Điểm trắng **D65** ≈ (0.3127, 0.3290) là ánh sáng ban ngày tiêu chuẩn
- Tam giác sRGB (tuỳ chọn) là gamut của màn hình máy tính thông thường
""")
st.caption("Sử dụng colour-science | CIE 1931 2° Standard Observer")
