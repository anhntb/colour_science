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
