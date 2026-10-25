import colorsys
import re

import matplotlib.colors as mcolors
import numpy as np
import streamlit as st


def clamp(value, lower=0.0, upper=1.0):
    return max(lower, min(upper, float(value)))


def parse_component(value, percent=False):
    value = value.strip()
    if value.endswith("%"):
        return clamp(float(value[:-1]) / 100)
    result = float(value)
    return clamp(result / 100 if percent and result > 1 else result)


def rgb_to_values(rgb):
    red, green, blue = [clamp(channel / 255) for channel in rgb]
    hue, saturation, lightness = colorsys.rgb_to_hls(red, green, blue)
    maximum, minimum = max(red, green, blue), min(red, green, blue)
    return {
        "rgb": tuple(int(round(channel)) for channel in rgb),
        "hex": "#{:02X}{:02X}{:02X}".format(*[int(round(channel)) for channel in rgb]),
        "hue": (hue * 360) % 360,
        "saturation": saturation,
        "lightness": lightness,
        "whiteness": minimum,
        "blackness": 1 - maximum,
        "cyan": 0 if maximum == 0 else (1 - red - (1 - maximum)) / maximum,
        "magenta": 0 if maximum == 0 else (1 - green - (1 - maximum)) / maximum,
        "yellow": 0 if maximum == 0 else (1 - blue - (1 - maximum)) / maximum,
        "black": 1 - maximum,
    }


def hsl_to_rgb(hue, saturation, lightness):
    red, green, blue = colorsys.hls_to_rgb(
        (hue % 360) / 360,
        clamp(lightness),
        clamp(saturation),
    )
    return tuple(channel * 255 for channel in (red, green, blue))


def hwb_to_rgb(hue, whiteness, blackness):
    whiteness, blackness = clamp(whiteness), clamp(blackness)
    if whiteness + blackness > 1:
        total = whiteness + blackness
        whiteness, blackness = whiteness / total, blackness / total
    base = np.array(hsl_to_rgb(hue, 1, 0.5)) / 255
    return tuple((base * (1 - whiteness - blackness) + whiteness) * 255)


def cmyk_to_rgb(cyan, magenta, yellow, black):
    return tuple(
        255 * (1 - min(1, channel * (1 - black) + black))
        for channel in (cyan, magenta, yellow)
    )


def parse_ncol(value):
    match = re.fullmatch(r"([RYGCBMW])\s*(\d{0,3}(?:\.\d+)?)", value.upper())
    if not match:
        raise ValueError("NCol phải có dạng R30, Y50, B20 hoặc W50.")
    letter, amount = match.groups()
    amount = clamp(float(amount or 0) / 100)
    if letter == "W":
        return hwb_to_rgb(0, 1 - amount, amount)
    hue = {"R": 0, "Y": 60, "G": 120, "C": 180, "B": 240, "M": 300}[letter]
    return hwb_to_rgb(hue + amount * 60, 0, 0)


def parse_color(value):
    value = value.strip()
    lowered = value.lower()
    if lowered in mcolors.CSS4_COLORS:
        value = mcolors.CSS4_COLORS[lowered]
    if re.fullmatch(r"#?[0-9a-fA-F]{3,6}", value):
        return tuple(channel * 255 for channel in mcolors.to_rgb(value))

    match = re.fullmatch(r"rgba?\(([^)]+)\)", lowered)
    if match:
        parts = [part.strip() for part in match.group(1).split(",")]
        if len(parts) not in (3, 4):
            raise ValueError("RGB phải có 3 thành phần.")
        return tuple(
            clamp(float(part[:-1]) / 100) * 255
            if part.endswith("%")
            else clamp(float(part), 0, 255)
            for part in parts[:3]
        )

    match = re.fullmatch(r"hsla?\(([^)]+)\)", lowered)
    if match:
        parts = [part.strip() for part in match.group(1).split(",")]
        if len(parts) not in (3, 4):
            raise ValueError("HSL phải có dạng hsl(h, s%, l%).")
        return hsl_to_rgb(
            float(parts[0].replace("deg", "")),
            parse_component(parts[1], percent=True),
            parse_component(parts[2], percent=True),
        )

    match = re.fullmatch(r"hwb\(([^)]+)\)", lowered)
    if match:
        parts = [part.strip() for part in match.group(1).split(",")]
        if len(parts) != 3:
            raise ValueError("HWB phải có dạng hwb(h, w%, b%).")
        return hwb_to_rgb(
            float(parts[0].replace("deg", "")),
            parse_component(parts[1], percent=True),
            parse_component(parts[2], percent=True),
        )

    match = re.fullmatch(r"cmyk\(([^)]+)\)", lowered)
    if match:
        parts = [part.strip() for part in match.group(1).split(",")]
        if len(parts) != 4:
            raise ValueError("CMYK phải có 4 thành phần.")
        return cmyk_to_rgb(*(parse_component(part, percent=True) for part in parts))

    if re.fullmatch(r"[RYGCBMW]\s*\d{0,3}(?:\.\d+)?", value.upper()):
        return parse_ncol(value)
    raise ValueError("Không nhận diện được màu. Hãy dùng HEX, tên màu, RGB, HSL, HWB, CMYK hoặc NCol.")


def ncol_from_hue(hue):
    hue %= 360
    letters = ("R", "Y", "G", "C", "B", "M")
    index = int(hue // 60)
    return f"{letters[index]}{(hue % 60) / 0.6:.0f}"


def color_name(rgb):
    hex_value = rgb_to_values(rgb)["hex"].lower()
    names = [
        name for name, value in mcolors.CSS4_COLORS.items()
        if value.lower() == hex_value
    ]
    return names[0] if names else "no name"


def show_preview(rgb, label):
    values = rgb_to_values(rgb)
    st.markdown(
        f"""
        <div style='height:90px;border-radius:10px;background:{values["hex"]};
                    border:1px solid rgba(255,255,255,.35);margin:8px 0 4px'></div>
        <p style='margin:0;color:var(--converter-text);font-size:13px;opacity:.78'>
            {label}: <b>{values["hex"]}</b>
        </p>
        """,
        unsafe_allow_html=True,
    )


st.markdown("""
<style>
/* Theme-aware palette: use Streamlit's light/dark theme variables. */
.stApp {
    --converter-accent: var(--primary-color, #4f6f8f);
    --converter-text: var(--text-color, #263238);
    --converter-surface: var(--secondary-background-color, #f3f5f7);
    --converter-border: var(--border-color, #d5dbe1);
    --converter-muted: #5f6b76;
}
@media (prefers-color-scheme: dark) {
    .stApp {
        --converter-text: #e2e8f0;
        --converter-surface: #202a38;
        --converter-border: #3a4858;
        --converter-muted: #aab7c6;
    }
}
[data-theme="dark"] .stApp,
[data-theme="dark"] {
    --converter-text: #e2e8f0;
    --converter-surface: #202a38;
    --converter-border: #3a4858;
    --converter-muted: #aab7c6;
}
[data-theme="light"] .stApp,
[data-theme="light"] {
    --converter-text: #263238;
    --converter-surface: #f5f7f9;
    --converter-border: #d5dbe1;
    --converter-muted: #5f6b76;
}
.converter-hero {
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    background: var(--converter-surface);
    border: 1px solid var(--converter-border);
    margin-bottom: 1rem;
}
.converter-hero h1 {
    margin: 0;
    color: var(--converter-text);
    font-size: clamp(1.55rem, 2.4vw, 2rem);
    font-weight: 650;
    letter-spacing: -.02em;
}
.converter-hero p {
    margin: .4rem 0 0;
    color: var(--converter-muted);
    font-size: .95rem;
}
.color-input-label {
    color: var(--converter-text);
    font-size: 1rem;
    font-weight: 600;
    font-style: italic;
    margin-bottom: .35rem;
}
.color-preview {
    min-height: 260px;
    border-radius: 10px;
    border: 1px solid var(--converter-border);
    box-shadow: 0 3px 12px rgba(0,0,0,.08);
}
.color-row {
    display: grid;
    grid-template-columns: 76px 1fr;
    align-items: center;
    min-height: 40px;
    border-bottom: 1px solid var(--converter-border);
    background: var(--converter-surface);
}
.color-row:first-child {
    border-top: 1px solid var(--converter-border);
    border-radius: 8px 8px 0 0;
}
.color-row:last-child {
    border-radius: 0 0 8px 8px;
}
.color-row-label {
    padding: .42rem .65rem;
    color: var(--converter-text);
    font-size: .9rem;
    font-weight: 600;
    font-style: italic;
    text-decoration: underline;
}
.color-row-value {
    padding: .42rem .75rem;
    color: var(--converter-text);
    font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
    font-size: .9rem;
    overflow-wrap: anywhere;
}
.hint-box {
    padding: .8rem 1rem;
    border-radius: 8px;
    background: var(--converter-surface);
    border: 1px solid var(--converter-border);
    color: var(--converter-muted);
    font-size: .84rem;
    line-height: 1.55;
}
.stTextInput input {
    min-height: 2.65rem;
    border-radius: 7px;
    border-color: var(--converter-border);
    background: var(--converter-surface);
    color: var(--converter-text);
    font-size: .95rem;
}
.stTextInput input::placeholder {
    color: var(--converter-muted);
    opacity: .85;
}
.stTextInput input:focus {
    border-color: var(--converter-accent);
    box-shadow: 0 0 0 .12rem color-mix(in srgb, var(--converter-accent) 20%, transparent);
}
div.stFormSubmitButton > button,
div[data-testid="stFormSubmitButton"] button {
    min-height: 2.65rem;
    border-radius: 7px;
    border: 1px solid var(--converter-accent);
    background: var(--converter-accent);
    color: #ffffff;
    font-size: .9rem;
    font-weight: 650;
    letter-spacing: .01em;
    transition: filter 140ms ease, transform 140ms ease;
}
div.stFormSubmitButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    filter: brightness(.92);
    transform: translateY(-1px);
}
[data-testid="stExpander"] {
    border-color: var(--converter-border);
    border-radius: 8px;
}
[data-testid="stMetric"] label,
[data-testid="stCaptionContainer"] {
    color: var(--converter-muted);
}
h3, h4, h5 {
    color: var(--converter-text);
    letter-spacing: -.01em;
}
</style>
<div class="converter-hero">
    <h1>🔄 Chuyển đổi màu sắc</h1>
    <p>Phân tích và chuyển đổi màu giữa HEX, RGB, HSL, HWB, CMYK, NCol và XYZ.</p>
</div>
""", unsafe_allow_html=True)

input_col, preview_col = st.columns([1.05, .95], gap="large")
with input_col:
    st.markdown("<div class='color-input-label'>Nhập một màu:</div>",
                unsafe_allow_html=True)
    with st.form("color_converter_form"):
        color_input = st.text_input(
            "name, hex, rgb, hsl, hwb, cmyk, ncol",
            value="hsl(205, 100%, 70%)",
            label_visibility="collapsed",
            placeholder="Ví dụ: #ff0000 hoặc hsl(205, 100%, 70%)",
        )
        submitted = st.form_submit_button("Phân tích màu", type="primary",
                                          use_container_width=True)
    st.markdown(
        "<div class='hint-box'><b>Định dạng hỗ trợ</b><br>"
        "Tên màu · HEX · RGB · HSL · HWB · CMYK · NCol</div>",
        unsafe_allow_html=True,
    )

if submitted or "parsed_color" not in st.session_state:
    try:
        st.session_state.parsed_color = parse_color(color_input)
        st.session_state.color_error = None
    except (TypeError, ValueError) as error:
        st.session_state.color_error = str(error)

if st.session_state.get("color_error"):
    st.error(st.session_state.color_error)
else:
    rgb = st.session_state.parsed_color
    values = rgb_to_values(rgb)

    with preview_col:
        st.markdown(
            f"<div class='color-preview' style='background:{values['hex']}'></div>",
            unsafe_allow_html=True,
        )

    with input_col:
        st.markdown("#### Kết quả chuyển đổi")
        hsl_text = (
            f"hsl({values['hue']:.0f}, {values['saturation'] * 100:.0f}%, "
            f"{values['lightness'] * 100:.0f}%)"
        )
        hwb_text = (
            f"hwb({values['hue']:.0f}, {values['whiteness'] * 100:.0f}%, "
            f"{values['blackness'] * 100:.0f}%)"
        )
        cmyk_text = "cmyk(" + ", ".join(
            f"{values[key] * 100:.0f}%" for key in
            ("cyan", "magenta", "yellow", "black")
        ) + ")"
        ncol_text = (
            f"{ncol_from_hue(values['hue'])}, "
            f"{values['whiteness'] * 100:.0f}%, {values['blackness'] * 100:.0f}%"
        )
        output_rows = [
            ("Name", color_name(rgb)),
            ("Rgb", "rgb({}, {}, {})".format(*values["rgb"])),
            ("Hex", values["hex"].lower()),
            ("Hsl", hsl_text),
            ("Hwb", hwb_text),
            ("Cmyk", cmyk_text),
            ("Ncol", ncol_text),
        ]
        st.markdown(
            "".join(
                f"<div class='color-row'><div class='color-row-label'>{label}</div>"
                f"<div class='color-row-value'>{value}</div></div>"
                for label, value in output_rows
            ),
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption(
    "Hỗ trợ HEX, tên màu CSS, RGB, HSL, HWB, CMYK và NCol · "
    "Phân tích màu theo các biểu diễn chuẩn"
)
