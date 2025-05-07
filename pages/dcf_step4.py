import streamlit as st

st.set_page_config(page_title="Step 4 - 株価の算出", layout="centered")
st.markdown("<h3 style='white-space: nowrap;'>💹 Step 4：企業価値と理論株価</h3>", unsafe_allow_html=True)


with st.expander("❓ このステップの目的"):
    st.markdown("""
    - これまでのステップで求めた**5年間のFCF**と**ターミナルバリュー（TV）**をもとに、企業の**全体価値（Enterprise Value）**を算出します。
    - そこから**純有利子負債（負債 − 現金）**を引くことで、**株主価値（Equity Value）**を求めます。
    - 最後に、**発行済株式数**で割ることで、**理論株価（1株あたりの価値）**が求まります。
    """)

# 入力
st.subheader("✅ 補足データの入力（百万円単位）")
col1, col2 = st.columns(2)
with col1:
    cash = st.number_input("現金・現金同等物", value=1000, format="%d")
    shares = st.number_input("発行済株式数（百万株）", value=10.0, format="%.2f")
with col2:
    debt = st.number_input("有利子負債（繰り返し）", value=0, format="%d")

# 前ステップの値
future_fcfs = st.session_state.get("future_fcfs", [])
wacc = st.session_state.get("wacc", None)
terminal_value = st.session_state.get("terminal_value", None)

def present_value(fcf, year, rate):
    return fcf / ((1 + rate) ** year)

# --- 理論株価の計算セクション ---
st.subheader("💰 理論株価の計算")

if st.button("✅ 理論株価を計算"):
    if not future_fcfs or wacc is None or terminal_value is None:
        st.warning("⚠️ Step 1〜3の入力を完了してください。")
    else:
        # 各年の現在価値を計算
        pv_list = [present_value(fcf, year+1, wacc) for year, fcf in enumerate(future_fcfs)]
        pv_terminal = present_value(terminal_value, 5, wacc)
        enterprise_value = sum(pv_list) + pv_terminal

        st.subheader("📊 現在価値の合計と企業価値")
        st.write(f"🔹 5年間のFCF現在価値合計： {sum(pv_list):,.0f} 百万円")
        st.write(f"🔹 ターミナルバリュー現在価値： {pv_terminal:,.0f} 百万円")
        st.success(f"🏢 企業価値（Enterprise Value）： {enterprise_value:,.0f} 百万円")

        equity_value = enterprise_value + cash - debt
        stock_price = equity_value / (shares * 1_000_000) * 1_000_000  # 百万円→円に換算

        st.subheader("💰 理論株価の計算結果")
        st.write(f"株主価値（Equity Value）：{equity_value:,.0f} 百万円")
        st.success(f"📈 理論株価： {stock_price:.2f} 円")

        # セッションに保存して比較ステップへ引き渡し
        st.session_state["stock_price"] = stock_price

# --- 現在株価との比較セクション（理論株価計算後にのみ表示） ---
if "stock_price" in st.session_state:
    st.markdown("---")
    st.subheader("📉 現在株価との比較")

    current_price = st.number_input("現在の株価（円）", value=3000.0, format="%.2f")

    if st.button("📊 割安・割高を判定"):
        stock_price = st.session_state["stock_price"]
        if stock_price and current_price > 0:
            diff = stock_price - current_price
            diff_pct = diff / current_price * 100

            if diff > 0:
                st.success(f"✅ 理論株価の方が **{diff:,.2f}円 高く**、約 **{diff_pct:.2f}% 割安**です。")
            elif diff < 0:
                st.error(f"⚠️ 理論株価の方が **{abs(diff):,.2f}円 低く**、約 **{abs(diff_pct):.2f}% 割高**です。")
            else:
                st.info("理論株価と現在株価は同じです。")


