import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import colour

st.set_page_config(page_title="Biểu đồ CIELab", page_icon="🎯", layout="wide")

st.markdown("## 🎯 Biểu đồ CIELab – Phân tích chuyển dịch màu")
st.markdown("""
Nhập hai màu **Lab1** và **Lab2**, chương trình sẽ:
- Hiển thị 2 điểm màu trên không gian CIELab (mặt phẳng **a\*–b\*** và trục **L\***)
- Vẽ mũi tên chuyển dịch từ Lab1 → Lab2
- Nhận xét chi tiết sự thay đổi về **độ sáng**, **sắc màu**, và **hướng dịch chuyển**
""")
st.markdown("---")

# ── Helper: Lab → preview hex ─────────────────────────────────────────────────
def lab_to_hex(L, a, b):
    Lab = np.array([L, a, b])
    XYZ = colour.Lab_to_XYZ(Lab)
    RGB = colour.XYZ_to_sRGB(XYZ)
    RGB = np.clip(RGB, 0, 1)
    return "#{:02X}{:02X}{:02X}".format(int(RGB[0]*255), int(RGB[1]*255), int(RGB[2]*255)), RGB

def describe_hue_angle(angle_deg):
    """Mô tả vùng màu dựa trên góc hue trong Lab."""
    a = angle_deg % 360
    if a < 30 or a >= 330:
        return "Đỏ"
    elif a < 90:
        return "Vàng – Đỏ cam"
    elif a < 120:
        return "Vàng"
    elif a < 150:
        return "Vàng – Lục"
    elif a < 210:
        return "Lục"
    elif a < 240:
        return "Lục – Lam"
    elif a < 270:
        return "Lam – Lam tím"
    elif a < 300:
        return "Lam – Tím"
    else:
        return "Đỏ tím"

# ── Nhập Lab1 ─────────────────────────────────────────────────────────────────
col_inp1, col_inp2 = st.columns(2)

with col_inp1:
    st.markdown("### 🔵 Màu Lab1 (nguồn)")
    L1 = st.number_input("L1*  (0 = đen, 100 = trắng)", 0.0, 100.0, 50.0, 0.5, key="L1")
    a1 = st.number_input("a1*  (âm = lục, dương = đỏ)", -128.0, 128.0, 30.0, 0.5, key="a1")
    b1 = st.number_input("b1*  (âm = lam, dương = vàng)", -128.0, 128.0, -20.0, 0.5, key="b1")

with col_inp2:
    st.markdown("### 🔴 Màu Lab2 (đích)")
    L2 = st.number_input("L2*  (0 = đen, 100 = trắng)", 0.0, 100.0, 70.0, 0.5, key="L2")
    a2 = st.number_input("a2*  (âm = lục, dương = đỏ)", -128.0, 128.0, -25.0, 0.5, key="a2")
    b2 = st.number_input("b2*  (âm = lam, dương = vàng)", -128.0, 128.0, 40.0, 0.5, key="b2")

# ── Preview màu ───────────────────────────────────────────────────────────────
hex1, rgb1 = lab_to_hex(L1, a1, b1)
hex2, rgb2 = lab_to_hex(L2, a2, b2)

pv1, pv2, pv3 = st.columns(3)
with pv1:
    st.markdown(f"""
    <div style='background:{hex1};width:100%;height:70px;border-radius:8px;
                border:2px solid #aaa'></div>
    <p style='text-align:center;font-size:13px;margin:4px 0'>
        <b>Lab1</b> → {hex1}<br>L={L1:.1f}, a={a1:.1f}, b={b1:.1f}
    </p>""", unsafe_allow_html=True)
with pv2:
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:center;
                height:70px;font-size:30px'>→</div>""", unsafe_allow_html=True)
with pv3:
    st.markdown(f"""
    <div style='background:{hex2};width:100%;height:70px;border-radius:8px;
                border:2px solid #aaa'></div>
    <p style='text-align:center;font-size:13px;margin:4px 0'>
        <b>Lab2</b> → {hex2}<br>L={L2:.1f}, a={a2:.1f}, b={b2:.1f}
    </p>""", unsafe_allow_html=True)

st.markdown("---")

if st.button("📊 Vẽ biểu đồ và phân tích", use_container_width=True):

    # ── Tính toán ──────────────────────────────────────────────────────────────
    dL = L2 - L1
    da = a2 - a1
    db = b2 - b1

    # Chroma
    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)
    dC = C2 - C1

    # Hue angle
    H1 = np.degrees(np.arctan2(b1, a1)) % 360
    H2 = np.degrees(np.arctan2(b2, a2)) % 360
    dH_raw = H2 - H1
    # Góc ngắn nhất
    if dH_raw > 180:
        dH_raw -= 360
    elif dH_raw < -180:
        dH_raw += 360

    # ΔE76 (Euclidean trong Lab)
    dE76 = np.sqrt(dL**2 + da**2 + db**2)

    # ΔE2000 qua colour-science
    Lab1_arr = np.array([L1, a1, b1])
    Lab2_arr = np.array([L2, a2, b2])
    dE2000 = colour.delta_E(Lab1_arr, Lab2_arr, method="CIE 2000")

    # ── Vẽ 2 biểu đồ ──────────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # ── Biểu đồ a*–b* (mặt phẳng màu sắc) ────────────────────────────────────
    ax1.set_facecolor("#1a1a2e")
    ax1.axhline(0, color="white", linewidth=0.5, alpha=0.4)
    ax1.axvline(0, color="white", linewidth=0.5, alpha=0.4)

    # Vẽ vòng tròn chroma tham chiếu
    for r in [25, 50, 75, 100]:
        circle = plt.Circle((0, 0), r, fill=False, color="white", linewidth=0.4, alpha=0.2)
        ax1.add_patch(circle)
        ax1.text(r, 1, f"{r}", color="white", fontsize=7, alpha=0.4)

    # Nhãn trục
    ax1.text(105, 0, "+a* (Đỏ)", color="#FF6666", fontsize=9, va="center")
    ax1.text(-105, 0, "−a* (Lục)", color="#66FF66", fontsize=9, va="center", ha="right")
    ax1.text(0, 108, "+b* (Vàng)", color="#FFFF66", fontsize=9, ha="center")
    ax1.text(0, -110, "−b* (Lam)", color="#6699FF", fontsize=9, ha="center")

    # Mũi tên chuyển dịch
    ax1.annotate("", xy=(a2, b2), xytext=(a1, b1),
                 arrowprops=dict(arrowstyle="-|>", color="white",
                                 lw=2, mutation_scale=18))

    # Điểm Lab1
    ax1.plot(a1, b1, "o", color=hex1, markersize=14,
             markeredgecolor="white", markeredgewidth=1.5, zorder=6)
    ax1.annotate(f"Lab1\n({a1:.1f}, {b1:.1f})", (a1, b1),
                 textcoords="offset points", xytext=(-12, 12), fontsize=8,
                 color="white",
                 bbox=dict(boxstyle="round,pad=0.3", fc="#333", alpha=0.8))

    # Điểm Lab2
    ax1.plot(a2, b2, "o", color=hex2, markersize=14,
             markeredgecolor="white", markeredgewidth=1.5, zorder=6)
    ax1.annotate(f"Lab2\n({a2:.1f}, {b2:.1f})", (a2, b2),
                 textcoords="offset points", xytext=(8, 8), fontsize=8,
                 color="white",
                 bbox=dict(boxstyle="round,pad=0.3", fc="#333", alpha=0.8))

    ax1.set_xlim([-120, 120])
    ax1.set_ylim([-120, 120])
    ax1.set_xlabel("a*  (Lục ← 0 → Đỏ)", color="white", fontsize=10)
    ax1.set_ylabel("b*  (Lam ← 0 → Vàng)", color="white", fontsize=10)
    ax1.set_title("Mặt phẳng a*–b* (Colour Gamut)", color="white", fontsize=12, pad=10)
    ax1.tick_params(colors="white")
    for spine in ax1.spines.values():
        spine.set_edgecolor("white")

    # ── Biểu đồ L* (thanh độ sáng) ────────────────────────────────────────────
    ax2.set_facecolor("#1a1a2e")

    # Gradient background L* từ đen → trắng
    grad = np.linspace(0, 1, 256).reshape(256, 1)
    ax2.imshow(grad, aspect="auto", cmap="gray",
               extent=[0.2, 0.8, 0, 100], origin="lower", alpha=0.35, zorder=1)

    # Thanh màu Lab1
    ax2.barh(L1, 0.25, left=0.1, height=3, color=hex1, zorder=5,
             edgecolor="white", linewidth=1)
    ax2.text(0.37, L1, f"L1 = {L1:.1f}", va="center", color="white", fontsize=11, zorder=6)

    # Thanh màu Lab2
    ax2.barh(L2, 0.25, left=0.1, height=3, color=hex2, zorder=5,
             edgecolor="white", linewidth=1)
    ax2.text(0.37, L2, f"L2 = {L2:.1f}", va="center", color="white", fontsize=11, zorder=6)

    # Mũi tên ΔL
    ax2.annotate("", xy=(0.22, L2), xytext=(0.22, L1),
                 arrowprops=dict(arrowstyle="-|>", color="#FFD700", lw=2, mutation_scale=15),
                 zorder=7)
    mid_L = (L1 + L2) / 2
    ax2.text(0.25, mid_L, f"ΔL = {dL:+.2f}", color="#FFD700", fontsize=10, va="center", zorder=7)

    ax2.set_xlim([0, 0.9])
    ax2.set_ylim([0, 100])
    ax2.set_yticks(range(0, 101, 10))
    ax2.set_ylabel("L*  (0 = Đen, 100 = Trắng)", color="white", fontsize=10)
    ax2.set_title("Trục độ sáng L*", color="white", fontsize=12, pad=10)
    ax2.set_xticks([])
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_edgecolor("white")

    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

    # ── Nhận xét chuyển dịch màu ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📝 Nhận xét sự chuyển dịch màu")

    # Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("ΔL* (Độ sáng)",   f"{dL:+.3f}", delta=f"{'Sáng hơn' if dL>0 else 'Tối hơn' if dL<0 else 'Không đổi'}")
    m2.metric("Δa* (Đỏ/Lục)",    f"{da:+.3f}", delta=f"{'→ Đỏ hơn' if da>0 else '→ Lục hơn' if da<0 else 'Không đổi'}")
    m3.metric("Δb* (Vàng/Lam)",  f"{db:+.3f}", delta=f"{'→ Vàng hơn' if db>0 else '→ Lam hơn' if db<0 else 'Không đổi'}")
    m4.metric("ΔE76",            f"{dE76:.4f}")
    m5.metric("ΔE2000",          f"{dE2000:.4f}")

    # Phân tích chi tiết
    # Độ sáng
    if abs(dL) < 1:
        L_nhan_xet = "Độ sáng **gần như không thay đổi** (ΔL < 1)."
    elif dL > 0:
        L_nhan_xet = f"Màu trở nên **sáng hơn** ({dL:+.2f} đơn vị L*). {'Thay đổi rõ rệt.' if dL > 5 else 'Thay đổi nhỏ.'}"
    else:
        L_nhan_xet = f"Màu trở nên **tối hơn** ({dL:+.2f} đơn vị L*). {'Thay đổi rõ rệt.' if abs(dL) > 5 else 'Thay đổi nhỏ.'}"

    # Sắc màu a*
    if abs(da) < 2:
        a_nhan_xet = "Thành phần đỏ–lục **hầu như không đổi** (Δa* < 2)."
    elif da > 0:
        a_nhan_xet = f"Dịch chuyển **về phía đỏ** (+a*) thêm {da:.2f} đơn vị. {'Đáng kể.' if da > 10 else 'Nhẹ.'}"
    else:
        a_nhan_xet = f"Dịch chuyển **về phía lục** (−a*) thêm {abs(da):.2f} đơn vị. {'Đáng kể.' if abs(da) > 10 else 'Nhẹ.'}"

    # Sắc màu b*
    if abs(db) < 2:
        b_nhan_xet = "Thành phần vàng–lam **hầu như không đổi** (Δb* < 2)."
    elif db > 0:
        b_nhan_xet = f"Dịch chuyển **về phía vàng** (+b*) thêm {db:.2f} đơn vị. {'Đáng kể.' if db > 10 else 'Nhẹ.'}"
    else:
        b_nhan_xet = f"Dịch chuyển **về phía lam** (−b*) thêm {abs(db):.2f} đơn vị. {'Đáng kể.' if abs(db) > 10 else 'Nhẹ.'}"

    # Chroma
    if abs(dC) < 2:
        C_nhan_xet = "Độ bão hoà màu (Chroma) **gần như không đổi**."
    elif dC > 0:
        C_nhan_xet = f"Độ bão hoà màu **tăng** {dC:.2f} đơn vị → màu trở nên **rực rỡ hơn**."
    else:
        C_nhan_xet = f"Độ bão hoà màu **giảm** {abs(dC):.2f} đơn vị → màu trở nên **nhạt/trung tính hơn**."

    # Hue
    H1_name = describe_hue_angle(H1)
    H2_name = describe_hue_angle(H2)
    if abs(dH_raw) < 5:
        H_nhan_xet = f"Sắc màu (Hue) **không thay đổi đáng kể** (ΔH ≈ {dH_raw:.1f}°). Vùng màu: **{H1_name}**."
    else:
        H_nhan_xet = (
            f"Sắc màu dịch chuyển từ **{H1_name}** (H={H1:.1f}°) "
            f"sang **{H2_name}** (H={H2:.1f}°), ΔH = {dH_raw:+.1f}°."
        )

    # Mức độ khác biệt theo ΔE2000
    if dE2000 < 1:
        dE_nhan_xet = "Sự khác biệt **không thể nhận biết** bằng mắt thường (ΔE₀₀ < 1)."
    elif dE2000 < 2:
        dE_nhan_xet = "Sự khác biệt rất nhỏ, **chỉ chuyên gia màu sắc mới nhận ra** (1 ≤ ΔE₀₀ < 2)."
    elif dE2000 < 3.5:
        dE_nhan_xet = "Sự khác biệt **có thể nhận ra** được nếu so sánh trực tiếp (2 ≤ ΔE₀₀ < 3.5)."
    elif dE2000 < 5:
        dE_nhan_xet = "Sự khác biệt **rõ ràng** khi nhìn cạnh nhau (3.5 ≤ ΔE₀₀ < 5)."
    else:
        dE_nhan_xet = f"Sự khác biệt **rất lớn**, hai màu **hoàn toàn khác nhau** (ΔE₀₀ = {dE2000:.2f} ≥ 5)."

    st.markdown(f"""
<div style='background:#f8f9ff;border-left:5px solid #003087;
            padding:18px 22px;border-radius:8px;line-height:1.9'>

**1. Độ sáng (L\*):** {L_nhan_xet}

**2. Thành phần Đỏ–Lục (a\*):** {a_nhan_xet}

**3. Thành phần Vàng–Lam (b\*):** {b_nhan_xet}

**4. Độ bão hoà màu (Chroma C\*):** {C_nhan_xet}  
→ C1 = {C1:.3f}, C2 = {C2:.3f}, ΔC = {dC:+.3f}

**5. Sắc màu (Hue H\*):** {H_nhan_xet}

**6. Tổng mức độ khác biệt:** {dE_nhan_xet}  
→ ΔE76 = {dE76:.4f} | ΔE2000 = {dE2000:.4f}

</div>
    """, unsafe_allow_html=True)

    # Bảng tóm tắt
    st.markdown("---")
    st.markdown("#### Bảng tóm tắt")
    import pandas as pd
    df_sum = pd.DataFrame({
        "Thuộc tính": ["L* (Độ sáng)", "a* (Đỏ/Lục)", "b* (Vàng/Lam)",
                       "C* (Chroma)", "H* (Hue °)", "ΔE76", "ΔE2000"],
        "Lab1": [f"{L1:.2f}", f"{a1:.2f}", f"{b1:.2f}", f"{C1:.2f}", f"{H1:.1f}°", "—", "—"],
        "Lab2": [f"{L2:.2f}", f"{a2:.2f}", f"{b2:.2f}", f"{C2:.2f}", f"{H2:.1f}°", "—", "—"],
        "Δ (thay đổi)": [f"{dL:+.2f}", f"{da:+.2f}", f"{db:+.2f}",
                          f"{dC:+.2f}", f"{dH_raw:+.1f}°", f"{dE76:.4f}", f"{dE2000:.4f}"],
    })
    st.dataframe(df_sum, use_container_width=True)

st.markdown("---")
st.caption("CIELab | ΔE CIE 76 & ΔE CIE 2000 | colour-science library")
