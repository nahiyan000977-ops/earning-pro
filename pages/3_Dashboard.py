import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Earning Pro | Premium", layout="wide")

# --- LOGIN CHECK ---
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please Login first!")
    st.stop()

user_email = str(st.session_state.user)
initial = user_email[0].upper()


# --- LOGOUT FUNCTION ---
def logout_user():
    st.session_state.user = None
    st.session_state.clear()
    st.rerun()


# --- ORIGINAL CSS (Unchanged) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    header { background-color: rgba(0,0,0,0) !important; backdrop-filter: none !important; }

    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; }

    /* Navbar */
    .nav-bar {
        position: fixed; top: 0; left: 0; width: 100%;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 10px 50px;
        display: flex; justify-content: space-between; align-items: center;
        z-index: 999; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .logo { font-size: 24px; font-weight: 700; background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .user-box { display: flex; align-items: center; gap: 12px; background: rgba(56, 189, 248, 0.1); padding: 5px 15px; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.2); }

    .main .block-container { padding-top: 100px !important; }

    /* Stats Card with Original Hover */
    .stats-card { 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 24px; 
        padding: 25px; 
        transition: transform 0.3s ease, background 0.3s ease, border-color 0.3s ease; 
        height: 120px;
    }
    .stats-card:hover { 
        transform: translateY(-10px) !important; 
        background: rgba(255, 255, 255, 0.06);
        border-color: #38bdf8; 
    }

    /* Original Hover Effect for Buttons */
    div.stButton > button {
        background: linear-gradient(145deg, #1e293b, #0f172a) !important;
        color: #f8fafc !important;
        border-radius: 20px !important;
        height: 120px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: transform 0.3s ease, border-color 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        border-color: #38bdf8 !important;
    }

    /* Fixed Bottom Logout Button */
    div.stButton > button[key="logout_btn"] {
        background: rgba(255, 75, 75, 0.1) !important;
        color: #ff4b4b !important;
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        height: 50px !important;
        margin-top: 60px !important;
        border-radius: 12px !important;
        width: 100% !important;
    }

    .section-title { font-size: 20px; font-weight: 600; margin: 40px 0 20px 0; color: #38bdf8; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION BAR ---
st.markdown(f'''
    <div class="nav-bar">
        <div class="logo">EARNING PRO AI</div>
        <div class="user-box">
            <span style="font-size: 13px; color: #38bdf8;">{user_email}</span>
            <div style="width: 32px; height: 32px; background: #38bdf8; border-radius: 8px; color: #0f172a; display: flex; align-items: center; justify-content: center; font-weight: 700;">{initial}</div>
        </div>
    </div>
''', unsafe_allow_html=True)


# --- DATA ---
def load_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as f: return json.load(f)
    return {"balances": {}, "referred_by_map": {}, "my_ref_code": {}, "affiliate_balances": {}, "wagering_target": {}}


data = load_data()
balance = data.get("balances", {}).get(user_email, 0.0)
affiliate_balance = data.get("affiliate_balances", {}).get(user_email, 0.0)
wagering = data.get("wagering_target", {}).get(user_email, 0.0)
my_code = data.get("my_ref_code", {}).get(user_email, "N/A")
ref_count = list(data.get("referred_by_map", {}).values()).count(user_email)

# --- MAIN CONTENT ---
st.markdown(f'<h1 style="font-weight:700; font-size:42px;">Portfolio Overview</h1>', unsafe_allow_html=True)

# Admin Mode
ADMIN_EMAIL = "omi529061@gmail.com"
if user_email == ADMIN_EMAIL:
    st.markdown(
        '<div style="background: rgba(56, 189, 248, 0.05); border: 1px solid #38bdf8; border-radius: 24px; padding: 20px; text-align: center;">🛡️ Admin Mode Active</div>',
        unsafe_allow_html=True)
    if st.button("🔓 OPEN ADMIN PANEL", use_container_width=True):
        st.switch_page("pages/5_Admin_Panel.py")

# Stats Grid (Updated to show Affiliate and Wagering)
st.markdown('<div class="section-title">Current Statistics</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1: st.markdown(
    f'<div class="stats-card"><div style="color: #94a3b8;">Player Balance</div><div style="font-size: 28px; font-weight: 700;">৳ {balance:,.2f}</div></div>',
    unsafe_allow_html=True)

with c2: st.markdown(
    f'<div class="stats-card"><div style="color: #94a3b8;">Affiliate Account</div><div style="font-size: 28px; font-weight: 700; color: #a78bfa;">৳ {affiliate_balance:,.2f}</div></div>',
    unsafe_allow_html=True)

with c3: st.markdown(
    f'<div class="stats-card"><div style="color: #94a3b8;">Play Required</div><div style="font-size: 28px; font-weight: 700; color: #fbbf24;">৳ {wagering:,.2f}</div></div>',
    unsafe_allow_html=True)

with c4: st.markdown(
    f'<div class="stats-card"><div style="color: #94a3b8;">Network Size</div><div style="font-size: 28px; font-weight: 700;">{ref_count}</div></div>',
    unsafe_allow_html=True)


# Action Grid (Updated for Stable Earn)
st.markdown('<div class="section-title">Financial Terminal</div>', unsafe_allow_html=True)
# কলাম সংখ্যা ৪ থেকে বাড়িয়ে ৫ করা হয়েছে নতুন বাটনের জন্য
b1, b2, b3, b4, b5 = st.columns(5)
with b1:
    if st.button("💎\nDeposit Funds"): st.switch_page("pages/6_Deposit.py")
with b2:
    if st.button("🚀\nWithdrawal"): st.switch_page("pages/7_withdraw.py")
with b3:
    if st.button("🕹️\nPlay Game"): st.switch_page("pages/4_Play_Game.py")
with b4:
    if st.button("📢\nRefer Center"): st.switch_page("pages/8_Refer.py")
with b5:
    # নতুন Stable Earn বাটনটি এখানে যোগ করা হলো
    if st.button("✨\nStable Earn"): st.switch_page("pages/9_Packages.py")

# --- NEW LOGIC FOR ACTIVE ASSETS BUTTON ---
# এটি ফাইন্যান্সিয়াল টার্মিনালের নিচে একটি বিশেষ বাটন যোগ করবে
st.markdown('<div class="section-title">Investment Portal</div>', unsafe_allow_html=True)
if st.button("⚡ VIEW ACTIVE ASSETS", use_container_width=True):
    # সেশন স্টেটে একটি ভেরিয়েবল সেট করা হচ্ছে যাতে অন্য পেজ বুঝতে পারে এই বাটনটি চাপা হয়েছে
    st.session_state.show_active_assets = True
    st.switch_page("pages/9_Packages.py")

# Affiliate Hub
st.markdown('<div class="section-title">Affiliate Hub</div>', unsafe_allow_html=True)
st.code(f"https://earning-pro-bd.streamlit.app/", language=None)

# --- LOGOUT ---
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("Logout From Account 🚪", key="logout_btn", use_container_width=True):
    logout_user()