import streamlit as st

st.set_page_config(page_title="Step 3 - ターミナルバリュー計算", layout="centered")
st.title("🌱 Step 3：ターミナルバリュー（永久成長）の計算")

with st.expander("❓ このステップの目的"):
    st.markdown("""
    - 明示的な5年間の予測のあと、企業が**永続的に成長していく部分**を評価するために**ターミナルバリュー（TV）**を使います。
    - TVは、DCFにおいてしばしば企業価値の大部分を占めます。
    - このステップでは、**永久成長率（g）**を設定し、5年目のFCFとWACCからTVを計算します。
    - 計算式：  
      **TV = FCF × (1 + g) / (WACC - g)**  
    - 注意：gはWACC未満である必要があります。
    """)

st.subheader("✅ 永久成長率（g）の設定方法を選択")
mode = st.radio("選択肢：", ["地域別売上比率から推定する", "手動で入力する"])

g = 0.0
if mode == "地域別売上比率から推定する":
    st.write("🌏 地域別売上構成比をスライダーで入力（合計100%になるように調整してください）")
    col1, col2, col3 = st.columns(3)
    with col1:
        jp = st.slider("日本", 0.0, 1.0, 0.6, 0.01)
    with col2:
        us = st.slider("米国", 0.0, 1.0, 0.3, 0.01)
    with col3:
        em = st.slider("新興国", 0.0, 1.0, 0.1, 0.01)

    total = jp + us + em
    if abs(total - 1.0) > 0.01:
        st.error("⚠️ 地域比率の合計が100%（=1.0）になっていません。調整してください。")
    else:
        g = jp * 0.01 + us * 0.03 + em * 0.05
        st.success(f"📈 推定された永久成長率 g：{g:.2%}")
else:
    g = st.number_input("永久成長率（g）を直接入力（例：0.015 = 1.5%）", value=0.015, format="%.3f")

st.markdown("---")
st.subheader("📌 ターミナルバリューの計算")

# 必要な値をsession_stateから取得
future_fcfs = st.session_state.get("future_fcfs", [])
wacc = st.session_state.get("wacc", None)

if not future_fcfs or wacc is None:
    st.warning("⚠️ Step 1とStep 2の入力を完了してください。")
else:
    fcf_last = future_fcfs[-1]
    if g >= wacc:
        st.error("❌ g（永久成長率）はWACCより小さくなければなりません。調整してください。")
    else:
        terminal_value = fcf_last * (1 + g) / (wacc - g)
        st.success(f"💰 ターミナルバリュー（TV）＝ {terminal_value:,.0f} 百万円")
        st.session_state["terminal_value"] = terminal_value
        st.session_state["g"] = g
