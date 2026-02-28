import streamlit as st
import json
import os
import gspread  # নতুন যোগ করা হলো
from google.oauth2 import service_account  # নতুন যোগ করা হলো

# --- GOOGLE SHEETS CONNECTION (নতুন কানেকশন লজিক) ---
# এটি তোমার Secrets থেকে তথ্য নিয়ে গুগল শিটের সাথে যোগাযোগ করবে
def connect_to_sheet():
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        client = gspread.authorize(credentials)
        # তোমার শিটের নাম হুবহু 'EARNING-PRO-BD' হতে হবে
        return client.open("EARNING-PRO-BD")
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# কানেকশনটি সেশন স্টেটে রাখা হচ্ছে যাতে সব পেজ থেকে ব্যবহার করা যায়
if "sheet_conn" not in st.session_state:
    st.session_state.sheet_conn = connect_to_sheet()

# --- INITIALIZE NEW DATA FIELDS (তোমার আগের কোড হুবহু রাখা হলো) ---
def sync_data_structure():
    if os.path.exists("user_data.json"):
        try:
            with open("user_data.json", "r") as f:
                data = json.load(f)

            updated = False
            fields = {
                "affiliate_balances": {},
                "wagering_target": {},
                "device_tracking": {},
                "active_packages": {}
            }

            for key, default_value in fields.items():
                if key not in data:
                    data[key] = default_value
                    updated = True

            if updated:
                with open("user_data.json", "w") as f:
                    json.dump(data, f, indent=4)
        except:
            pass

sync_data_structure()

if "user" not in st.session_state:
    st.session_state.user = None

# --- PAGE DEFINITIONS (তোমার আগের কোড হুবহু রাখা হলো) ---
register_pg = st.Page("pages/1_Register.py", title="Register", icon="📝")
login_pg = st.Page("pages/2_Login.py", title="Login", icon="🔑")
dashboard_pg = st.Page("pages/3_Dashboard.py", title="Dashboard", icon="📊")
game_pg = st.Page("pages/4_Play_Game.py", title="Color Game", icon="🎮")
admin_pg = st.Page("pages/5_Admin_Panel.py", title="Admin Panel", icon="🛠️")
deposit_pg = st.Page("pages/6_Deposit.py", title="Deposit Funds", icon="📥")
withdraw_pg = st.Page("pages/7_withdraw.py", title="Withdraw Money", icon="📤")
refer_pg = st.Page("pages/8_Refer.py", title="Refer & Earn", icon="👥")
packages_pg = st.Page("pages/9_Packages.py", title="Stable Earn", icon="💎")

st.session_state.pages = {
    "dashboard": dashboard_pg,
    "deposit": deposit_pg,
    "withdraw": withdraw_pg,
    "game": game_pg,
    "refer": refer_pg,
    "register": register_pg,
    "login": login_pg,
    "packages": packages_pg
}

if st.session_state.user is None:
    pg = st.navigation([register_pg, login_pg])
else:
    pages_list = [dashboard_pg, packages_pg, game_pg, deposit_pg, withdraw_pg, refer_pg]
    if st.session_state.user == "omi529061@gmail.com":
        pages_list.append(admin_pg)
    pg = st.navigation(pages_list)

# --- SAFE NAVIGATION LOGIC ---
if "register_clicked" in st.session_state and st.session_state.register_clicked:
    st.session_state.register_clicked = False
    st.switch_page("pages/1_Register.py")

pg.run()