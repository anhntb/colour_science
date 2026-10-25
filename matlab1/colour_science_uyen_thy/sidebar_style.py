import streamlit as st


def apply_sidebar_style():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1730 0%, #111d3b 55%, #16264b 100%);
        border-right: 1px solid rgba(126, 200, 255, 0.14);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.25rem 0.85rem 1.5rem;
    }

    [data-testid="stSidebarNav"] {
        padding-top: 0.5rem;
    }

    [data-testid="stSidebarNav"]::before {
        content: "ĐIỀU HƯỚNG ỨNG DỤNG";
        display: block;
        margin: 1rem 0 0.55rem 0.7rem;
        color: #7ec8ff;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
    }

    [data-testid="stSidebarNav"] ul {
        gap: 0.35rem;
    }

    [data-testid="stSidebarNav"] li {
        margin: 0;
    }

    [data-testid="stSidebarNav"] a {
        border: 1px solid transparent;
        border-radius: 10px;
        color: #c9d8f3;
        padding: 0.62rem 0.7rem;
        transition: background-color 160ms ease, border-color 160ms ease,
                    color 160ms ease, transform 160ms ease;
    }

    [data-testid="stSidebarNav"] a span {
        color: inherit;
        font-size: 0.88rem;
        font-weight: 500;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(74, 158, 255, 0.14);
        border-color: rgba(126, 200, 255, 0.28);
        color: #ffffff;
        transform: translateX(3px);
    }

    [data-testid="stSidebarNav"] li[aria-current="page"] > a {
        background: linear-gradient(90deg, #246bc0, #3189d7);
        border-color: rgba(190, 230, 255, 0.42);
        box-shadow: 0 5px 16px rgba(19, 93, 173, 0.28);
        color: #ffffff;
        font-weight: 700;
    }

    [data-testid="stSidebarNav"] li[aria-current="page"] > a::before {
        content: "";
        width: 3px;
        height: 1.2rem;
        margin-right: 0.5rem;
        border-radius: 4px;
        background: #dff4ff;
    }

    /* Controls rendered by individual pages below the navigation. */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h5,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h6,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] label {
        color: #dce8f7 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] b {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(190, 220, 245, 0.52);
        color: #f2f7ff !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        color: #f2f7ff !important;
        caret-color: #ffffff;
    }

    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #c2d2e4 !important;
        opacity: 1;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        color: #f2f7ff !important;
        fill: #f2f7ff;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] label,
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label span,
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
        color: #dce8f7 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
        background: #9bc9f2;
        border-color: #e7f4ff;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background: #5f9ed0;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] svg {
        fill: #b9d9f3;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        color: #dce8f7 !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] section,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.09) !important;
        border: 1px dashed rgba(190, 220, 245, 0.55) !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] *,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] *,
    [data-testid="stSidebar"] [data-testid="stFileUploaderFile"] * {
        color: #dce8f7 !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
        background: #315f8f !important;
        border: 1px solid #80b5df !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover {
        background: #3d73a7 !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(190, 220, 245, 0.42) !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
        color: #aac4e8;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style='padding:0.35rem 0.35rem 0.85rem; border-bottom:1px solid rgba(126,200,255,0.16);'>
        <div style='display:flex; align-items:center; gap:0.65rem;'>
            <div style='display:flex; align-items:center; justify-content:center;
                        width:38px; height:38px; border-radius:11px;
                        background:linear-gradient(135deg,#4a9eff,#7ec8ff);
                        color:#0d1730; font-size:21px; box-shadow:0 5px 14px rgba(74,158,255,.3);'>
                🎨
            </div>
            <div>
                <div style='color:#ffffff; font-weight:700; font-size:1rem; line-height:1.2;'>
                    Khoa học Màu sắc
                </div>
                <div style='color:#aac4e8; font-size:0.72rem; margin-top:3px;'>
                    HCMUTE • Interactive Lab
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
