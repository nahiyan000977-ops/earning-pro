import streamlit as st
import json
import os
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Admin Control Panel", layout="wide")

# --- UNIVERSAL PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    header {visibility: hidden;} 

    /* High-End Radial Gradient Background */
    .stApp { 
        background: radial-gradient(circle at top right, #1e293b, #0f172a 60%, #020617 100%);
        color: #ffffff; 
    }

    /* Admin Expander/Card Styling */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 10px !important;
        backdrop-filter: blur(10px);
    }

    /* Table/Metric Boxes within Admin Panel */
    code {
        color: #38bdf8 !important;
        background-color: rgba(56, 189, 248, 0.1) !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
    }

    /* Approve/Reject Button Styling */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    /* Approve Button Special */
    div[data-testid="column"]:nth-of-type(1) .stButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important;
        border: none !important;
    }

    /* Reject Button Special */
    div[data-testid="column"]:nth-of-type(2) .stButton > button {
        background: rgba(255, 75, 75, 0.1) !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
    }

    /* Clear All Button */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# --- DATA FUNCTIONS ---
def load_data(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"users": {}, "balances": {}, "history": {}, "affiliate_balances": {},
                    "wagering_target": {}} if "user" in file_name else []
    return {"users": {}, "balances": {}, "history": {}, "affiliate_balances": {},
            "wagering_target": {}} if "user" in file_name else []


def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


# Admin Security Check
ADMIN_EMAIL = "omi529061@gmail.com"
if st.session_state.get("user") != ADMIN_EMAIL:
    st.error("⛔ Access Denied! You do not have permission to view this page.")
    st.stop()

st.title("🛡️ Admin Approval Panel")

# Load current data
requests = load_data("requests.json")
user_data = load_data("user_data.json")

if not requests:
    st.info("No pending requests at the moment.")
else:
    for i, req in enumerate(requests):
        # এক্সপান্ডারে লেবেল যোগ করা হয়েছে চেনার জন্য
        req_type = req.get('type', 'Unknown')
        req_label = req.get('label', '')
        display_title = f"📍 {req_type} {f'[{req_label}]' if req_label else ''} - {req.get('user', 'User')} (৳{req.get('amount', 0)})"

        with st.expander(display_title):

            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Method:** {req.get('method', 'N/A')}")
                trx_value = req.get('trxid') or req.get('TRXID') or req.get('number') or req.get(
                    'trx') or "Not Provided"
                st.markdown(f"**TRXID / Number:** `{trx_value}`")

            with col_b:
                req_time = req.get('time', 'Not Recorded')
                st.write(f"**Requested At:** {req_time}")
                st.write(f"**Amount:** ৳{req.get('amount', 0)}")

            st.write("---")

            col1, col2 = st.columns(2)

            # --- APPROVE LOGIC ---
            if col1.button(f"✅ Approve", key=f"app_{i}", use_container_width=True):
                user_email = req['user']
                amount = float(req['amount'])

                if req['type'] == "Deposit":
                    # মেইন ব্যালেন্স বাড়ানো
                    current_bal = user_data["balances"].get(user_email, 0.0)
                    user_data["balances"][user_email] = current_bal + amount

                    # ৭০% হিডেন টার্গেট সেট করা
                    wag_to_add = req.get('wagering_target', amount * 0.70)
                    if "wagering_target" not in user_data: user_data["wagering_target"] = {}
                    user_data["wagering_target"][user_email] = user_data["wagering_target"].get(user_email,
                                                                                                0.0) + wag_to_add

                    if "history" not in user_data: user_data["history"] = {}
                    if user_email not in user_data["history"]: user_data["history"][user_email] = []

                    user_data["history"][user_email].append({
                        "type": "Deposit",
                        "amount": amount,
                        "time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        "status": "Approved"
                    })

                    # --- রেফারেল বোনাস লজিক (৪০%) - এখন অ্যাফিলিয়েট ব্যালেন্সে যাবে ---
                    is_first = req.get('is_first_deposit', False)
                    referrer = user_data.get("referred_by_map", {}).get(user_email)

                    if is_first and referrer:
                        bonus_amount = amount * 0.40
                        if "affiliate_balances" not in user_data: user_data["affiliate_balances"] = {}

                        # এখানে মেইন ব্যালেন্সের বদলে অ্যাফিলিয়েট ব্যালেন্সে যোগ হচ্ছে
                        ref_aff_bal = user_data["affiliate_balances"].get(referrer, 0.0)
                        user_data["affiliate_balances"][referrer] = ref_aff_bal + bonus_amount

                        if referrer not in user_data["history"]: user_data["history"][referrer] = []
                        user_data["history"][referrer].append({
                            "type": "Referral Bonus (Affiliate)",
                            "from": user_email,
                            "amount": bonus_amount,
                            "time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        })

                requests.pop(i)
                save_data("user_data.json", user_data)
                save_data("requests.json", requests)
                st.success(f"Request for {user_email} Approved!")
                st.rerun()

            # --- REJECT LOGIC ---
            if col2.button(f"❌ Reject", key=f"rej_{i}", use_container_width=True):
                user_email = req['user']
                amount = float(req['amount'])
                if req['type'] == "Withdraw":
                    # রিজেক্ট করলে সঠিক ব্যালেন্সে টাকা ফেরত দেওয়া
                    if req.get('label') == "From Affiliate Account":
                        user_data["affiliate_balances"][user_email] = user_data["affiliate_balances"].get(user_email,
                                                                                                          0.0) + amount
                    else:
                        user_data["balances"][user_email] = user_data["balances"].get(user_email, 0.0) + amount

                requests.pop(i)
                save_data("user_data.json", user_data)
                save_data("requests.json", requests)
                st.warning(f"Request for {user_email} Rejected!")
                st.rerun()

st.write("---")
if st.button("🗑️ Clear All Pending Requests", use_container_width=True):
    save_data("requests.json", [])
    st.rerun()