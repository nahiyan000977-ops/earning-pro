import streamlit as st
import json
import os
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Withdraw - Earning Pro", layout="centered")

# --- UNIVERSAL PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    header {visibility: hidden;} 
    .stApp { background: radial-gradient(circle at top right, #1e293b, #0f172a 60%, #020617 100%); color: #ffffff; }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 28px !important;
        padding: 35px !important;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
    }
    .balance-card {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
    }
    .affiliate-card {
        background: rgba(139, 92, 246, 0.05);
        border: 1px solid rgba(139, 92, 246, 0.2);
        padding: 15px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600;
        height: 50px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)


# --- DATA FUNCTIONS ---
def load_data(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except:
            return {"users": {}, "balances": {}, "history": {}, "affiliate_balances": {},
                    "wagering_target": {}} if "user" in file_name else []
    return {"users": {}, "balances": {}, "history": {}, "affiliate_balances": {},
            "wagering_target": {}} if "user" in file_name else []


def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


user_email = st.session_state.get("user")
if not user_email:
    st.error("Please login first!")
    st.stop()

st.title("📤 Withdraw Money")

user_data = load_data("user_data.json")
requests_data = load_data("requests.json")

# ব্যালেন্স লোড (আপনার ১ নং শর্ত অনুযায়ী আলাদা ব্যালেন্স)
current_balance = user_data.get("balances", {}).get(user_email, 0.0)
affiliate_balance = user_data.get("affiliate_balances", {}).get(user_email, 0.0)
hidden_wagering = user_data.get("wagering_target", {}).get(user_email, 0.0)

# চেক: পেন্ডিং উইথড্র আছে কিনা
has_pending_withdraw = False
if isinstance(requests_data, list):
    for r in requests_data:
        if r.get('user') == user_email and r.get('status') == "Pending":
            has_pending_withdraw = True
            break

# ব্যালেন্স ডিসপ্লে
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown(
        f'<div class="balance-card"><span style="color: #94a3b8; font-size: 13px;">Player Balance</span><br><span style="color: #38bdf8; font-size: 24px; font-weight: 700;">৳ {current_balance}</span></div>',
        unsafe_allow_html=True)
with col_b2:
    st.markdown(
        f'<div class="affiliate-card"><span style="color: #94a3b8; font-size: 13px;">Affiliate Balance</span><br><span style="color: #a78bfa; font-size: 24px; font-weight: 700;">৳ {affiliate_balance}</span></div>',
        unsafe_allow_html=True)

if has_pending_withdraw:
    st.warning("⚠️ You already have a pending request. Please wait.")
else:
    # উইথড্র টাইপ সিলেক্ট (আপনার ১ নং শর্ত)
    withdraw_type = st.radio("Withdraw From:", ["Player Balance", "Affiliate Account"], horizontal=True)

    with st.form("withdraw_form"):
        method = st.selectbox("Select Method", ["Bkash", "Nagad", "Rocket"])
        number = st.text_input("Account Number")
        amount = st.number_input("Amount", min_value=100, step=50)
        submit = st.form_submit_button("Submit Request")

        if submit:
            # শর্ত ১: অ্যাফিলিয়েট অ্যাকাউন্ট উইথড্র (মিনিমাম ২০০০)
            if withdraw_type == "Affiliate Account":
                if affiliate_balance < 2000:
                    st.error("❌ Affiliate withdrawal requires a minimum balance of ৳ 2000.")
                elif amount > affiliate_balance:
                    st.error("❌ Insufficient Affiliate balance!")
                elif amount < 2000:
                    st.error("❌ Minimum Affiliate withdraw amount is ৳ 2000.")
                else:
                    # সাকসেস লজিক ফর অ্যাফিলিয়েট
                    user_data["affiliate_balances"][user_email] -= amount
                    process_withdraw = True
                    withdraw_label = "From Affiliate Account"

            # শর্ত ২: প্লেয়ার ব্যালেন্স উইথড্র (৭০% ওয়েজারিং চেক)
            else:
                if hidden_wagering > 0.1:  # ০.১ দেওয়া হয়েছে ফ্লোটিং পয়েন্ট সেফটির জন্য
                    st.error(
                        f"❌ You need to play ৳ {round(hidden_wagering, 2)} more in games before you can withdraw your deposit.")
                elif amount > current_balance:
                    st.error("❌ Insufficient Player balance!")
                else:
                    user_data["balances"][user_email] -= amount
                    process_withdraw = True
                    withdraw_label = "From Player Balance"

            # ফাইনাল প্রসেসিং
            if 'process_withdraw' in locals() and process_withdraw:
                now = datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")

                # হিস্টোরিতে সেভ
                if "history" not in user_data: user_data["history"] = {}
                if user_email not in user_data["history"]: user_data["history"][user_email] = []
                user_data["history"][user_email].append({
                    "type": f"Withdraw ({withdraw_label})", "amount": amount, "method": method, "time": now,
                    "status": "Pending"
                })
                save_data("user_data.json", user_data)

                # রিকোয়েস্ট লিস্টে সেভ (আপনার ১ নং শর্ত অনুযায়ী লেবেলসহ)
                if not isinstance(requests_data, list): requests_data = []
                requests_data.append({
                    "user": user_email, "type": "Withdraw", "label": withdraw_label,  # এডমিন প্যানেলের জন্য লেবেল
                    "method": method, "number": number, "amount": amount, "time": now, "status": "Pending"
                })
                save_data("requests.json", requests_data)

                st.success(f"✅ Request submitted {withdraw_label}!")
                st.balloons()
                st.rerun()

st.info("💡 Note: Processing takes up to 24 hours.")