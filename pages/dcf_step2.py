import streamlit as st

st.set_page_config(page_title="Step 2 - WACC計算", layout="centered")
st.markdown("<h3 style='white-space: nowrap;'>📉 Step 2：WACC（資本コスト）の計算</h3>", unsafe_allow_html=True)


with st.expander("❓ このステップの目的"):
    st.markdown("""
    - **WACC（加重平均資本コスト）**は、DCFモデルで使う**割引率（Discount Rate）**です。
    - 割引率とは、将来のキャッシュフローを現在の価値に換算するための「基準」です。
    - 企業が資金を調達する方法は大きく分けて2つ：
      - **株主資本（Equity）**：株主が期待するリターン（例：8%など）
      - **負債（Debt）**：借入にかかる利息（支払利息）で、税引後で評価します
    - WACCはこれらを加重平均して求めたものであり、企業の資本コストを総合的に表します。
    - この値をもとに、**次のステップで「ターミナルバリュー（6年目以降の企業価値）」を算出します。**
    """)

st.subheader("✅ 財務データを入力してください（百万円単位）")
col1, col2 = st.columns(2)
with col1:
    equity = st.number_input("自己資本", value=5000, format="%d")
    equity_cost = st.number_input("株主資本コスト（例：0.08 = 8%）", value=0.08, format="%.2f")
with col2:
    debt = st.number_input("有利子負債", value=0, format="%d")
    interest = st.number_input("年間の支払利息", value=0, format="%d")

col3, _ = st.columns(2)
with col3:
    tax_rate = st.number_input("法人税率（例：0.30 = 30%）", value=0.30, format="%.2f")

if st.button("✅ WACCを計算"):
    total_capital = equity + debt
    if total_capital == 0:
        st.error("⚠️ 自己資本と負債がともに0のため、WACCが計算できません。")
    else:
        equity_weight = equity / total_capital
        debt_weight = debt / total_capital
        debt_cost = (interest / debt) if debt > 0 else 0
        after_tax_debt_cost = debt_cost * (1 - tax_rate)

        wacc = equity_weight * equity_cost + debt_weight * after_tax_debt_cost
        st.success(f"📌 計算されたWACC：{wacc:.2%}")

        # セッションに保存
        st.session_state["wacc"] = wacc
