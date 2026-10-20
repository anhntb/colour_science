import streamlit as st
import numpy as np
import colour
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

st.set_page_config(page_title="Tính ΔE Màu sắc", page_icon="📐", layout="wide")

st.markdown("## 📐 Tính ΔE – Color Difference (Độ lệch màu)")
st.markdown("""
Công cụ tính **độ lệch màu ΔE** giữa màu **tham chiếu** (Reference) và màu **mẫu** (Sample)
theo 3 tiêu chuẩn: **ΔE76**, **ΔE94**, và **ΔE2000**.  
Đây là chỉ số quan trọng trong kiểm soát chất lượng màu sắc in ấn và thiết kế.
""")
st.markdown("---")

# ── Helper ────────────────────────────────────────────────────────────────────
def lab_to_hex(L, a, b):
    Lab = np.array([float(L), float(a), float(b)])
    XYZ = colour.Lab_to_XYZ(Lab)
    RGB = colour.XYZ_to_sRGB(XYZ)
    RGB = np.clip(RGB, 0, 1)
    return "#{:02X}{:02X}{:02X}".format(int(RGB[0]*255), int(RGB[1]*255), int(RGB[2]*255))

def classify_dE(dE, standard="ΔE2000"):
    if dE < 1.0:
        return "🟢 Không nhận biết được", "#27ae60"
    elif dE < 2.0:
        return "🟡 Chỉ chuyên gia màu mới nhận ra", "#f1c40f"
    elif dE < 3.5:
        return "🟠 Có thể nhận ra khi so sánh trực tiếp", "#e67e22"
    elif dE < 5.0:
        return "🔴 Rõ ràng khi nhìn cạnh nhau", "#e74c3c"
    elif dE < 12.0:
        return "🔴 Khác biệt lớn", "#c0392b"
    else:
        return "⛔ Hai màu hoàn toàn khác nhau", "#8e1a0e"

# ── Tabs: Nhập 1 cặp hoặc nhiều cặp ──────────────────────────────────────────
tab1, tab2 = st.tabs(["📌 Tính 1 cặp màu", "📋 Tính nhiều cặp (batch)"])

# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Nhập giá trị CIELab")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔵 Màu tham chiếu (Reference)")
        Lr = st.number_input("L ref", 0.0, 100.0, 50.0, 0.5, key="Lr")
        ar = st.number_input("a ref", -128.0, 128.0, 10.0, 0.5, key="ar")
        br = st.number_input("b ref", -128.0, 128.0, 20.0, 0.5, key="br")
        hex_r = lab_to_hex(Lr, ar, br)
        st.markdown(f"""
        <div style='background:{hex_r};width:100%;height:60px;border-radius:8px;
                    border:2px solid #aaa;margin:8px 0'></div>
        <p style='text-align:center;font-size:12px;color:#555'>Reference: <b>{hex_r}</b></p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🔴 Màu mẫu (Sample)")
        Ls = st.number_input("L sample", 0.0, 100.0, 55.0, 0.5, key="Ls")
        as_ = st.number_input("a sample", -128.0, 128.0, 15.0, 0.5, key="as")
        bs  = st.number_input("b sample", -128.0, 128.0, 30.0, 0.5, key="bs")
        hex_s = lab_to_hex(Ls, as_, bs)
        st.markdown(f"""
        <div style='background:{hex_s};width:100%;height:60px;border-radius:8px;
                    border:2px solid #aaa;margin:8px 0'></div>
        <p style='text-align:center;font-size:12px;color:#555'>Sample: <b>{hex_s}</b></p>
        """, unsafe_allow_html=True)

    if st.button("🧮 Tính ΔE", use_container_width=True, key="calc_single"):
        Lab_ref = np.array([Lr, ar, br])
        Lab_smp = np.array([Ls, as_, bs])

        dE76   = colour.delta_E(Lab_ref, Lab_smp, method="CIE 1976")
        dE94   = colour.delta_E(Lab_ref, Lab_smp, method="CIE 1994")
        dE2000 = colour.delta_E(Lab_ref, Lab_smp, method="CIE 2000")

        st.markdown("---")
        st.markdown("### Kết quả ΔE")

        m1, m2, m3 = st.columns(3)
        m1.metric("ΔE76  (CIE 1976)", f"{dE76:.4f}")
        m2.metric("ΔE94  (CIE 1994)", f"{dE94:.4f}")
        m3.metric("ΔE2000 (CIE 2000)", f"{dE2000:.4f}")

        label, bg_color = classify_dE(dE2000)
        st.markdown(f"""
        <div style='background:{bg_color};color:white;padding:14px 20px;
                    border-radius:8px;font-size:16px;font-weight:bold;text-align:center;margin:10px 0'>
            Đánh giá: {label}
        </div>
        """, unsafe_allow_html=True)

        # ── Biểu đồ so sánh 2 màu ─────────────────────────────────────────────
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            # Swatches
            fig, ax = plt.subplots(1, 2, figsize=(5, 2.5))
            ax[0].set_facecolor(hex_r)
            ax[0].set_title(f"Reference\n({Lr:.0f},{ar:.0f},{br:.0f})", fontsize=10)
            ax[0].axis("off")
            ax[1].set_facecolor(hex_s)
            ax[1].set_title(f"Sample\n({Ls:.0f},{as_:.0f},{bs:.0f})", fontsize=10)
            ax[1].axis("off")
            plt.suptitle("So sánh màu", fontsize=11)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)

        with col_chart2:
            # Gauge bar ΔE2000
            fig2, ax2 = plt.subplots(figsize=(5, 2.5))
            bar_colors = ["#27ae60", "#f1c40f", "#e67e22", "#e74c3c", "#c0392b"]
            bar_limits = [1, 2, 3.5, 5, 12]
            bar_labels = ["<1\nKhông\nnhận ra", "1–2\nChuyên\ngia", "2–3.5\nNhận ra\nkhi so", "3.5–5\nRõ\nràng", "5–12+\nKhác\nbiệt lớn"]
            cumx = 0
            for i, (lim, col, lbl) in enumerate(zip(bar_limits, bar_colors, bar_labels)):
                w = lim if i == 0 else lim - bar_limits[i-1]
                ax2.barh(0, w, left=cumx, height=0.5, color=col, alpha=0.8)
                center = cumx + w / 2
                ax2.text(center, 0, lbl, ha="center", va="center", fontsize=6.5, color="white", fontweight="bold")
                cumx += w

            # Chỉ thị vị trí ΔE2000
            dE_clamp = min(dE2000, 12.5)
            ax2.axvline(dE_clamp, color="black", linewidth=2.5, zorder=5)
            ax2.text(dE_clamp, 0.33, f"ΔE₀₀={dE2000:.2f}", ha="center", fontsize=9,
                     color="black", fontweight="bold",
                     bbox=dict(fc="white", ec="black", boxstyle="round,pad=0.2"))

            ax2.set_xlim([0, 12.5])
            ax2.set_ylim([-0.4, 0.6])
            ax2.axis("off")
            ax2.set_title("Thang đánh giá ΔE2000", fontsize=10)
            plt.tight_layout()
            st.pyplot(fig2, clear_figure=True)

        # Bảng thành phần
        st.markdown("#### Chi tiết thành phần")
        dL = Ls - Lr; da = as_ - ar; db = bs - br
        Cr = np.sqrt(ar**2 + br**2); Cs = np.sqrt(as_**2 + bs**2)
        df_det = pd.DataFrame({
            "Thành phần": ["L*", "a*", "b*", "C* (Chroma)"],
            "Reference": [f"{Lr:.2f}", f"{ar:.2f}", f"{br:.2f}", f"{Cr:.2f}"],
            "Sample":    [f"{Ls:.2f}", f"{as_:.2f}", f"{bs:.2f}", f"{Cs:.2f}"],
            "Δ":         [f"{dL:+.2f}", f"{da:+.2f}", f"{db:+.2f}", f"{Cs-Cr:+.2f}"],
        })
        st.dataframe(df_det, use_container_width=True)

        # Giải thích công thức
        with st.expander("📖 Giải thích công thức ΔE"):
            st.markdown(r"""
**ΔE76 (CIE 1976)** — khoảng cách Euclid trong không gian Lab:
$$\Delta E_{76} = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}$$

**ΔE94 (CIE 1994)** — có hệ số trọng số cho từng thành phần:
$$\Delta E_{94} = \sqrt{\left(\frac{\Delta L^*}{k_L S_L}\right)^2 + \left(\frac{\Delta C^*}{k_C S_C}\right)^2 + \left(\frac{\Delta H^*}{k_H S_H}\right)^2}$$

**ΔE2000 (CIE 2000)** — công thức chính xác nhất, có hiệu chỉnh cho vùng màu lam và độ chroma thấp.

**Thang đánh giá ΔE2000:**
| ΔE₀₀ | Mức độ nhận biết |
|------|-----------------|
| < 1 | Không nhận biết được |
| 1–2 | Chỉ chuyên gia màu nhận ra |
| 2–3.5 | Nhận ra khi so sánh trực tiếp |
| 3.5–5 | Rõ ràng khi đặt cạnh nhau |
| > 5 | Khác biệt lớn – hai màu khác nhau hoàn toàn |
            """)

# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Tính ΔE cho nhiều cặp màu (Batch)")
    st.markdown("""
    Nhập dữ liệu thủ công hoặc upload file CSV với cấu trúc:
    `Name, Lr, ar, br, Ls, as, bs`
    """)

    # Upload CSV batch
    batch_file = st.file_uploader("📂 Upload CSV batch", type=["csv"], key="batch_csv")

    if batch_file is not None:
        df_batch = pd.read_csv(batch_file)
        st.markdown("**Dữ liệu input:**")
        st.dataframe(df_batch, use_container_width=True)

        required_cols = {"Lr", "ar", "br", "Ls", "as", "bs"}
        if required_cols.issubset(set(df_batch.columns)):
            results_batch = []
            for _, row in df_batch.iterrows():
                Lab_r = np.array([row["Lr"], row["ar"], row["br"]])
                Lab_s = np.array([row["Ls"], row["as"], row["bs"]])
                dE76   = colour.delta_E(Lab_r, Lab_s, method="CIE 1976")
                dE94   = colour.delta_E(Lab_r, Lab_s, method="CIE 1994")
                dE2000 = colour.delta_E(Lab_r, Lab_s, method="CIE 2000")
                label, _ = classify_dE(dE2000)
                results_batch.append({
                    "Tên":    row.get("Name", f"Cặp {len(results_batch)+1}"),
                    "ΔE76":   round(dE76, 4),
                    "ΔE94":   round(dE94, 4),
                    "ΔE2000": round(dE2000, 4),
                    "Đánh giá": label,
                })

            df_results = pd.DataFrame(results_batch)
            st.markdown("**Kết quả:**")
            st.dataframe(df_results, use_container_width=True)

            # Biểu đồ bar ΔE2000
            fig_b, ax_b = plt.subplots(figsize=(max(6, len(df_results)*0.8), 4))
            colors_bar = [classify_dE(v)[1] for v in df_results["ΔE2000"]]
            bars = ax_b.bar(df_results["Tên"], df_results["ΔE2000"], color=colors_bar, edgecolor="white")
            ax_b.axhline(1,   color="#27ae60", linestyle="--", linewidth=1, alpha=0.7, label="ΔE=1 (ngưỡng không nhìn thấy)")
            ax_b.axhline(3.5, color="#e67e22", linestyle="--", linewidth=1, alpha=0.7, label="ΔE=3.5 (ngưỡng rõ ràng)")
            for bar, val in zip(bars, df_results["ΔE2000"]):
                ax_b.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                          f"{val:.2f}", ha="center", va="bottom", fontsize=9)
            ax_b.set_ylabel("ΔE2000", fontsize=11)
            ax_b.set_title("ΔE2000 theo từng cặp màu", fontsize=12)
            ax_b.legend(fontsize=8)
            ax_b.grid(True, axis="y", linestyle="--", alpha=0.4)
            plt.tight_layout()
            st.pyplot(fig_b, clear_figure=True)
        else:
            st.error(f"File CSV cần có các cột: {required_cols}")
    else:
        st.info("Upload file CSV để tính hàng loạt. Định dạng: `Name,Lr,ar,br,Ls,as,bs`")
        st.markdown("**Ví dụ file CSV:**")
        example = pd.DataFrame({
            "Name": ["Cyan", "Magenta", "Yellow"],
            "Lr": [57.84, 52.15, 87.37], "ar": [-49.31, 74.27, -9.17], "br": [-20.89, -35.50, 93.68],
            "Ls": [60.00, 55.00, 90.00], "as": [-45.00, 70.00, -7.00], "bs": [-18.00, -30.00, 90.00],
        })
        st.dataframe(example, use_container_width=True)

st.markdown("---")
st.caption("ΔE CIE 1976 | ΔE CIE 1994 | ΔE CIE 2000 | colour-science library | CIELab D50")
