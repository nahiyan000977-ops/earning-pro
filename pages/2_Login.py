import streamlit as st
import json
import hashlib
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Login - Earning Pro", layout="centered")

# --- ULTRA-PREMIUM CSS (Apnar ager design huba-hu rakha hoyeche) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    header {visibility: hidden;} 

    .stApp { 
        background: radial-gradient(circle at top right, #1e293b, #0f172a 60%, #020617 100%);
        color: #ffffff; 
    }

    div.stButton > button, div.stTextInput > div > div > input {
        transition: all 0.3s ease !important;
    }

    .login-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        margin-top: 20px;
    }

    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 12px !important;
    }

    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        border: none !important;
        height: 50px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        width: 100%;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5) !important;
    }

    .login-title { 
        text-align: center; 
        font-weight: 800; 
        font-size: 38px; 
        background: linear-gradient(to right, #38bdf8, #818cf8); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .login-sub { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)


def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BACKUP SYSTEM: GOOGLE SHEET THEKE DATA KHUJE ANA ---
def check_backup_login(email, hashed_pw):
    try:
        if "sheet_conn" in st.session_state and st.session_state.sheet_conn:
            sheet = st.session_state.sheet_conn.worksheet("Users")
            cell = sheet.find(email)
            if cell:
                # Password column 2 te ache (Register code onujayi)
                db_password = sheet.cell(cell.row, 2).value
                if db_password == hashed_pw:
                    return True
    except:
        pass
    return False


# --- LOGIN LOGIC ---
if "user" in st.session_state and st.session_state.user is not None:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="login-title">Welcome Back</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="login-sub">Logged in as: {st.session_state.user}</div>', unsafe_allow_html=True)

    if st.button("Go to Dashboard", use_container_width=True):
        st.switch_page("pages/3_Dashboard.py")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="login-title">User Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Enter your credentials to access your account</div>', unsafe_allow_html=True)

    with st.container():
        email = st.text_input("Enter Gmail").lower().strip()
        pwd = st.text_input("Enter Password", type="password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Login Now"):
            if email and pwd:
                hashed_input_pwd = hash_password(pwd)
                authenticated = False

                # ১. আপনার অরিজিনাল JSON লজিক (হুবহু রাখা হয়েছে)
                if os.path.exists("user_data.json"):
                    with open("user_data.json", "r") as f:
                        data = json.load(f)
                    if email in data.get("users", {}) and data["users"][email] == hashed_input_pwd:
                        authenticated = True

                # ২. ব্যাকআপ চেক (যদি অনলাইনে JSON ডিলিট হয়ে যায়)
                if not authenticated:
                    if check_backup_login(email, hashed_input_pwd):
                        authenticated = True

                if authenticated:
                    st.session_state.user = email
                    st.success(f"✅ Welcome {email}! Logging in...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Wrong Email or Password.")
            else:
                st.warning("⚠️ Please enter both email and password.")

    st.markdown("---")
    if st.button("Don't have an account? Register Here", use_container_width=True):
        st.switch_page("pages/1_Register.py")