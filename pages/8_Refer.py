import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Refer & Earn - Earning Pro", layout="centered")

# --- UNIVERSAL PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    header {visibility: hidden;} 
    .stApp { 
        background: radial-gradient(circle at top right, #1e293b, #0f172a 60%, #020617 100%);
        color: #ffffff; 
    }
    .stInfo, .stSuccess {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    .ref-code-display {
        background: rgba(56, 189, 248, 0.1);
        border: 2px dashed #38bdf8;
        padding: 10px;
        border-radius: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# --- ডাটা লোড করার ফাংশন ---
def load_data(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except:
            return {"users": {}, "balances": {}, "history": {}, "my_ref_code": {}, "referred_by_map": {},
                    "affiliate_balances": {}}
    return {"users": {}, "balances": {}, "history": {}, "my_ref_code": {}, "referred_by_map": {},
            "affiliate_balances": {}}


# ইউজার লগইন চেক
user_email = st.session_state.get("user")
if not user_email:
    st.error("Please login first!")
    st.stop()

st.title("🔗 Refer & Earn")
user_data = load_data("user_data.json")

# ইউজারের নিজস্ব রেফারেল কোড
my_code = user_data.get("my_ref_code", {}).get(user_email, "Not Generated")

st.markdown("### Share your code and get **40% Bonus** on their first deposit!")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="stInfo">
            <span style="font-size: 14px; color: #94a3b8;">YOUR REFERRAL CODE</span>
            <div class="ref-code-display">{my_code}</div>
            <p style="font-size: 12px; color: #64748b; margin-top: 10px;">Copy and share with friends.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # শর্ত ১: এখন বোনাস সরাসরি affiliate_balances থেকে দেখানো হচ্ছে
    total_bonus = user_data.get("affiliate_balances", {}).get(user_email, 0.0)

    # রেফারেল কাউন্ট বের করা (হিস্টরি থেকে)
    user_history = user_data.get("history", {}).get(user_email, [])
    ref_count = sum(
        1 for entry in user_history if isinstance(entry, dict) and "Referral Bonus" in str(entry.get("type")))

    st.markdown(f"""
        <div class="stSuccess">
            <span style="font-size: 14px; color: #94a3b8;">AFFILIATE BALANCE</span>
            <div style="font-size: 28px; font-weight: 700; color: #34d399; margin-top: 10px;">৳ {total_bonus}</div>
            <p style="font-size: 12px; color: #64748b; margin-top: 10px;">Total Successful Referrals: {ref_count}</p>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# বোনাস রুলস (আপনার ১ নং শর্ত অনুযায়ী আপডেট করা)
st.markdown("""
### 📢 How it works?
1. **Invite Friends:** Ask your friends to register using your **Referral Code**.
2. **They Deposit:** When they make their **first deposit**.
3. **Instant Bonus:** You will get **40% bonus** in your Affiliate Account.
4. **Withdrawal:** You can withdraw your affiliate earnings once they reach **৳ 2000**.
""")

# রেফারেল হিস্টোরি টেবিল
if st.checkbox("Show Referral History Details"):
    ref_history = []
    for h in user_history:
        if isinstance(h, dict) and "Referral Bonus" in h.get("type", ""):
            status = "✅" if h.get("status") != "Rejected" else "❌"
            ref_history.append(
                f"{status} Received ৳{h.get('amount')} from {h.get('from', 'User')} on {h.get('time', 'N/A')}")

    if ref_history:
        for item in ref_history:
            st.info(item)
    else:
        st.write("No referral bonus received yet.")