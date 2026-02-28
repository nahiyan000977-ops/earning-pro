import streamlit as st
import json
import os
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Deposit - Earning Pro", layout="centered")

# --- UNIVERSAL PREMIUM CSS (Original Unchanged) ---
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
        padding: 30px !important;
        backdrop-filter: blur(20px);
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        height: 45px !important;
        width: 100% !important;
    }
    .payment-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        margin-bottom: 10px;
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
            return {"users": {}, "balances": {}, "history": {}, "wagering_target": {},
                    "referred_by_map": {}} if "user" in file_name else []
    return {"users": {}, "balances": {}, "history": {}, "wagering_target": {},
            "referred_by_map": {}} if "user" in file_name else []


def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


# --- GOOGLE SHEET SYNC (Checking if first deposit from Cloud) ---
def is_truly_first_deposit(email, local_history):
    # Prothome local history check kora
    for h in local_history:
        if isinstance(h, dict) and h.get("type") == "Deposit" and h.get("status") == "Approved":
            return False

    # Jodi local e na thake (Cloud reset), tobe sheet check kora
    try:
        if "sheet_conn" in st.session_state and st.session_state.sheet_conn:
            sheet = st.session_state.sheet_conn.worksheet("Users")
            cell = sheet.find(email)
            if cell:
                # Row index 3 (Main Balance) jodi 0 er beshi hoy, mane shey age deposit koreche
                balance_on_sheet = float(sheet.cell(cell.row, 3).value or 0)
                if balance_on_sheet > 0:
                    return False
    except:
        pass
    return True


user_email = st.session_state.get("user")
if not user_email:
    st.error("Please login first!")
    st.stop()

st.title("💰 Deposit Money")

# --- ADMIN PAYMENT DETAILS (Original Unchanged) ---
st.markdown("### Admin Payment Details")
st.markdown(
    '''<div class="payment-box"><img src="https://img.icons8.com/color/48/000000/wallet.png" width="30" style="margin-right: 15px;"><span style="color: #ffffff; font-weight: 400; font-size: 16px;"><i style="color: #ffb7d5;">Bkash (Personal):</i> <b style="color: #ffb7d5;">01872328618</b></span></div>''',
    unsafe_allow_html=True)
st.markdown(
    '''<div class="payment-box"><img src="https://img.icons8.com/color/48/000000/money-box.png" width="30" style="margin-right: 15px;"><span style="color: #ffffff; font-weight: 400; font-size: 16px;"><i style="color: #ffd29d;">Nagad (Personal):</i> <b style="color: #ffd29d;">01849378469</b></span></div>''',
    unsafe_allow_html=True)
st.markdown(
    '''<div class="payment-box"><img src="https://img.icons8.com/color/48/000000/safe.png" width="30" style="margin-right: 15px;"><span style="color: #ffffff; font-weight: 400; font-size: 16px;"><i style="color: #d8b4fe;">Rocket (Personal):</i> <b style="color: #d8b4fe;">01325839867</b></span></div>''',
    unsafe_allow_html=True)
st.write("---")

# Deposit Form
with st.form("deposit_form"):
    method = st.selectbox("Select Method", ["Bkash", "Nagad", "Rocket"])
    amount = st.number_input("Amount (Min 100 BDT)", min_value=100, value=100, step=50)
    trxid = st.text_input("Transaction ID (TRXID)").strip()
    submit = st.form_submit_button("Submit Deposit")

    if submit:
        if not trxid:
            st.error("Please enter the Transaction ID!")
        elif len(trxid) < 6:
            st.error("Invalid Transaction ID!")
        else:
            user_data = load_data("user_data.json")
            requests_data = load_data("requests.json")
            if not isinstance(requests_data, list): requests_data = []

            duplicate_check = any(req.get('trxid') == trxid for req in requests_data)

            if duplicate_check:
                st.error("This Transaction ID is already under review. Please wait!")
            else:
                now = datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
                user_history = user_data.get("history", {}).get(user_email, [])

                # Smart Check for First Deposit
                is_first_deposit = is_truly_first_deposit(user_email, user_history)

                referred_by = user_data.get("referred_by_map", {}).get(user_email, None)
                wagering_to_add = float(amount) * 0.70

                new_request = {
                    "user": user_email, "type": "Deposit", "method": method,
                    "trxid": trxid, "amount": amount, "time": now,
                    "status": "Pending", "is_first_deposit": is_first_deposit,
                    "referred_by": referred_by,
                    "wagering_target": wagering_to_add
                }
                requests_data.append(new_request)
                save_data("requests.json", requests_data)
                st.success(f"Deposit request of ৳{amount} submitted!")
                st.balloons()