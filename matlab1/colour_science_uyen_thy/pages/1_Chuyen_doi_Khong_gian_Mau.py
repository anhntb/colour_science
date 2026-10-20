import streamlit as st
import numpy as np
import colour

st.set_page_config(page_title="Chuyển đổi Không gian Màu", page_icon="🔄", layout="wide")

st.markdown("## 🔄 Chuyển đổi Không gian Màu")
st.markdown("Chuyển đổi hai chiều giữa **sRGB ↔ XYZ** sử dụng tiêu chuẩn CIE 1931.")
st.markdown("---")

tab1, tab2 = st.tabs(["sRGB → XYZ", "XYZ → sRGB"])

# ── Tab 1: sRGB → XYZ ─────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Nhập giá trị sRGB (0 – 255)")
    c1, c2, c3 = st.columns(3)
    R = c1.number_input("R", min_value=0.0, max_value=255.0, value=255.0, step=1.0, key="R_in")
    G = c2.number_input("G", min_value=0.0, max_value=255.0, value=0.0,   step=1.0, key="G_in")
    B = c3.number_input("B", min_value=0.0, max_value=255.0, value=0.0,   step=1.0, key="B_in")

    # Preview màu
    hex_color = "#{:02X}{:02X}{:02X}".format(int(R), int(G), int(B))
    st.markdown(f"""
    <div style='width:80px;height:80px;background:{hex_color};
                border-radius:8px;border:2px solid #ccc;margin:10px 0'></div>
    <p style='color:#555;font-size:13px'>Màu preview: <b>{hex_color}</b></p>
    """, unsafe_allow_html=True)

    if st.button("Chuyển sang XYZ", key="btn_rgb2xyz"):
        r_n = R / 255.0
        g_n = G / 255.0
        b_n = B / 255.0
        RGB = np.array([r_n, g_n, b_n])
        XYZ = colour.sRGB_to_XYZ(RGB) * 100  # scale lên 0–100

        st.markdown("---")
        st.markdown("### Kết quả XYZ")
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("X", f"{XYZ[0]:.4f}")
        rc2.metric("Y", f"{XYZ[1]:.4f}")
        rc3.metric("Z", f"{XYZ[2]:.4f}")

        st.info(f"""
**Công thức sử dụng:**
- Chuẩn hoá: R' = R/255, G' = G/255, B' = B/255
- Áp dụng ma trận tuyến tính sRGB → XYZ (D65, CIE 1931 2°)
- **X = {XYZ[0]:.4f}**, **Y = {XYZ[1]:.4f}**, **Z = {XYZ[2]:.4f}**
        """)

        # Bảng so sánh
        st.markdown("#### Tóm tắt")
        data = {
            "Thành phần": ["R (sRGB)", "G (sRGB)", "B (sRGB)", "X", "Y", "Z"],
            "Giá trị gốc": [f"{R:.0f}", f"{G:.0f}", f"{B:.0f}", "—", "—", "—"],
            "Giá trị kết quả": ["—", "—", "—", f"{XYZ[0]:.4f}", f"{XYZ[1]:.4f}", f"{XYZ[2]:.4f}"],
        }
        st.table(data)

# ── Tab 2: XYZ → sRGB ─────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Nhập giá trị XYZ (thang 0 – 100)")
    c1, c2, c3 = st.columns(3)
    X = c1.number_input("X", min_value=0.0, max_value=200.0, value=41.24, step=0.01, key="X_in")
    Y = c2.number_input("Y", min_value=0.0, max_value=200.0, value=21.26, step=0.01, key="Y_in")
    Z = c3.number_input("Z", min_value=0.0, max_value=200.0, value=1.93,  step=0.01, key="Z_in")

    if st.button("Chuyển sang sRGB", key="btn_xyz2rgb"):
        XYZ_in = np.array([X / 100.0, Y / 100.0, Z / 100.0])
        RGB_out = colour.XYZ_to_sRGB(XYZ_in)
        RGB_out_clipped = np.clip(RGB_out, 0, 1)
        R_out = RGB_out_clipped[0] * 255
        G_out = RGB_out_clipped[1] * 255
        B_out = RGB_out_clipped[2] * 255

        st.markdown("---")
        st.markdown("### Kết quả sRGB")
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("R", f"{R_out:.1f}  ({int(round(R_out))})")
        rc2.metric("G", f"{G_out:.1f}  ({int(round(G_out))})")
        rc3.metric("B", f"{B_out:.1f}  ({int(round(B_out))})")

        hex_out = "#{:02X}{:02X}{:02X}".format(int(round(R_out)), int(round(G_out)), int(round(B_out)))
        st.markdown(f"""
        <div style='width:80px;height:80px;background:{hex_out};
                    border-radius:8px;border:2px solid #ccc;margin:10px 0'></div>
        <p style='color:#555;font-size:13px'>Màu preview: <b>{hex_out}</b></p>
        """, unsafe_allow_html=True)

        if any(v < 0 or v > 1 for v in RGB_out):
            st.warning("⚠️ Một số giá trị XYZ nằm ngoài gamut sRGB — đã clamp về [0, 255].")

        st.info(f"""
**Công thức sử dụng:**
- Chuẩn hoá: X' = X/100, Y' = Y/100, Z' = Z/100
- Áp dụng ma trận nghịch đảo XYZ → sRGB (D65, CIE 1931 2°)
- **R = {R_out:.1f}**, **G = {G_out:.1f}**, **B = {B_out:.1f}**
        """)

        data = {
            "Thành phần": ["X", "Y", "Z", "R (sRGB)", "G (sRGB)", "B (sRGB)"],
            "Giá trị gốc": [f"{X:.2f}", f"{Y:.2f}", f"{Z:.2f}", "—", "—", "—"],
            "Giá trị kết quả": ["—", "—", "—", f"{R_out:.1f}", f"{G_out:.1f}", f"{B_out:.1f}"],
        }
        st.table(data)

st.markdown("---")
st.caption("Sử dụng thư viện colour-science | CIE 1931 2° Standard Observer | Illuminant D65")
