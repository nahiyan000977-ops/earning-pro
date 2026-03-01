import streamlit as st
import json
import os


# --- INITIALIZE NEW DATA FIELDS ---
# অ্যাপ শুরুতেই যেন নতুন ডাটা স্ট্রাকচারগুলো লোড করতে পারে তার ব্যবস্থা
def sync_data_structure():
    if os.path.exists("user_data.json"):
        try:
            with open("user_data.json", "r") as f:
                data = json.load(f)

            # আপনার শর্তানুযায়ী নতুন ফিল্ডগুলো চেক করা এবং না থাকলে যোগ করা
            updated = False
            fields = {
                "affiliate_balances": {},
                "wagering_target": {},
                "device_tracking": {},
                "active_packages": {} # Packages এর জন্য নতুন ফিল্ড যোগ করা হলো
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

# --- PAGE DEFINITIONS ---
# প্রতিটি পেজকে একটি ভেরিয়েবলে রাখা হচ্ছে যাতে সুইচ করা সহজ হয়
register_pg = st.Page("pages/1_Register.py", title="Register", icon="📝")
login_pg = st.Page("pages/2_Login.py", title="Login", icon="🔑")
dashboard_pg = st.Page("pages/3_Dashboard.py", title="Dashboard", icon="📊")
game_pg = st.Page("pages/4_Play_Game.py", title="Color Game", icon="🎮")
admin_pg = st.Page("pages/5_Admin_Panel.py", title="Admin Panel", icon="🛠️")
deposit_pg = st.Page("pages/6_Deposit.py", title="Deposit Funds", icon="📥")
withdraw_pg = st.Page("pages/7_withdraw.py", title="withdraw Money", icon="📤")
refer_pg = st.Page("pages/8_Refer.py", title="Refer & Earn", icon="👥")
# নতুন প্যাকেজ পেজটি এখানে যুক্ত করা হলো
packages_pg = st.Page("pages/9_Packages.py", title="Stable Earn", icon="💎")

# সেশন স্টেটে পেজগুলো সেভ করে রাখা হচ্ছে যাতে অন্য পেজ থেকে অ্যাক্সেস করা যায়
st.session_state.pages = {
    "dashboard": dashboard_pg,
    "deposit": deposit_pg,
    "withdraw": withdraw_pg,
    "game": game_pg,
    "refer": refer_pg,
    "register": register_pg,
    "login": login_pg,
    "packages": packages_pg # এখানেও যুক্ত করা হলো

}

if st.session_state.user is None:
    pg = st.navigation([register_pg, login_pg])
else:
    # এখানে packages_pg যুক্ত করা হয়েছে যাতে লগইন করার পর এটি সাইডবারে দেখা যায়
    pages_list = [dashboard_pg, packages_pg, game_pg, deposit_pg, withdraw_pg, refer_pg]
    if st.session_state.user == "omi529061@gmail.com":
        pages_list.append(admin_pg)
    pg = st.navigation(pages_list)

# --- SAFE NAVIGATION LOGIC (NOT CHANGING ANYTHING ABOVE) ---
# এটি নিশ্চিত করবে যে switch_page কল করলে সঠিক ফোল্ডার পাথ পায়
if "register_clicked" in st.session_state and st.session_state.register_clicked:
    st.session_state.register_clicked = False
    st.switch_page("pages/1_Register.py")
# এটি নিশ্চিত করবে যে কোনো পেজ না পেলে সে সরাসরি রেজিস্ট্রেশন পেজে যাবে
try:
    pg.run()
except Exception:
    st.switch_page(register_pg)
pg.run()