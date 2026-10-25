import streamlit as st


def apply_page_style():
    """Apply the shared visual language to functional pages."""
    st.markdown(
        """
        <style>
        .stApp {
            --page-text: #263238;
            --page-muted: #5f6b76;
            --page-surface: #f5f7f9;
            --page-border: #d5dbe1;
            --page-accent: var(--primary-color, #4f6f8f);
        }

        @media (prefers-color-scheme: dark) {
            .stApp {
                --page-text: #e2e8f0;
                --page-muted: #aab7c6;
                --page-surface: #202a38;
                --page-border: #3a4858;
            }
        }

        [data-theme="dark"] .stApp,
        [data-theme="dark"] {
            --page-text: #e2e8f0;
            --page-muted: #aab7c6;
            --page-surface: #202a38;
            --page-border: #3a4858;
        }

        [data-theme="light"] .stApp,
        [data-theme="light"] {
            --page-text: #263238;
            --page-muted: #5f6b76;
            --page-surface: #f5f7f9;
            --page-border: #d5dbe1;
        }

        .main h1, .main h2, .main h3, .main h4, .main h5 {
            color: var(--page-text);
            letter-spacing: -.015em;
            font-weight: 650;
        }

        .main h2 {
            margin-bottom: .45rem;
            font-size: clamp(1.45rem, 2.2vw, 1.9rem);
        }

        .main h3 {
            margin-top: 1.25rem;
            font-size: 1.15rem;
        }

        .main p, .main li, .main label {
            color: var(--page-text);
        }

        .main p {
            line-height: 1.6;
        }

        [data-testid="stCaptionContainer"] {
            color: var(--page-muted);
        }

        [data-testid="stFileUploader"] section,
        [data-testid="stDataFrame"],
        [data-testid="stExpander"],
        [data-testid="stAlert"] {
            border-color: var(--page-border);
            border-radius: 9px;
        }

        [data-testid="stFileUploader"] section {
            background: var(--page-surface);
        }

        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span {
            color: var(--page-muted);
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] button {
            min-height: 2.5rem;
            padding: .45rem 1rem;
            border-radius: 7px;
            border: 1px solid var(--page-accent);
            font-size: .9rem;
            font-weight: 650;
            transition: filter 140ms ease, transform 140ms ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            filter: brightness(.92);
            transform: translateY(-1px);
        }

        .stTextInput input,
        .stNumberInput input,
        .stSelectbox [data-baseweb="select"],
        .stSlider [data-baseweb="slider"] {
            border-color: var(--page-border);
        }

        .stTextInput input,
        .stNumberInput input {
            color: var(--page-text);
            background: var(--page-surface);
            border-radius: 7px;
        }

        [data-testid="stMetric"] {
            padding: .7rem .8rem;
            border: 1px solid var(--page-border);
            border-radius: 9px;
            background: var(--page-surface);
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: var(--page-text);
        }

        hr {
            border-color: var(--page-border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
