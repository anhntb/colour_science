import streamlit as st
import os

st.set_page_config(
    page_title="Khoa học Màu sắc - HCMUTE",
    page_icon="🎨",
    layout="wide"
)

# ── Header: logo + tên trường ──────────────────────────────────────────────────
col_logo, col_info = st.columns([1, 4])

with col_logo:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_hcmute.png")
    st.image(logo_path, width=130)

with col_info:
    st.markdown("""
    <div style='padding-top:10px'>
        <h4 style='margin:0; color:#4a9eff'>TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT TP.HCM</h4>
        <p style='margin:2px 0; color:#7ec8ff; font-size:14px'>
            Ho Chi Minh City University of Technology and Engineering (HCMUTE)
        </p>
        <p style='margin:2px 0 0 0; color:#aac4e8; font-size:13px'>
            Khoa Công nghệ In &amp; Truyền thông
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Tiêu đề chính ─────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#4a9eff;'>🎨 Khoa học Màu sắc</h1>
<h4 style='text-align:center; color:#aaa;'>Colour Science Interactive Web Application</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Thông tin sinh viên ────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown("""
    <div style='background:#1e2a4a; border-left:5px solid #4a9eff;
                padding:20px 30px; border-radius:8px; text-align:center;'>
        <h3 style='margin:0 0 12px 0; color:#ffffff;'>Thông tin sinh viên</h3>
        <p style='margin:6px 0; font-size:16px; color:#e0e8ff;'>
            <b style="color:#7ec8ff;">Họ tên:</b> Nguyễn Lê Uyên Thy
        </p>
        <p style='margin:6px 0; font-size:16px; color:#e0e8ff;'>
            <b style="color:#7ec8ff;">MSSV:</b> 24158137
        </p>
        <p style='margin:6px 0; font-size:16px; color:#e0e8ff;'>
            <b style="color:#7ec8ff;">Ngành:</b> Công nghệ Kỹ thuật In
        </p>
        <p style='margin:6px 0; font-size:16px; color:#e0e8ff;'>
            <b style="color:#7ec8ff;">Trường:</b> HCMUTE – TP.HCM
        </p>
        <p style='margin:6px 0; font-size:16px; color:#e0e8ff;'>
            <b style="color:#7ec8ff;">Năm nhập học:</b> 2024
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Mô tả các chức năng ───────────────────────────────────────────────────────
st.markdown("### 📋 Nội dung ứng dụng")

features = [
    ("1️⃣", "Chuyển đổi Không gian Màu",    "Chuyển đổi hai chiều giữa sRGB ↔ XYZ"),
    ("2️⃣", "Tính Giá trị 3 Thành phần",     "Tính X, Y, Z từ file phổ đo CSV với CIE 1931 D65"),
    ("3️⃣", "Biểu đồ CIE 1931",              "Vẽ biểu đồ chromaticity diagram hình móng ngựa"),
    ("4️⃣", "Gamut Thiết bị RGB",             "Vẽ gamut màu của thiết bị RGB trên biểu đồ CIE"),
    ("5️⃣", "Gamut Máy in",                   "Vẽ gamut màu máy in từ file dữ liệu Lab"),
    ("6️⃣", "Đặc tính hoá Máy in Nửa tông",  "Phân tích phổ và đường cong tái tạo tông màu halftone"),
    ("7️⃣", "CIE Band 400–700 nm",            "Vẽ biểu đồ CIE dạng dải màu quang phổ 400–700 nm"),
    ("8️⃣", "Biểu đồ CIELab",                "Nhập Lab1/Lab2 – vẽ và nhận xét chuyển dịch màu"),
    ("9️⃣", "Tính ΔE Màu sắc",               "Tính color difference ΔE76 và ΔE2000 giữa 2 màu"),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div style='background:#1a2035; border:1px solid #2a3a6a; border-radius:8px;
                    padding:14px 16px; margin-bottom:14px; min-height:90px;'>
            <span style='font-size:22px'>{icon}</span>
            <b style='color:#7ec8ff; font-size:15px'> {title}</b>
            <p style='margin:6px 0 0 0; color:#aaa; font-size:13px'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#555; font-size:12px'>"
    "© 2024 Nguyễn Lê Uyên Thy – HCMUTE | Môn: Khoa học Màu sắc</p>",
    unsafe_allow_html=True,
)
