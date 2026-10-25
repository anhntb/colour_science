import streamlit as st

from sidebar_style import apply_sidebar_style


st.set_page_config(
    page_title="Khoa học Màu sắc - HCMUTE",
    page_icon="🎨",
    layout="wide",
)

apply_sidebar_style()

pages = [
    st.Page(
        "Khoa_hoc_Mau_sac.py",
        title="Trang chủ",
        # icon="🏠",
    ),
    st.Page(
        "pages/1_Chuyen_doi_Khong_gian_Mau.py",
        title="Chuyển đổi không gian màu",
        # icon="🔄",
    ),
    st.Page(
        "pages/2_Tinh_gia_tri_3_thanh_phan.py",
        title="Tính giá trị XYZ",
        # icon="📊",
    ),
    st.Page(
        "pages/3_Bieu_do_CIE_1931.py",
        title="Biểu đồ CIE 1931",
        # icon="🎨",
    ),
    st.Page(
        "pages/4_Gamut_Thiet_bi_RGB.py",
        title="Gamut thiết bị RGB",
        # icon="🖥️",
    ),
    st.Page(
        "pages/5_Gamut_May_In.py",
        title="Gamut máy in",
        # icon="🖨️",
    ),
    st.Page(
        "pages/6_Dac_tinh_hoa_May_in_Nua_tong.py",
        title="Đặc tính hóa máy in nửa tông",
        # icon="📈",
    ),
    st.Page(
        "pages/7_CIE_Band_400_700nm.py",
        title="Dải CIE 400–700 nm",
        # icon="🌈",
    ),
    st.Page(
        "pages/8_Bieu_do_CIELab.py",
        title="Biểu đồ CIELab",
        # icon="📉",
    ),
    st.Page(
        "pages/9_Tinh_Delta_E.py",
        title="Tính độ khác biệt màu ΔE",
        # icon="📐",
    ),
]

page = st.navigation(pages)
page.run()
