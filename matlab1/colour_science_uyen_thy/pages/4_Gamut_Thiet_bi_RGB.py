import streamlit as st
from page_style import apply_page_style
import matplotlib.pyplot as plt
import colour
import numpy as np

apply_page_style()

st.markdown("## 🖥️ Gamut màu của thiết bị RGB")
st.markdown("""
Biểu đồ này thể hiện **gamut màu sRGB** — vùng màu mà màn hình máy tính tiêu chuẩn
có thể tái tạo — trên nền biểu đồ CIE 1931 Chromaticity Diagram.
""")
st.markdown("---")

# ── Tuỳ chọn màu sắc primary ─────────────────────────────────────────────────
st.sidebar.markdown("### Tuỳ chọn hiển thị")
show_labels = st.sidebar.checkbox("Hiển thị nhãn R, G, B", value=True)
show_wp     = st.sidebar.checkbox("Hiển thị White Point D65", value=True)
line_color  = st.sidebar.color_picker("Màu đường gamut", "#000000")
line_width  = st.sidebar.slider("Độ dày đường", 1.0, 4.0, 2.0, 0.5)

# ── Tính toán tọa độ chromaticity của R, G, B ─────────────────────────────────
primaries = {
    "R": np.array([1.0, 0.0, 0.0]),
    "G": np.array([0.0, 1.0, 0.0]),
    "B": np.array([0.0, 0.0, 1.0]),
}

xy_coords = {}
for name, rgb in primaries.items():
    XYZ = colour.sRGB_to_XYZ(rgb)
    xy_coords[name] = colour.XYZ_to_xy(XYZ)

# ── Vẽ biểu đồ ────────────────────────────────────────────────────────────────
figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
axes.set_xlim([-0.1, 0.85])
axes.set_ylim([-0.1, 0.90])
axes.set_title("CIE 1931 Chromaticity Diagram\nGamut Thiết bị RGB (sRGB)", fontsize=13)

# Vẽ tam giác gamut
tri_x = [xy_coords["R"][0], xy_coords["G"][0], xy_coords["B"][0], xy_coords["R"][0]]
tri_y = [xy_coords["R"][1], xy_coords["G"][1], xy_coords["B"][1], xy_coords["R"][1]]
axes.plot(tri_x, tri_y, color=line_color, linewidth=line_width, label="sRGB Gamut")

# Tô màu vùng gamut (alpha nhẹ)
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
triangle = Polygon(list(zip(tri_x[:-1], tri_y[:-1])), closed=True,
                   facecolor="white", edgecolor=line_color,
                   alpha=0.15, linewidth=line_width)
axes.add_patch(triangle)

# Nhãn R, G, B
if show_labels:
    offsets = {"R": (0.02, -0.03), "G": (0.01, 0.02), "B": (-0.05, -0.03)}
    dot_colors = {"R": "#FF0000", "G": "#00CC00", "B": "#0000FF"}
    for name, xy in xy_coords.items():
        axes.plot(xy[0], xy[1], "o", color=dot_colors[name], markersize=9,
                  markeredgecolor="white", markeredgewidth=1.2, zorder=5)
        ox, oy = offsets[name]
        axes.annotate(
            f"{name}  ({xy[0]:.3f}, {xy[1]:.3f})",
            (xy[0], xy[1]),
            xytext=(xy[0]+ox, xy[1]+oy),
            fontsize=9, color="white",
            bbox=dict(boxstyle="round,pad=0.3", fc=dot_colors[name], alpha=0.85),
        )

# White Point D65
if show_wp:
    axes.plot(0.3127, 0.3290, "w+", markersize=14,
              markeredgecolor="black", markeredgewidth=1.5)
    axes.annotate("D65", (0.3127, 0.3290), textcoords="offset points",
                  xytext=(8, 6), fontsize=9, color="black",
                  bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))

axes.legend(loc="upper right", fontsize=9)
figure, axes = colour.plotting.render(show=False, x_tighten=True, y_tighten=True)
st.pyplot(figure, clear_figure=True)

# ── Bảng tọa độ ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Tọa độ chromaticity của các primary")

rows = []
for name, rgb in primaries.items():
    XYZ = colour.sRGB_to_XYZ(rgb) * 100
    xy = xy_coords[name]
    rows.append({
        "Primary": name,
        "sRGB": str(list(map(int, rgb * 255))),
        "X": f"{XYZ[0]:.4f}",
        "Y": f"{XYZ[1]:.4f}",
        "Z": f"{XYZ[2]:.4f}",
        "x": f"{xy[0]:.4f}",
        "y": f"{xy[1]:.4f}",
    })
import pandas as pd
st.dataframe(pd.DataFrame(rows), use_container_width=True)

st.markdown("---")
st.caption("sRGB Primaries | CIE 1931 2° Standard Observer | Illuminant D65")
