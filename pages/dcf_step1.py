import streamlit as st
import pandas as pd

st.set_page_config(page_title="Step 1 - FCF予測", layout="centered")
st.title("🧮 Step 1：FCFの予測（1〜5年目）")

with st.expander("❓ このステップの目的"):
    st.markdown("""
    - **フリーキャッシュフロー（FCF）** とは、企業が自由に使える現金のことです。
    - このステップでは、**過去のFCF**から**成長率を推定**し、**将来5年間のFCF**を予測します。
    - 予測されたFCFは後のステップで理論株価の計算に使います。
    """)

st.subheader("✅ 過去のFCFを入力してください（百万円）")
col1, col2, col3, col4, col5 = st.columns(5)

fcf_inputs = []
with col1:
    fcf1 = st.number_input("5年前", value=0, format="%d")
    fcf_inputs.append(fcf1)
with col2:
    fcf2 = st.number_input("4年前", value=0, format="%d")
    fcf_inputs.append(fcf2)
with col3:
    fcf3 = st.number_input("3年前", value=2107, format="%d")
    fcf_inputs.append(fcf3)
with col4:
    fcf4 = st.number_input("2年前", value=872, format="%d")
    fcf_inputs.append(fcf4)
with col5:
    fcf5 = st.number_input("1年前（直近）", value=1200, format="%d")
    fcf_inputs.append(fcf5)

if st.button("✅ FCFを確定して成長率を計算"):
    valid_fcfs = [v for v in fcf_inputs if v > 0]

    if len(valid_fcfs) >= 2:
        start_val = valid_fcfs[0]
        end_val = valid_fcfs[-1]
        n = len(valid_fcfs) - 1
        try:
            growth_rate = (end_val / start_val) ** (1 / n) - 1
        except ZeroDivisionError:
            growth_rate = 0.0
        st.success(f"📈 推定される平均成長率（CAGR）：{growth_rate:.2%}")

        future_fcfs = []
        current_fcf = fcf_inputs[-1] if fcf_inputs[-1] > 0 else end_val
        for i in range(1, 6):
            projected = current_fcf * ((1 + growth_rate) ** i)
            future_fcfs.append(round(projected))

        df = pd.DataFrame({
            "年度": [f"Year {i}" for i in range(1, 6)],
            "予測FCF（百万円）": future_fcfs
        })

        st.subheader("📊 予測された将来のFCF（編集可能）")
        edited_df = st.data_editor(df, num_rows="fixed", use_container_width=True)

        st.session_state["future_fcfs"] = edited_df["予測FCF（百万円）"].tolist()
        st.session_state["growth_rate"] = growth_rate

    else:
        st.warning("⚠️ 少なくとも2年以上のFCFを入力してください。")
