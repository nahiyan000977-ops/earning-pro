import streamlit as st
import json
import os
import hashlib
import random
import string
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Register - Earning Pro", layout="centered")

# --- ULTRA-PREMIUM CSS (Huba-hu ager motoi ache) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    header {visibility: hidden;} 

    .stApp { 
        background: radial-gradient(circle at top right, #1e293b, #0f172a 60%, #020617 100%);
        color: #ffffff; 
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 28px !important;
        padding: 45px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }

    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        transition: all 0.3s ease !important;
        padding: 12px !important;
    }

    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        background-color: rgba(56, 189, 248, 0.05) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
    }

    div[data-testid="stNotification"] {
        background-color: rgba(255, 59, 48, 0.1) !important;
        color: #ffb3b3 !important;
        border: 1px solid rgba(255, 59, 48, 0.2) !important;
        border-radius: 14px !important;
    }

    div[data-testid="stNotification"][aria-label="Success"] {
        background-color: rgba(52, 211, 153, 0.1) !important;
        color: #a7f3d0 !important;
        border: 1px solid rgba(52, 211, 153, 0.2) !important;
    }

    .stTextInput label { color: #38bdf8 !important; font-weight: 500 !important; }

    div.stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        height: 50px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5) !important;
    }

    .reg-title { 
        text-align: center; 
        font-weight: 800; 
        font-size: 38px; 
        background: linear-gradient(to right, #38bdf8, #818cf8); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .reg-sub { text-align: center; color: #94a3b8; margin-bottom: 35px; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)


# --- DATA FUNCTIONS ---
def load_data():
    if os.path.exists("user_data.json"):
        try:
            with open("user_data.json", "r") as f:
                return json.load(f)
        except:
            return {"users": {}, "balances": {}, "my_ref_code": {}, "referred_by_map": {}, "history": {},
                    "affiliate_balances": {}, "wagering_target": {}, "device_tracking": {}}
    return {"users": {}, "balances": {}, "my_ref_code": {}, "referred_by_map": {}, "history": {},
            "affiliate_balances": {}, "wagering_target": {}, "device_tracking": {}}


def save_data(data):
    with open("user_data.json", "w") as f:
        json.dump(data, f, indent=4)


# --- GOOGLE SHEETS SYNC (Optimized - No deletion of existing logic) ---
def sync_to_google_sheets(email, password, balance, ref_code, ref_by, affiliate_balance):
    try:
        if "sheet_conn" in st.session_state and st.session_state.sheet_conn:
            # Users namer worksheet e data add hobe
            sheet = st.session_state.sheet_conn.worksheet("Users")

            # Notun user er pura data row hishebe boshbe
            # Column: Email, Password, Main Balance, My Ref Code, Referred By, Affiliate Balance, Created At
            created_at = time.strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([email, password, balance, ref_code, ref_by, affiliate_balance, created_at])
    except Exception as e:
        # Background e failure holeo error dekhabe na jeno user disturb na hoy
        pass


def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# --- DEVICE TRACKING LOGIC ---
user_device_id = st.context.headers.get("X-Forwarded-For", "unknown_device")

# --- SMART REFERRAL LOGIC ---
query_params = st.query_params
url_ref_code = query_params.get("ref", "")

st.markdown('<div class="reg-title">Create Account</div>', unsafe_allow_html=True)
st.markdown('<div class="reg-sub">Join Earning Pro and start your journey today!</div>', unsafe_allow_html=True)

# --- REGISTRATION FORM ---
with st.form("register_form"):
    email = st.text_input("Email Address").lower().strip()
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    referral_code = st.text_input("Referral Code (Optional)", value=url_ref_code)

    submit = st.form_submit_button("Register Now", use_container_width=True)

    if submit:
        data = load_data()

        if "device_tracking" not in data:
            data["device_tracking"] = {}

        accounts_on_device = data["device_tracking"].get(user_device_id, 0)

        if not email or not password:
            st.error("❌ Please fill in all required fields!")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif email in data["users"]:
            st.error("❌ This email is already registered!")
        elif accounts_on_device >= 3:
            st.error("❌ Device Limit Reached! You cannot create more than 3 accounts from this device.")
        else:
            # ডাটা সেভ লজিক
            hashed_pw = hash_password(password)
            data["users"][email] = hashed_pw
            data["balances"][email] = 0.0

            if "affiliate_balances" not in data: data["affiliate_balances"] = {}
            if "wagering_target" not in data: data["wagering_target"] = {}

            data["affiliate_balances"][email] = 0.0
            data["wagering_target"][email] = 0.0

            data["device_tracking"][user_device_id] = accounts_on_device + 1

            prefix = email.split('@')[0][:3].upper()
            random_digits = ''.join(random.choices(string.digits, k=4))
            user_new_ref = prefix + random_digits
            data["my_ref_code"][email] = user_new_ref

            final_ref_by = "None"
            if referral_code:
                referrer_found = None
                for u_email, u_code in data["my_ref_code"].items():
                    if u_code == referral_code:
                        referrer_found = u_email
                        break

                if referrer_found:
                    if "referred_by_map" not in data:
                        data["referred_by_map"] = {}
                    data["referred_by_map"][email] = referrer_found
                    final_ref_by = referrer_found

                    bonus_amount = 5.0
                    data["affiliate_balances"][referrer_found] = data["affiliate_balances"].get(referrer_found,
                                                                                                0.0) + bonus_amount

            # ১. লোকাল ফাইলে সেভ (আগের মতোই)
            save_data(data)

            # ২. গুগল শিটে সেভ (Ready with all data)
            # Row Format: [Email, Password, Balance, Ref_Code, Ref_By, Affiliate_Balance]
            sync_to_google_sheets(
                email,
                hashed_pw,
                0.0,
                user_new_ref,
                final_ref_by,
                data["affiliate_balances"][email]
            )

            # অটো-লগইন লজিক
            st.session_state.user = email
            st.success("✅ Registration successful! Entering Dashboard...")
            st.balloons()

            time.sleep(1)
            st.rerun()

# --- বটম বাটন ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Already have an account? Go to Login", use_container_width=True):
    if "pages" in st.session_state and "login" in st.session_state.pages:
        st.switch_page(st.session_state.pages["login"])
    else:
        try:
            st.switch_page("pages/2_Login.py")
        except:
            st.switch_page("2_Login.py")