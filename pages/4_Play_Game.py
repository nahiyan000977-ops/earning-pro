import streamlit as st
import json
import os
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Earning Pro AI | Elite Edition", layout="wide")

# --- ROYAL PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    header {visibility: hidden;} 

    /* Luxury Dark Background */
    .stApp { 
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%); 
        color: #ffffff; 
    }

    /* Elite Title Styling */
    .elite-title {
        font-family: 'Goldman', cursive;
        font-size: 55px;
        text-align: center;
        background: linear-gradient(180deg, #ffd700 0%, #b8860b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -30px;
        filter: drop-shadow(0 0 10px rgba(184, 134, 11, 0.5));
    }

    /* Wallet Shield */
    .wallet-shield {
        background: linear-gradient(145deg, #1e1e1e, #111111);
        border: 2px solid #b8860b;
        border-radius: 50px;
        padding: 10px 40px;
        display: inline-block;
        box-shadow: 0 0 20px rgba(184, 134, 11, 0.2);
        margin-bottom: 30px;
    }

    /* Main Gaming Console */
    .gaming-console {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 40px;
        padding: 50px;
        box-shadow: inset 0 0 50px rgba(0,0,0,1), 0 20px 40px rgba(0,0,0,0.8);
        position: relative;
        overflow: hidden;
    }

    /* Golden 3D Spin Button */
    div.stButton > button {
        background: linear-gradient(180deg, #ffd700 0%, #8b6508 100%) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 800 !important;
        font-family: 'Goldman' !important;
        height: 85px !important;
        font-size: 28px !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        box-shadow: 0 10px 0 #5e4304, 0 15px 30px rgba(184, 134, 11, 0.4) !important;
        transition: 0.1s !important;
    }
    div.stButton > button:active {
        transform: translateY(5px) !important;
        box-shadow: 0 5px 0 #5e4304 !important;
    }
    div.stButton > button:hover {
        filter: brightness(1.2);
    }

    /* Input Box Customization */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: rgba(0,0,0,0.5) !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }

    .live-chip {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        border: 1px solid #10b981;
    }
    </style>
    """, unsafe_allow_html=True)


# --- DATA ---
def load_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as f: return json.load(f)
    return {"balances": {}, "wagering_target": {}, "game_logs": []}


def save_data(data):
    with open("user_data.json", "w") as f: json.dump(data, f, indent=4)


user_email = st.session_state.get("user")
if not user_email:
    st.error("Access Denied!")
    st.stop()

if "active_game" not in st.session_state:
    st.session_state.active_game = None

# --- LOBBY (Compact Slots) ---
if st.session_state.active_game is None:
    st.markdown("<h1 class='elite-title'>ELITE LOBBY</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            '<div style="background:rgba(255,215,0,0.05); padding:20px; border-radius:20px; text-align:center; border:1px solid #b8860b;">🎰<br><b>Mega Spin AI</b></div>',
            unsafe_allow_html=True)
        if st.button("OPEN", key="play_mega"):
            st.session_state.active_game = "mega_spin"
            st.rerun()

# --- THE ELITE GAME INTERFACE ---
elif st.session_state.active_game == "mega_spin":
    data = load_data()
    balance = data.get("balances", {}).get(user_email, 0.0)
    wagering = data.get("wagering_target", {}).get(user_email, 0.0)

    # Back & Status
    b_col, s_col = st.columns([1, 4])
    with b_col:
        if st.button("◀ EXIT", key="exit_btn"):
            st.session_state.active_game = None
            st.rerun()
    with s_col:
        st.markdown("<div style='text-align:right'><span class='live-chip'>● SERVER LIVE</span></div>",
                    unsafe_allow_html=True)

    # Center Display
    st.markdown("<h1 class='elite-title'>MEGA SPIN AI</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center;">
            <div class="wallet-shield">
                <span style="color: #ffd700; font-size: 12px; letter-spacing: 2px;">SECURE PLAYER WALLET</span><br>
                <span style="font-size: 32px; font-weight: 700; color: #fff;">৳ {balance:,.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Console
    st.markdown('<div class="gaming-console">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p style='color:#ffd700; font-size:14px; font-weight:600;'>SELECT YOUR STAKE</p>",
                    unsafe_allow_html=True)
        bet_amount = st.number_input("", min_value=20.0, max_value=10000.0, value=20.0, label_visibility="collapsed")

    with c2:
        st.markdown("<p style='color:#ffd700; font-size:14px; font-weight:600;'>MULTIPLIER LEVEL</p>",
                    unsafe_allow_html=True)
        odd_choice = st.selectbox("", ["Low Risk (1:0.5x)", "Medium Risk (1:1x)", "High Risk (1:2x)",
                                       "Jackpot Mode (1:5x)"], label_visibility="collapsed")

    odds_config = {"Low Risk (1:0.5x)": {"multiplier": 0.5, "chance": 80},
                   "Medium Risk (1:1x)": {"multiplier": 1.0, "chance": 48},
                   "High Risk (1:2x)": {"multiplier": 2.0, "chance": 30},
                   "Jackpot Mode (1:5x)": {"multiplier": 5.0, "chance": 13}}
    selected = odds_config[odd_choice]

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💎 SPIN TO WIN 💎", use_container_width=True):
        if balance < bet_amount:
            st.error("Insufficient Balance!")
        else:
            # --- NEW PROFESSIONAL SLOT ANIMATION ---
            slot_placeholder = st.empty()
            symbols = ["🍒", "💎", "🎰", "🔔", "🍋", "⭐", "💰", "🔥"]

            # Spinning Loop
            for _ in range(25):
                s1, s2, s3 = random.sample(symbols, 3)
                slot_placeholder.markdown(f"""
                    <div style="display: flex; justify-content: center; gap: 20px; font-size: 65px; 
                                background: rgba(0,0,0,0.4); padding: 25px; border-radius: 25px; 
                                border: 2px solid #ffd700; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255,215,0,0.2);">
                        <span>{s1}</span> <span>{s2}</span> <span>{s3}</span>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(0.08)

            # Logic (Unchanged)
            win_roll = random.randint(1, 100)
            is_win = win_roll <= selected["chance"]
            data["wagering_target"][user_email] = max(0.0, wagering - bet_amount)

            # Show Final Result Symbols
            final_icon = "🎰" if is_win else "💀"
            slot_placeholder.markdown(f"""
                <div style="display: flex; justify-content: center; font-size: 80px; 
                            background: rgba(0,0,0,0.6); padding: 25px; border-radius: 25px; 
                            border: 3px solid {'#10b981' if is_win else '#ef4444'}; margin-bottom: 25px;">
                    <span>{final_icon}</span>
                </div>
            """, unsafe_allow_html=True)

            if is_win:
                profit = bet_amount * selected["multiplier"]
                data["balances"][user_email] = balance + profit
                st.balloons()
                st.markdown(
                    f"<div style='background:rgba(16,185,129,0.2); padding:20px; border-radius:15px; border:1px solid #10b981; text-align:center; font-size:24px; color:#10b981;'>🏆 WINNER: ৳ {profit:,.2f}</div>",
                    unsafe_allow_html=True)
            else:
                data["balances"][user_email] = balance - bet_amount
                st.markdown(
                    f"<div style='background:rgba(239,68,68,0.2); padding:20px; border-radius:15px; border:1px solid #ef4444; text-align:center; font-size:24px; color:#ef4444;'>💀 LOST: ৳ {bet_amount:,.2f}</div>",
                    unsafe_allow_html=True)

            # Save logs (Unchanged)
            new_log = {"user": user_email[:4] + "***", "bet": bet_amount, "mode": odd_choice.split(" ")[0],
                       "res": "Win" if is_win else "Loss", "time": time.strftime("%H:%M:%S")}
            if "game_logs" not in data: data["game_logs"] = []
            data["game_logs"].insert(0, new_log)
            save_data(data)
            time.sleep(2)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # History Table (Updated to show last 10 logs)
    st.markdown("<br><p style='color:#ffd700; font-weight:700;'>🛰️ GLOBAL WINNER LOG (LAST 10)</p>", unsafe_allow_html=True)
    for log in data.get("game_logs", [])[:10]:
        res_col = "#10b981" if log["res"] == "Win" else "#ef4444"
        st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02); padding:12px; border-radius:12px; margin-bottom:5px; border-left:4px solid {res_col}; display:flex; justify-content:space-between;">
                <span>👤 {log['user']}</span>
                <span>💰 ৳{log['bet']}</span>
                <span style="color:{res_col}; font-weight:700;">{log['res']}</span>
            </div>
        """, unsafe_allow_html=True)