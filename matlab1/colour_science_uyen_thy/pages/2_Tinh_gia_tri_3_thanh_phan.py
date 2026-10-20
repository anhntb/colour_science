import streamlit as st
import colour
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tính giá trị 3 thành phần", page_icon="📊", layout="wide")

st.markdown("## 📊 Tính giá trị 3 thành phần X, Y, Z")
st.markdown("""
Upload file phổ đo dạng CSV (2 cột: **bước sóng** và **phổ phản xạ**).  
Chương trình sẽ tính **X, Y, Z** dựa trên CIE 1931 2° Standard Observer và illuminant **D65**.
""")
st.markdown("---")

# ── Upload file ────────────────────────────────────────────────────────────────
csv_file = st.sidebar.file_uploader("📂 Upload file phổ CSV", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Định dạng file CSV:**")
st.sidebar.markdown("""
```
400, 0.0500
410, 0.0512
...
700, 0.4800
```
- Cột 1: Bước sóng (nm)
- Cột 2: Phổ phản xạ (0–1)
- Không có header
""")

if csv_file is not None:
    df = pd.read_csv(csv_file, header=None)
    df.columns = ["Bước sóng (nm)", "Phổ phản xạ"]
    df["Bước sóng (nm)"] = df["Bước sóng (nm)"].astype(int)

    n = len(df)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📄 Dữ liệu file phổ")
        # Hiển thị 5 đầu + 5 cuối
        preview = pd.concat([df.head(5), pd.DataFrame([{"Bước sóng (nm)": "...", "Phổ phản xạ": "..."}]), df.tail(5)])
        st.dataframe(preview, use_container_width=True)
        st.caption(f"Tổng số bước sóng: **{n}** | Từ **{df['Bước sóng (nm)'].iloc[0]} nm** đến **{df['Bước sóng (nm)'].iloc[-1]} nm**")

    with col2:
        st.markdown("### 📈 Biểu đồ phổ phản xạ")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(df["Bước sóng (nm)"], df["Phổ phản xạ"], color="#0055A4", linewidth=2)
        ax.set_xlabel("Bước sóng (nm)")
        ax.set_ylabel("Phổ phản xạ")
        ax.set_title("Spectral Reflectance")
        ax.set_xlim([df["Bước sóng (nm)"].min(), df["Bước sóng (nm)"].max()])
        ax.set_ylim([0, max(df["Phổ phản xạ"].max() * 1.1, 0.1)])
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig, clear_figure=True)

    st.markdown("---")

    if st.button("🔢 Tính X, Y, Z", use_container_width=True):
        # Tạo spectral distribution
        dict_data = {}
        for _, row in df.iterrows():
            dict_data[int(row["Bước sóng (nm)"])] = float(row["Phổ phản xạ"])

        sd = colour.SpectralDistribution(dict_data)
        cmfs = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
        illuminant = colour.SDS_ILLUMINANTS["D65"]

        XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
        X, Y, Z = XYZ[0], XYZ[1], XYZ[2]

        st.markdown("### ✅ Kết quả")
        m1, m2, m3 = st.columns(3)
        m1.metric("X", f"{X:.4f}")
        m2.metric("Y", f"{Y:.4f}")
        m3.metric("Z", f"{Z:.4f}")

        # Chuyển thêm sang xy chromaticity và Lab
        xy = colour.XYZ_to_xy(XYZ / 100)
        RGB_preview = colour.XYZ_to_sRGB(XYZ / 100)
        RGB_preview = np.clip(RGB_preview, 0, 1)
        hex_c = "#{:02X}{:02X}{:02X}".format(
            int(RGB_preview[0]*255), int(RGB_preview[1]*255), int(RGB_preview[2]*255)
        )

        col_r, col_info = st.columns([1, 3])
        with col_r:
            st.markdown(f"""
            <div style='width:100px;height:100px;background:{hex_c};
                        border-radius:10px;border:2px solid #ccc;margin:10px 0'></div>
            <p style='font-size:13px;color:#555'>Màu xấp xỉ: <b>{hex_c}</b></p>
            """, unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
| Đại lượng | Giá trị |
|-----------|---------|
| **X** | {X:.4f} |
| **Y** | {Y:.4f} |
| **Z** | {Z:.4f} |
| **x** (chromaticity) | {xy[0]:.4f} |
| **y** (chromaticity) | {xy[1]:.4f} |
            """)

        st.info("""
**Phương pháp tính:**  
Sử dụng tích phân số:  
X = k·∫ S(λ)·x̄(λ)·dλ, Y = k·∫ S(λ)·ȳ(λ)·dλ, Z = k·∫ S(λ)·z̄(λ)·dλ  
với k được chuẩn hoá theo illuminant D65 và hàm so màu CIE 1931 2°.
        """)
else:
    st.info("👈 Vui lòng upload file CSV phổ màu ở sidebar bên trái.")
    st.markdown("#### Ví dụ dữ liệu mẫu (Color_Cyan_Sample.csv)")
    sample = pd.DataFrame({
        "Bước sóng (nm)": [400, 410, 420, "...", 690, 700],
        "Phổ phản xạ":    [0.050, 0.051, 0.053, "...", 0.480, 0.490],
    })
    st.dataframe(sample, use_container_width=False)

st.markdown("---")
st.caption("Sử dụng colour-science | CIE 1931 2° Standard Observer | Illuminant D65")
