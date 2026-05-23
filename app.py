import streamlit as st
import pandas as pd
import numpy as np
import requests  # Built-in library to ping the Open-Meteo endpoint directly

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie Pro", layout="wide")

# Premium glassmorphism layout theme styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(4, 18, 10, 0.65), rgba(8, 24, 14, 0.75)), 
                    url('https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        width: 100vw;
        height: 100vh;
        color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(6, 20, 12, 0.95) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    label, p, h3, h4, h5, h6 {
        color: #F1F5F9 !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.85);
    }
    
    .dashboard-panel {
        background-color: rgba(10, 28, 16, 0.85);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(54, 113, 79, 0.35);
        box-shadow: 0 14px 32px -6px rgba(0, 0, 0, 0.75);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px;
        border-radius: 8px;
        text-align: center;
    }

    .stDataFrame {
        background-color: rgba(6, 18, 11, 0.8);
        border-radius: 10px;
        padding: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA PERSISTENCE INITIALIZATION ---
if "bag_df" not in st.session_state:
    default_bag = {
        "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
        "Full Stock": [285, 260, 245, 215, 205, 195, 180, 170, 155, 125, 95, 80],
        "Base Dispersion (y)": [14, 12, 11, 9, 8, 8, 7, 6, 6, 5, 4, 3]
    }
    st.session_state.bag_df = pd.DataFrame(default_bag)

st.title("Virtual Personal Caddie Pro")
st.markdown("Advanced environmental vectoring and safety dispersion matrixing.")
st.markdown("---")

# --- 1. SIDEBAR CONFIGURATION (WEATHER API & BAG CONTROLS) ---
st.sidebar.header("Pre-Round & Weather Synchronization")

# Native GPS Coordinate entry fields for custom golf course tracking
st.sidebar.markdown("##### GPS Coordinates (Course Location)")
col_lat, col_lon = st.sidebar.columns(2)
with col_lat:
    # Defaults to general university area coordinates as a stable baseline
    course_lat = st.number_input("Latitude", value=39.678, format="%.4f")
with col_lon:
    course_lon = st.number_input("Longitude", value=-75.752, format="%.4f")

# Initialize default manually fallback numbers in state if API isn't triggered
if "live_temp" not in st.session_state:
    st.session_state.live_temp = 75.0
if "live_wind_speed" not in st.session_state:
    st.session_state.live_wind_speed = 10.0
if "live_wind_deg" not in st.session_state:
    st.session_state.live_wind_deg = 0

if st.sidebar.button("Fetch Live Course Weather", use_container_width=True):
    try:
        # Pinging Open-Meteo's completely public developer api framework
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={course_lat}&longitude={course_lon}&current=temperature_2m,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph"
        response = requests.get(api_url, timeout=5).json()
        
        # Parse data variables straight down into operational session states
        st.session_state.live_temp = float(response["current"]["temperature_2m"])
        st.session_state.live_wind_speed = float(response["current"]["wind_speed_10m"])
        st.session_state.live_wind_deg = int(response["current"]["wind_direction_10m"])
        st.sidebar.success("Weather metrics updated live!")
    except Exception as e:
        st.sidebar.error("Could not reach weather grid. Falling back to manual dials.")

# Dials display either the parsed API values or manual overrides smoothly
air_temp = st.sidebar.slider("Air Temp (°F)", 30, 110, value=int(st.session_state.live_temp), step=1)
live_wind_mph = st.sidebar.slider("Wind Velocity (MPH)", 0, 40, value=int(st.session_state.live_wind_speed), step=1)
wind_direction_heading = st.sidebar.slider("Wind Source Bearing Angle (°)", 0, 360, value=int(st.session_state.live_wind_deg), step=5)

st.sidebar.markdown("---")
if st.sidebar.button("Reset Bag Defaults"):
    del st.session_state.bag_df
    st.rerun()

st.sidebar.subheader("Live Active Bag Profile")
edited_df = st.sidebar.data_editor(st.session_state.bag_df, hide_index=True, num_rows="fixed", key="persistent_data_editor")
st.session_state.bag_df = edited_df

# --- 2. MAIN DASHBOARD PANELS ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Live Shot Setup")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        live_dist = st.number_input("Target Distance to Pin (y)", min_value=1, max_value=600, value=165)
    with col_d2:
        pin_position = st.selectbox("Pin Placement Zone", ["Middle", "Front", "Back"])
        
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        elevation_ft = st.number_input("Elevation Change (Feet: +Uphill / -Downhill)", value=0)
    with col_e2:
        ball_lie = st.selectbox("Ball Lie Condition", ["Fairway", "Flyer Rough (+5% Dist, -Spin)", "Heavy Rough (-10% Dist)", "Fairway Bunker (-5% Dist)"])
    
    # CALCULATE SHOT RELATIVE DIRECTION VECTOR VIA TARGET HEADING vs WIND ANGLE
    st.markdown("##### Target Line Heading Vector Alignment")
    target_heading = st.slider("Target Line Heading Direction (°)", 0, 360, value=0, step=5, help="Direction you are hitting toward. 0° is North, 90° East, etc.")

    # Calculate net angle difference to find relative heading vector (Headwind vs Tailwind)
    angle_diff = (wind_direction_heading - target_heading) % 360
    
    # Mathematical classification maps degrees directly to flight impact zones
    if 45 <= angle_diff < 135:
        shot_wind_relation = "Crosswind (Left to Right)"
    elif 135 <= angle_diff < 225:
        shot_wind_relation = "Straight Downwind"
    elif 225 <= angle_diff < 315:
        shot_wind_relation = "Crosswind (Right to Left)"
    else:
        shot_wind_relation = "Straight Into"

    st.markdown(f"Mapped Relative Vector Path: **{shot_wind_relation}**")

    # Global Environmental Baseline Calculations
    temp_variance = float(air_temp) - 75.0
    temp_adjustment = -(temp_variance / 10.0) * 2.0
    elevation_adjustment = float(elevation_ft) / 3.0
    
    base_play_as = float(live_dist) + temp_adjustment + elevation_adjustment
    
    st.markdown("---")
    st.markdown(f"### Play-As Target Base: **{base_play_as:.1f} Yards**")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"<div class='metric-card'><small>Air Temp (Live)</small><br><b>{air_temp}°F</b></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-card'><small>Wind (Live)</small><br><b>{live_wind_mph} MPH</b></div>", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"<div class='metric-card'><small>Wind Angle</small><br><b>{wind_direction_heading}°</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- INTERACTIVE TEE SHOT OPTIMIZER ---
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Tee Shot Strategy & Risk Assessment")
    
    hole_length = st.number_input("Total Hole Length (y)", min_value=50, max_value=650, value=424)
    club_options = edited_df["Club"].tolist()
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        tee_club_1 = st.selectbox("Aggressive / Primary Option", club_options, index=0)
    with col_sel2:
        tee_club_2 = st.selectbox("Conservative / Layback Option", club_options, index=2)

    def get_tee_shot_data(club_name, bag_data):
        try:
            row = bag_data[bag_data["Club"] == club_name].iloc[0]
            stock = float(row["Full Stock"])
            disp = float(row["Base Dispersion (y)"])
        except IndexError:
            return 0.0, 0.0, 0.0
            
        aero = 0.85 if any(g in club_name for g in ["Driver", "3-Wood", "Hybrid"]) else 1.0
        wind_adj = 0.0
        if "Straight Into" in shot_wind_relation:
            wind_adj = float(live_wind_mph) * 1.30 * aero
        elif "Straight Downwind" in shot_wind_relation:
            wind_adj = -float(live_wind_mph) * 0.60 * (1 / aero)
            
        expected_carry = stock - wind_adj + (-temp_adjustment)
        remaining = max(0.0, float(hole_length) - expected_carry)
        return expected_carry, remaining, disp

    carry_1, rem_1, disp_1 = get_tee_shot_data(tee_club_1, edited_df)
    carry_2, rem_2, disp_2 = get_tee_shot_data(tee_club_2, edited_df)
    gained_yards = carry_1 - carry_2

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""
        <div style='background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2); padding:12px; border-radius:8px;'>
            <b style='color:#FCA5A5;'>Option A: {tee_club_1}</b><br>
            Est. Carry: <b>{carry_1:.1f}y</b><br>
            Approach Left: <b style='color:#FCA5A5;'>{rem_1:.1f}y</b><br>
            Lateral Error Risk: <b>±{disp_1}y</b>
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown(f"""
        <div style='background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.2); padding:12px; border-radius:8px;'>
            <b style='color:#86EFAC;'>Option B: {tee_club_2}</b><br>
            Est. Carry: <b>{carry_2:.1f}y</b><br>
            Approach Left: <b style='color:#86EFAC;'>{rem_2:.1f}y</b><br>
            Lateral Error Risk: <b>±{disp_2}y</b>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    
    if rem_1 < 40 and rem_1 > 5:
        st.markdown(f"💡 **Strategic Advisory:** **{tee_club_2} is heavily favored.** Hitting {tee_club_1} leaves an awkward partial wedge distance of {rem_1:.1f}y.")
    elif abs(gained_yards) < 12:
        st.markdown(f"💡 **Strategic Advisory:** **Take the shorter option ({tee_club_2}).** The calculated distance gap between these clubs is compressed to just {abs(gained_yards):.1f} yards.")
    elif rem_2 > 200 and rem_1 <= 170:
        st.markdown(f"🔥 **Strategic Advisory:** **{tee_club_1} is highly viable.** Laying back leaves a grueling long-iron approach of {rem_2:.1f}y.")
    else:
        st.markdown(f"⚖️ **Strategic Advisory:** **Balanced Choice.** {tee_club_1} leaves a shorter look but features a wider dispersion pattern.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Calculated Strategic Matrix")

    matrix_data = []
    for index, row in edited_df.iterrows():
        club = row['Club']
        stock_val = float(row['Full Stock'])
        base_dispersion = float(row['Base Dispersion (y)'])
        
        aero_mult = 1.3 if any(w in club for w in ["Wedge", "9-iron", "8-iron"]) else (0.85 if any(g in club for g in ["Driver", "3-Wood", "Hybrid"]) else 1.0)
            
        club_wind_adj = 0.0
        if "Straight Into" in shot_wind_relation:
            club_wind_adj = float(live_wind_mph) * 1.30 * aero_mult
        elif "Straight Downwind" in shot_wind_relation:
            club_wind_adj = float(live_wind_mph) * -0.60 * (1 / aero_mult)
        elif "Crosswind" in shot_wind_relation:
            club_wind_adj = float(live_wind_mph) * 0.15 * aero_mult

        lie_dist_mod = 1.0
        dispersion_mod = 1.0
        if "Flyer" in ball_lie:
            lie_dist_mod = 1.05; dispersion_mod = 1.4
        elif "Heavy" in ball_lie:
            lie_dist_mod = 0.90; dispersion_mod = 1.6
        elif "Bunker" in ball_lie:
            lie_dist_mod = 0.95; dispersion_mod = 1.2
            
        final_stock = (stock_val * lie_dist_mod) - club_wind_adj
        final_grip = ((stock_val * 0.95) * lie_dist_mod) - club_wind_adj
        final_three_quarter = ((stock_val * 0.85) * lie_dist_mod) - club_wind_adj
        final_dispersion = base_dispersion * dispersion_mod
        
        matrix_data.append({
            "Club": club,
            "Full Stock": round(final_stock, 1),
            "Grip Down": round(final_grip, 1),
            "3/4 Swing": round(final_three_quarter, 1),
            "Current Dispersion": round(final_dispersion, 1)
        })
        
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix.drop(columns=["Current Dispersion"]), use_container_width=True, hide_index=True)
    
    st.markdown("##### Safest Strategic Matches (Factoring Pin Protection & Ball Dispersion):")
    matches = []
    for item in matrix_data:
        for mode in ["Full Stock", "Grip Down", "3/4 Swing"]:
            calculated_carry = item[mode]
            diff = calculated_carry - float(live_dist)
            abs_diff = abs(diff)
            disp = item["Current Dispersion"]
            
            if abs_diff <= (disp + 4.0):
                if pin_position == "Front" and (diff - (disp / 2.0)) < -3.0:
                    continue
                elif pin_position == "Back" and (diff + (disp / 2.0)) > 3.0:
                    continue
                matches.append((abs_diff, diff, item["Club"], mode, calculated_carry, disp))
                
    matches.sort(key=lambda x: x[0])
    if matches:
        for abs_diff, raw_diff, club_name, shot_type, final_yards, current_disp in matches[:3]:
            direction_label = "long" if raw_diff > 0 else "short"
            st.markdown(f"• **{club_name}** ({shot_type}) — Expected Flight: **{final_yards:.1f}y** <br>&nbsp;&nbsp;<small style='color:#A1A1AA;'>Pin Miss: {abs(raw_diff):.1f}y {direction_label} | Standard Shot Dispersion Range: ±{current_disp/2:.1f}y</small>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#FCA5A5;'>*No high-safety matches found with current configurations.*</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
