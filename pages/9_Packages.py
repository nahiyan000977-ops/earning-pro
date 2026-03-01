import streamlit as st
import json
import os
import time
import random
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="VIP Packages | Stable Earn", layout="wide")

# --- ROYAL PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&family=Montserrat:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    header {visibility: hidden;} 
    .stApp { 
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%); 
        color: #ffffff; 
    }
    .pkg-card {
        background: linear-gradient(145deg, #1e1e1e, #111111);
        border: 1px solid rgba(184, 134, 11, 0.3);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .pkg-card:hover {
        transform: translateY(-10px);
        border-color: #ffd700;
        box-shadow: 0 15px 30px rgba(184, 134, 11, 0.2);
    }
    .pkg-title {
        font-family: 'Goldman', cursive;
        color: #ffd700;
        font-size: 22px;
        margin-bottom: 10px;
    }
    .reward-status {
        background: rgba(16, 185, 129, 0.1);
        border: 1px dashed #10b981;
        border-radius: 12px;
        padding: 10px;
        margin: 15px 0;
        color: #10b981;
        font-weight: 700;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        font-family: 'Goldman' !important;
        font-weight: 700 !important;
        transition: 0.3s !important;
        height: 45px !important;
    }
    button[key*="buy"] {
        background: linear-gradient(180deg, #ffd700 0%, #8b6508 100%) !important;
        color: black !important;
        border: none !important;
    }
    .pop-text { font-size: 14px; color: #e2e8f0; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)


# --- DATA HANDLING ---
def load_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as f: return json.load(f)
    return {"balances": {}, "active_packages": {}}


def save_data(data):
    with open("user_data.json", "w") as f: json.dump(data, f, indent=4)


# User Validation
user_email = st.session_state.get("user")
if not user_email:
    st.error("Access Denied! Please login from the Main Dashboard.")
    st.stop()

data = load_data()

# Ensure keys exist
if "active_packages" not in data: data["active_packages"] = {}
if user_email not in data["active_packages"]: data["active_packages"][user_email] = []

# --- NEW SESSION STATE FOR GAME ---
if "game_active" not in st.session_state: st.session_state.game_active = False
if "current_claim_idx" not in st.session_state: st.session_state.current_claim_idx = None

balance = data.get("balances", {}).get(user_email, 0.0)

# --- 🎮 GAME UI SECTION ---
if st.session_state.game_active:
    st.markdown("<h2 style='text-align:center; color:#ffd700; font-family:Goldman;'>🛡️ HUMAN VERIFICATION</h2>",
                unsafe_allow_html=True)
    st.info("Level 3 শেষ করে রিওয়ার্ড ক্লেইম করুন।")

    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body{ font-family:Arial; background:#000; text-align:center; color:white; }
        .flash{ background:red !important; }
        #gameArea{ width:100%; max-width:450px; height:320px; background:#111; margin:20px auto; position:relative; border-radius:15px; border:2px solid #ffd700; overflow:hidden; }
        .box{ width:50px; height:50px; background:#ffd700; position:absolute; cursor:pointer; display:none; border-radius:10px; box-shadow:0 0 15px #ffd700; }
        .btn-start{ padding:12px 25px; background:linear-gradient(180deg, #ffd700, #b8860b); color:black; border:none; border-radius:8px; cursor:pointer; font-weight:bold; }
    </style>
    </head>
    <body>
        <p>Level: <span id="level">1</span> | Score: <span id="score">0</span> | Boxes: <span id="boxes">0</span>/10</p>
        <button class="btn-start" onclick="startLevel()">START LEVEL</button>
        <div id="gameArea"><div class="box" id="box"></div></div>
        <script>
            let level = 1; let score = 0; let boxCount = 0; let maxBoxes = 10;
            let box = document.getElementById("box"); let boxVisible = false;
            let levelSpeed = { 1: 1300, 2: 1200, 3: 1000 };
            let levelTarget = { 1: 6, 2: 7, 3: 8 };

            function randomPosition(){
                let area = document.getElementById("gameArea");
                box.style.left = Math.random() * (area.clientWidth - 60) + "px";
                box.style.top = Math.random() * (area.clientHeight - 60) + "px";
            }
            function showNextBox(){
                if(boxCount >= maxBoxes){ finishLevel(); return; }
                randomPosition(); box.style.display = "block"; boxVisible = true; boxCount++;
                document.getElementById("boxes").innerText = boxCount;
                setTimeout(function(){
                    if(boxVisible){ score -= 1; document.body.classList.add("flash"); setTimeout(()=>{document.body.classList.remove("flash");},100); }
                    box.style.display = "none"; boxVisible = false;
                    document.getElementById("score").innerText = score;
                    showNextBox();
                }, levelSpeed[level]);
            }
            function startLevel(){ score = 0; boxCount = 0; showNextBox(); }
            function finishLevel(){
                if(score >= levelTarget[level]){
                    if(level < 3){ level++; alert("🔥 Level " + level + " Started!"); startLevel(); } 
                    else { alert("🏆 Success! Click VERIFY button below."); }
                } else { alert("❌ Failed! Try again."); }
            }
            box.onclick = function(){ if(boxVisible){ score++; boxVisible = false; box.style.display = "none"; document.getElementById("score").innerText = score; } };
        </script>
    </body>
    </html>
    """
    components.html(game_html, height=500)

    if st.button("✅ VERIFY & ADD REWARD"):
        idx = st.session_state.current_claim_idx
        # ডাটা সেভ করার আগে পজিশন চেক করা
        if idx is not None and idx < len(data["active_packages"][user_email]):
            pkg = data["active_packages"][user_email][idx]
            reward_amt = float(pkg.get('price', 0)) * 0.20

            data["active_packages"][user_email][idx]['reward_balance'] += reward_amt
            data["active_packages"][user_email][idx]['last_claim'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(data)

            st.session_state.game_active = False
            st.success("Reward Claimed Successfully!")
            time.sleep(1)
            st.rerun()

    if st.button("Cancel Challenge"):
        st.session_state.game_active = False
        st.rerun()

# --- MAIN PAGE LOGIC ---
else:
    st.markdown(
        "<h1 style='text-align:center; font-family:Goldman; color:#ffd700; margin-top:-40px;'>STABLE EARN PACKAGES</h1>",
        unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align:center; margin-bottom:40px;'>WALLET BALANCE: <span style='color:#ffd700; font-weight:bold; font-size:20px;'>৳ {balance:,.2f}</span></div>",
        unsafe_allow_html=True)

    # --- STORE SECTION ---
    if not st.session_state.get("show_active_assets", False):
        st.markdown("### 💎 Available Offers")
        shop_cols = st.columns(4)
        prices = [200, 500, 1000, 2000, 5000, 10000, 20000, 25000]

        for i, p_price in enumerate(prices):
            with shop_cols[i % 4]:
                st.markdown(f"""
                    <div class="pkg-card">
                        <div class="pkg-title">VIP {i + 1}</div>
                        <h2 style="margin:0;">৳ {p_price}</h2>
                        <p style="color:#94a3b8; font-size:12px; margin-top:5px;">Return: 20% Daily</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"REDEEM ৳{p_price}", key=f"buy_{p_price}_{i}"):
                    if balance >= p_price:
                        data["balances"][user_email] -= p_price
                        if "wagering_target" in data and user_email in data["wagering_target"]:
                            data["wagering_target"][user_email] = max(0.0,
                                                                      data["wagering_target"][user_email] - p_price)

                        new_entry = {
                            "price": p_price,
                            "reward_balance": 0.0,
                            "last_claim": "",  # None এর বদলে ফাঁকা স্ট্রিং রাখা ভালো
                            "id": random.randint(10000, 99999)
                        }
                        data["active_packages"][user_email].append(new_entry)
                        save_data(data)
                        st.toast(f"Package VIP {i + 1} Activated!", icon="✅")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Insufficient Balance!")

    # --- ACTIVE ASSETS SECTION ---
    if st.session_state.get("show_active_assets", False):
        st.markdown("### ⚡ Your Active Assets")
        if st.button("⬅️ Back to Store"):
            st.session_state.show_active_assets = False
            st.rerun()

        user_pkgs = data["active_packages"][user_email]
        if not user_pkgs:
            st.info("No active packages.")
        else:
            active_cols = st.columns(3)
            for idx, pkg in enumerate(user_pkgs):
                with active_cols[idx % 3]:
                    # Type safety for display
                    pkg_price = float(pkg.get('price', 0))
                    pkg_reward = float(pkg.get('reward_balance', 0))

                    st.markdown(f"""
                        <div class="pkg-card" style="border-left: 4px solid #ffd700;">
                            <p style="color:#94a3b8; font-size:11px; margin:0;">ACTIVE PACKAGE</p>
                            <div style="font-size:24px; font-weight:bold;">৳ {pkg_price:,.0f}</div>
                            <div class="reward-status"><small>Reward Balance</small><br>৳ {pkg_reward:.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    # --- FIXED 24H CLAIM LOGIC ---
                    can_claim = True
                    remaining_str = ""
                    last_claim_raw = pkg.get('last_claim', "")

                    if last_claim_raw and isinstance(last_claim_raw, str) and last_claim_raw != "":
                        try:
                            last_time = datetime.strptime(last_claim_raw, "%Y-%m-%d %H:%M:%S")
                            if datetime.now() < last_time + timedelta(hours=24):
                                can_claim = False
                                rem = (last_time + timedelta(hours=24)) - datetime.now()
                                remaining_str = str(rem).split('.')[0]
                        except ValueError:
                            can_claim = True  # ফরম্যাট ভুল হলে ক্লেইম করতে দাও

                    if st.button(f"📺 CLAIM REWARD (20%)", key=f"claim_{idx}"):
                        if can_claim:
                            st.session_state.game_active = True
                            st.session_state.current_claim_idx = idx
                            st.rerun()
                        else:
                            st.warning(f"Next claim in: {remaining_str}")

                    # Withdraw Logic
                    with st.popover("💰 WITHDRAW & RESET", use_container_width=True):
                        st.markdown("### ⚠️ Are you sure?")
                        st.markdown(
                            f'<p class="pop-text">Close <b>৳{pkg_price}</b> and transfer <b>৳{pkg_reward:.2f}</b> to wallet?</p>',
                            unsafe_allow_html=True)
                        if st.button("✅ YES, CONFIRM", key=f"wd_confirm_{idx}"):
                            if pkg_reward > 0:
                                data["balances"][user_email] += pkg_reward
                                data["active_packages"][user_email].pop(idx)
                                save_data(data)
                                st.success("Package Reset!")
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error("Empty reward!")