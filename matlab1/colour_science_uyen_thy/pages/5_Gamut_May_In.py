import streamlit as st
import matplotlib.pyplot as plt
import colour
import numpy as np
import pandas as pd

st.markdown("## 🖨️ Gamut màu của máy in")
st.markdown("""
Upload file CSV chứa dữ liệu đo màu của máy in (định dạng CIELab).  
Chương trình sẽ chuyển **Lab → XYZ → xy** và vẽ gamut lên biểu đồ CIE 1931.
""")
st.markdown("---")

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("### Tuỳ chọn")
csv_file = st.sidebar.file_uploader("📂 Upload file gamut CSV", type=["csv"])
show_labels = st.sidebar.checkbox("Hiển thị nhãn điểm màu", value=True)
gamut_color = st.sidebar.color_picker("Màu đường gamut", "#000000")

st.sidebar.markdown("---")
st.sidebar.markdown("**Định dạng file CSV:**")
st.sidebar.markdown("""
```
ColorSpace,L,a,b
R,47.22,58.61,36.98
Y,87.37,-9.17,93.68
G,46.53,-64.69,49.40
C,57.84,-49.31,-20.89
B,24.68,24.25,-53.70
M,52.15,74.27,-35.50
```
""")

def process_gamut(df):
    """Chuyển Lab → XYZ → xy cho từng màu."""
    results = {}
    # Cột: ColorSpace, L, a, b  (hoặc index là ColorSpace)
    if "ColorSpace" in df.columns:
        df = df.set_index("ColorSpace")

    for color_name in df.index:
        L = float(df.loc[color_name, "L"])
        a = float(df.loc[color_name, "a"])
        b = float(df.loc[color_name, "b"])
        Lab = np.array([L, a, b])
        XYZ = colour.Lab_to_XYZ(Lab)
        xy  = colour.XYZ_to_xy(XYZ)
        results[color_name] = {"Lab": Lab, "XYZ": XYZ, "xy": xy}
    return results

# ── Màu đặt tên cho từng primary ──────────────────────────────────────────────
POINT_COLORS = {
    "R": "#FF3333", "Y": "#FFEE00", "G": "#00BB00",
    "C": "#00CCCC", "B": "#3333FF", "M": "#CC00CC",
}

def get_point_color(name):
    name_up = name.strip().upper()
    return POINT_COLORS.get(name_up, "#333333")

# ── Thứ tự nối gamut CMYK ─────────────────────────────────────────────────────
GAMUT_ORDER = ["R", "Y", "G", "C", "B", "M"]

if csv_file is not None:
    df_raw = pd.read_csv(csv_file)
    if "ColorSpace" in df_raw.columns:
        df_display = df_raw.set_index("ColorSpace")
    else:
        df_display = df_raw

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📄 Dữ liệu input")
        st.dataframe(df_display, use_container_width=True)

    with col2:
        results = process_gamut(df_raw.copy())

        # Sắp xếp điểm theo thứ tự gamut
        ordered_keys = [k for k in GAMUT_ORDER if k in results]
        # Thêm các key không nằm trong GAMUT_ORDER vào cuối
        for k in results:
            if k not in ordered_keys:
                ordered_keys.append(k)

        px = [results[k]["xy"][0] for k in ordered_keys]
        py = [results[k]["xy"][1] for k in ordered_keys]
        # Đóng vòng
        px.append(px[0])
        py.append(py[0])

        # Vẽ
        figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
        axes.set_xlim([-0.1, 0.85])
        axes.set_ylim([-0.1, 0.90])
        axes.set_title("CIE 1931 – Gamut Máy In\n(từ dữ liệu CIELab đo thực tế)", fontsize=12)

        axes.plot(px, py, color=gamut_color, linewidth=2, label="Gamut máy in")

        if show_labels:
            for k in ordered_keys:
                xy = results[k]["xy"]
                c  = get_point_color(k)
                axes.plot(xy[0], xy[1], "o", color=c, markersize=9,
                          markeredgecolor="white", markeredgewidth=1.2, zorder=5)
                axes.annotate(k, (xy[0], xy[1]),
                              textcoords="offset points", xytext=(6, 4),
                              fontsize=9, color="white",
                              bbox=dict(boxstyle="round,pad=0.25", fc=c, alpha=0.9))

        axes.legend(loc="upper right", fontsize=9)
        figure, _ = colour.plotting.render(show=False, x_tighten=True, y_tighten=True)
        st.pyplot(figure, clear_figure=True)

    # ── Bảng kết quả ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Bảng tọa độ xy của các màu primary")
    table_rows = []
    for k, v in results.items():
        table_rows.append({
            "Màu": k,
            "L*": f"{v['Lab'][0]:.2f}",
            "a*": f"{v['Lab'][1]:.2f}",
            "b*": f"{v['Lab'][2]:.2f}",
            "X":  f"{v['XYZ'][0]:.4f}",
            "Y":  f"{v['XYZ'][1]:.4f}",
            "Z":  f"{v['XYZ'][2]:.4f}",
            "x":  f"{v['xy'][0]:.4f}",
            "y":  f"{v['xy'][1]:.4f}",
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

else:
    st.info("👈 Vui lòng upload file gamut CSV ở sidebar bên trái để bắt đầu.")

    # Vẽ biểu đồ trống mặc định
    figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    axes.set_xlim([-0.1, 0.85])
    axes.set_ylim([-0.1, 0.90])
    axes.set_title("CIE 1931 Chromaticity Diagram\n(Upload file để vẽ gamut máy in)", fontsize=12)
    figure, _ = colour.plotting.render(show=False, x_tighten=True, y_tighten=True)
    st.pyplot(figure, clear_figure=True)

st.markdown("---")
st.caption("CIE 1931 2° Standard Observer | Lab → XYZ → xy | Illuminant D50 (colour-science default for Lab)")
