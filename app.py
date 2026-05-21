import streamlit as st
import pandas as pd
import numpy as np

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie", page_icon="⛳", layout="wide")

# Custom CSS injection for an elite, modern Fairway/Golf Course theme
st.markdown("""
    <style>
    /* Main App Background - Smooth Grass/Fairway Gradient */
    .stApp {
        background: linear-gradient(135deg, #0B2516 0%, #133A22 50%, #1B4D32 100%);
        color: #F8FAFC;
    }
    
    /* Sidebar styling adjustment for contrast */
    [data-testid="stSidebar"] {
        background-color: #081C10 !important;
    }
    
    /* Metric blocks mimicking a premium launch monitor layout */
    .metric-container {
        background-color: rgba(15, 34, 23, 0.75);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2B5B3F;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* Tier 1: Recommended Stock Choice (Rich Emerald) */
    .main-rec {
        background-color: #1B4D32;
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #22C55E;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    /* Tier 2: Flighted Alternative (Warm Gold/Sand) */
    .control-rec {
        background-color: #78350F;
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #EAB308;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    /* Advisory Warning (Deep Redish Brown for Danger/Alert) */
    .advisory-box {
        background-color: #4C1D1D;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #7F1D1D;
        margin-bottom: 15px;
    }
    
    /* History card entries */
    .history-card {
        background-color: rgba(8, 28, 16, 0.6);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #234E35;
        margin-bottom: 10px;
    }
    
    /* Make standard text input and labels pop against dark green background */
    label, p, h3, h5 {
        color: #F1F5F9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Clean, professional typography with the emoji logo completely removed
st.title("Virtual Personal Caddie")
st.markdown("Your data-driven strategic partner on the course. Adjust your stock yardages and conditions live.")
st.markdown("---")

# --- 1. HARDCODED HISTORICAL ROUND DATA ---
historical_shots = [
    {"hole": 1, "dist_range": "200-220", "club": "4-iron", "shape": "Right", "note": "4 iron heel blade right trying to punch"},
    {"hole": 3, "dist_range": "140-160", "club": "Iron", "shape": "Right", "note": "Approach out of rough was a push and miss right"},
    {"hole": 4, "dist_range": "140-160", "club": "9-iron", "shape": "Right", "note": "Hit green but slightly short with a slight cut (153 yards)"},
    {"hole": 5, "dist_range": "70-90", "club": "54-deg Wedge", "shape": "Right", "note": "76 yard wedge shot slightly bladed"},
    {"hole": 6, "dist_range": "210-230", "club": "Hybrid", "shape": "Right", "note": "Good hybrid hit too far to the right into water"},
    {"hole": 7, "dist_range": "50-70", "club": "Wedge", "shape": "Right", "note": "Pushed wedge to the right by a lot (maybe 40 yards)"},
    {"hole": 8, "dist_range": "200-220", "club": "6-iron", "shape": "Right", "note": "High right 6-iron that hit green 50 feet away"},
    {"hole": 9, "dist_range": "90-110", "club": "Wedge", "shape": "Right", "note": "Blocked wedge shot that was into wind right and short"}
]
df_history = pd.DataFrame(historical_shots)

# --- 2. SIDEBAR CONFIGURATION ---
st.sidebar.header("⚙️ Pre-Round & Bag Setup")

global_wind_dir = st.sidebar.selectbox("Pre-Round Wind Baseline Direction", ["North", "South", "East", "West", "Variable"])
grip_down_pct = st.sidebar.slider("Grip Down Distance Reduction (%)", 1, 15, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Live Stock Bag Distances (Full Swings)")

default_bag = {
    "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
    "Full Hard": [275, 240, 220, 205, 195, 180, 168, 155, 142, 122, 105, 85],
    "Full Stock": [260, 230, 210, 195, 185, 170, 158, 145, 132, 112, 95, 75],
    "Full Light": [245, 215, 200, 185, 175, 160, 148, 135, 122, 102, 85, 65]
}
df_stock = pd.DataFrame(default_bag)
edited_df = st.sidebar.data_editor(df_stock, hide_index=True, num_rows="fixed")


# --- 3. MAIN DASHBOARD ---
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.subheader("🎯 Live Shot Setup")
    
    col_d, col_w_rel, col_w_mph = st.columns(3)
    with col_d:
        live_dist = st.number_input("Target Distance to Pin (Yards)", min_value=1, max_value=600, value=153)
    with col_w_rel:
        shot_wind_relation = st.selectbox("Wind Relation For Shot", ["None", "Straight Into", "Straight Downwind", "Crosswind"])
    with col_w_mph:
        live_wind_mph = st.slider("Wind Velocity (MPH)", 0, 40, 12)

    # Calculate Play-As Yardage
    wind_adjustment = 0.0
    if shot_wind_relation == 'Straight Into':
        wind_adjustment = float(live_wind_mph) * 1.0  
    elif shot_wind_relation == 'Straight Downwind':
        wind_adjustment = float(live_wind_mph) * -0.5 
        
    adjusted_distance = float(live_dist) + wind_adjustment

    # KPI Metrics Row
    st.markdown("<br>", unsafe_allow_html=True)
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"<div class='metric-container'><span style='color:#94A3B8; font-size:14px;'>PLAY-AS TARGET</span><br><span style='color:#22C55E; font-size:32px; font-weight:bold;'>{adjusted_distance:.1f}y</span></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<div class='metric-container'><span style='color:#94A3B8; font-size:14px;'>WIND DEFL</span><br><span style='color:#EAB308; font-size:32px; font-weight:bold;'>{wind_adjustment:+.1f}y</span></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<div class='metric-container'><span style='color:#94A3B8; font-size:14px;'>BASE SYSTEM</span><br><span style='color:#60A5FA; font-size:24px; font-weight:bold; line-height:40px;'>{global_wind_dir}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>### 📋 Personalized Strategic Options", unsafe_allow_html=True)

    # ALGORITHM ENGINE
    best_stock_club = None
    best_stock_mode = ""
    best_stock_dist = 999.0
    stock_diff = 999.0

    best_control_club = None
    best_control_mode = ""
    best_control_dist = 999.0
    control_diff = 999.0
    is_grip_down = False

    for index, row in edited_df.iterrows():
        club_name = row['Club']
        modes = {
            "Full Hard": float(row['Full Hard']),
            "Full Stock": float(row['Full Stock']),
            "Full Light": float(row['Full Light'])
        }
        
        for mode_name, base_yardage in modes.items():
            # Standard Full Options
            d_diff = abs(base_yardage - adjusted_distance)
            if d_diff < stock_diff and d_diff <= 8:
                stock_diff = d_diff
                best_stock_club = club_name
                best_stock_mode = mode_name
                best_stock_dist = base_yardage

            # 3/4 Swing Math Logic (Full Swing Value * 0.85)
            three_quarter_yardage = base_yardage * 0.85
            tq_diff = abs(three_quarter_yardage - adjusted_distance)
            if tq_diff < control_diff and tq_diff <= 8:
                control_diff = tq_diff
                best_control_club = club_name
                best_control_mode = f"3/4 {mode_name}"
                best_control_dist = three_quarter_yardage
                is_grip_down = False

            # 3/4 Swing + Grip Down Math Logic
            gd_three_quarter_yardage = three_quarter_yardage * (1 - (float(grip_down_pct) / 100))
            gd_diff = abs(gd_three_quarter_yardage - adjusted_distance)
            if gd_diff < control_diff and gd_diff <= 8:
                control_diff = gd_diff
                best_control_club = club_name
                best_control_mode = f"3/4 {mode_name}"
                best_control_dist = gd_three_quarter_yardage
                is_grip_down = True

    # Render Tier 1 HTML
    if best_stock_club:
        html_stock = f"<div class='main-rec'><span style='color:#A7F3D0; font-size:14px; font-weight:bold;'>🏆 TIER 1: RECOMMENDED STOCK CHOICE</span><br><span style='font-size:22px; font-weight:bold; color:white;'>Smooth {best_stock_club}</span><br><span style='color:#E2E8F0; font-size:15px;'>Execution Strategy: <b>{best_stock_mode} Swing</b> with normal grip setup. Carries roughly <b>{best_stock_dist:.1f} yards</b>.</span></div>"
        st.markdown(html_stock, unsafe_allow_html=True)
    else:
        st.warning("No standard stock match available. Check bag range layout bounds.")

    # Render Tier 2 HTML
    if best_control_club and best_control_club != best_stock_club:
        grip_instruction = "Grip Down" if is_grip_down else "Normal Grip"
        html_control = f"<div class='control-rec'><span style='color:#FDE68A; font-size:14px; font-weight:bold;'>💨 TIER 2: CONTROL / FLIGHTED ALTERNATIVE</span><br><span style='font-size:22px; font-weight:bold; color:white;'>Flighted {best_control_club}</span><br><span style='color:#E2E8F0; font-size:15px;'>Execution Strategy: <b>{grip_instruction}</b> using a <b>{best_control_mode}</b> profile. Expected flight limits travel <b>{best_control_dist:.1f} yards</b>.</span></div>"
        st.markdown(html_control, unsafe_allow_html=True)


with col_right:
    st.subheader("📊 Spatial Reality Check & History")
    
    # Track the distance band layout parameters
    if adjusted_distance <= 90:
        band, label = "70-90", "Short Wedges"
    elif adjusted_distance <= 115:
        band, label = "90-110", "Wedge Scoring Zone"
    elif adjusted_distance <= 165:
        band, label = "140-160", "Mid-Iron Targets"
    else:
        band, label = "200-220", "Long Range / Approach Flights"
        
    filtered_past = df_history[df_history['dist_range'] == band]
    
    # Calculate historical miss counts
    right_miss_count = len(filtered_past[filtered_past['shape'] == 'Right'])
    total_miss_tracked = len(filtered_past)
    
    if total_miss_tracked > 0:
        pct_right = (float(right_miss_count) / float(total_miss_tracked)) * 100.0
        
        # Render Advisory Block via safe string execution
        html_advisory = f"<div class='advisory-box'><span style='color:#FDBA74; font-size:13px; font-weight:bold;'>⚠️ CADDIE TENDENCY ADVISORY</span><br><span style='font-size:18px; font-weight:bold; color:white;'>{pct_right:.0f}% Miss Pattern to the RIGHT</span><br><p style='color:#FFEDD5; font-size:14px; margin-top:5px;'>Your data shows a historical block signature from this distance tier ({label}). Aim toward the left green safety margin and play for a natural bleed back.</p></div>"
        st.markdown(html_advisory, unsafe_allow_html=True)
        
        st.markdown("##### 🕒 Your Real Past Notes From This Range:")
        for _, raw_row in filtered_past.iterrows():
            html_card = f"<div class='history-card'><span style='color:#60A5FA; font-weight:bold; font-size:13px;'>Hole {raw_row['hole']} Shot Log:</span><br><span style='color:#E2E8F0; font-size:14px;'>\"{raw_row['note']}\"</span></div>"
            st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.info("Gathering calibration data footprint for this custom target layer.")
