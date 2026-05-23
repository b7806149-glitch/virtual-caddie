import streamlit as st
import pandas as pd
import numpy as np
import requests

# Set up wide screen view
st.set_page_config(page_title="Strategic Flight Command", layout="wide")

# High-end tactical glassmorphism theme styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(10, 25, 17, 0.70), rgba(4, 12, 8, 0.85)), 
                    url('https://images.unsplash.com/photo-1535131749006-b7f58c99034b?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(5, 15, 10, 0.96) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    label, p, h3, h4, h5, h6, span {
        color: #F1F5F9 !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
    }
    
    .tactical-card {
        background-color: rgba(12, 36, 22, 0.85);
        backdrop-filter: blur(12px);
        padding: 22px;
        border-radius: 12px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }

    .alert-card {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 14px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .safe-card {
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.4);
        padding: 14px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE PERSISTENT BAG STATE ---
if "bag_df" not in st.session_state:
    st.session_state.bag_df = pd.DataFrame({
        "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
        "Full Stock": [285, 260, 245, 215, 205, 195, 180, 170, 155, 125, 95, 80],
        "Base Dispersion (y)": [14, 12, 11, 9, 8, 8, 7, 6, 6, 5, 4, 3]
    })

# --- SIDEBAR CONFIGURATION (AUTOMATED CONDITIONS) ---
st.sidebar.header("System Environmental Sync")

course_lat = st.number_input("Latitude", value=39.678, format="%.4f")
course_lon = st.number_input("Longitude", value=-75.752, format="%.4f")

if "temp" not in st.session_state: st.session_state.temp = 75.0
if "w_speed" not in st.session_state: st.session_state.w_speed = 8.0
if "w_deg" not in st.session_state: st.session_state.w_deg = 180

if st.sidebar.button("Fetch Live Weather Data Connection", use_container_width=True):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={course_lat}&longitude={course_lon}&current=temperature_2m,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph"
        res = requests.get(url, timeout=4).json()
        st.session_state.temp = float(res["current"]["temperature_2m"])
        st.session_state.w_speed = float(res["current"]["wind_speed_10m"])
        st.session_state.w_deg = int(res["current"]["wind_direction_10m"])
        st.sidebar.success("Atmospheric grid synchronized!")
    except:
        st.sidebar.error("Grid connection failed. Using profile memory defaults.")

air_temp = st.sidebar.slider("Air Temperature (°F)", 30, 110, int(st.session_state.temp))
wind_speed = st.sidebar.slider("Wind Velocity (MPH)", 0, 40, int(st.session_state.w_speed))
wind_deg = st.sidebar.slider("Wind Vector Heading (°)", 0, 360, int(st.session_state.w_deg))

st.sidebar.markdown("---")
st.sidebar.subheader("Live Bag Configuration")
edited_bag = st.sidebar.data_editor(st.session_state.bag_df, hide_index=True, num_rows="fixed")
st.session_state.bag_df = edited_bag

# --- MATHEMATICAL VECTOR UTILITIES ---
temp_adj = -((float(air_temp) - 75.0) / 10.0) * 2.0

# --- MAIN INTERACTIVE STRATEGY INTERFACE ---
st.title("Strategic Design Command Center")
st.markdown("Shift parameters away from emotional desires to absolute statistical boundaries.")
st.markdown("---")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.subheader("1. Spatial Hazard Mapping")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        pin_dist = st.number_input("True Yardage to Pin (y)", min_value=1, max_value=600, value=152)
        target_line_heading = st.slider("Target Line Path Heading (°)", 0, 360, value=0, step=5)
    with col_s2:
        pin_location = st.selectbox("Pin Location Pattern", ["Middle", "Tucked Front", "Tucked Back Left", "Tucked Back Right"])
        hazard_type = st.selectbox("Closest Severe Penalty Danger", ["None", "Front Bunker / False Front", "Back Water Hazard", "Right Out of Bounds", "Left Penalty Stake"])

    elevation_ft = st.number_input("Slope Change (Feet: +Uphill / -Downhill)", value=6)
    slope_adj = float(elevation_ft) / 3.0
    
    # Resolve Wind Intersect Vectors
    diff_deg = (wind_deg - target_line_heading) % 360
    if 45 <= diff_deg < 135: relation = "Crosswind (L to R)"
    elif 135 <= diff_deg < 225: relation = "Straight Downwind"
    elif 225 <= diff_deg < 315: relation = "Crosswind (R to L)"
    else: relation = "Straight Into"
    
    st.markdown(f"**Calculated Atmospheric Vector Cross:** {relation} @ {wind_speed} MPH")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- EXPECTED DESIRED MISS MATRIX LOGIC ---
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.subheader("2. Statistical Play Plan Selector")
    
    strategy_profile = st.radio(
        "Target Preference Engine",
        ["Center-Mass Safety (Maximize Green-In-Regulation Probability)", 
         "Aggressive Fire (Hunting Pin, Accepting High Penalty Exposure)", 
         "Defensive Hedge (Aiming Safely Away From Mapped Danger Zone)"],
        index=0
    )
    
    # Structural Adjustment Factors based on choice
    aim_shift = 0.0
    if "Center-Mass" in strategy_profile:
        if "Front" in pin_location: aim_shift = +4.0  # Force ball deeper into green body
        elif "Back" in pin_location: aim_shift = -4.0 # Pull back safely from rear collars
    elif "Defensive Hedge" in strategy_profile:
        if "Front" in pin_location: aim_shift = +7.0
        if "Back" in pin_location: aim_shift = -6.0

    working_target = float(pin_dist) + aim_shift
    final_play_as_target = working_target + temp_adj + slope_adj
    
    st.markdown("---")
    st.markdown(f"### Target Aiming Baseline: **{working_target:.1f} Yards**")
    st.markdown(f"### True Environmental Play-As: **{final_play_as_target:.1f} Yards**")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.subheader("3. Probability Optimization Matrix")
    st.markdown("<small>Your mathematical dispersion pattern applied down directly through your active bag settings:</small>", unsafe_allow_html=True)
    
    scored_options = []
    for index, row in edited_bag.iterrows():
        club = row["Club"]
        stock = float(row["Full Stock"])
        disp = float(row["Base Dispersion (y)"])
        
        # Apply aerodynamic multipliers
        aero = 1.3 if any(w in club for w in ["Wedge", "9-iron", "8-iron"]) else (0.85 if any(g in club for g in ["Driver", "3-Wood", "Hybrid"]) else 1.0)
        
        wind_penalty = 0.0
        if "Straight Into" in relation: wind_penalty = float(wind_speed) * 1.30 * aero
        elif "Straight Downwind" in relation: wind_penalty = -float(wind_speed) * 0.60 * (1 / aero)
        
        for shot_mode, mult in [("Full", 1.0), ("Grip Down", 0.95), ("3/4 Swing", 0.85)]:
            calculated_carry = (stock * mult) - wind_penalty + (-temp_adj)
            variance_diff = calculated_carry - final_play_as_target
            
            # Save all options that fall near our zone matrix
            if abs(variance_diff) <= (disp + 6.0):
                scored_options.append({
                    "Club": club,
                    "Swing": shot_mode,
                    "Carry": round(calculated_carry, 1),
                    "Diff": variance_diff,
                    "Dispersion": disp
                })

    # Sort choices by how accurately they match the calculated target line
    scored_options.sort(key=lambda x: abs(x["Diff"]))
    
    if scored_options:
        best = scored_options[0]
        # Calculate Expected Miss Metrics
        short_miss = best["Carry"] - (best["Dispersion"] / 2.0)
        long_miss = best["Carry"] + (best["Dispersion"] / 2.0)
        
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03); padding:16px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);'>
            <h4>Optimal Tactical Selection: <b style='color:#34D399;'>{best["Club"]} ({best["Swing"]})</b></h4>
            Expected True Delivery: <b>{best["Carry"]:.1f} Yards</b><br>
            Current Target Distance Window: <b>{final_play_as_target:.1f} Yards</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
        st.markdown("##### Predicted Outcome Boundary Windows (Expected Desired Misses):")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.02); padding:10px; border-radius:6px; border-left:4px solid #60A5FA;'>
                <small><b>Predicted Short Miss Limit</b></small><br>
                Carry: <b>{short_miss:.1f}y</b><br>
                Result vs Pin: <b>{short_miss - pin_dist:+.1f}y</b>
            </div>
            """, unsafe_allow_html=True)
        with col_p2:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.02); padding:10px; border-radius:6px; border-left:4px solid #F43F5E;'>
                <small><b>Predicted Long Miss Limit</b></small><br>
                Carry: <b>{long_miss:.1f}y</b><br>
                Result vs Pin: <b>{long_miss - pin_dist:+.1f}y</b>
            </div>
            """, unsafe_allow_html=True)
            
        # --- AUTOMATED DECISION TREE SAFETY RISK CHECKER ---
        st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
        st.markdown("##### Threat Assessment Assessment & Correction Guidance:")
        
        threat_triggered = False
        remedy_text = ""
        
        if hazard_type == "Front Bunker / False Front" and (short_miss - pin_dist) < -2.0:
            threat_triggered = True
            remedy_text = "Your calculated short-miss dispersion boundary drops directly into the front bunker complex. **Correction:** Abandon pin-hunting trajectory. Shift profile selection to Defensive Hedge or scale up club choices to establish backend green containment."
        elif hazard_type == "Back Water Hazard" and (long_miss - pin_dist) > 3.0:
            threat_triggered = True
            remedy_text = "Your predicted long-miss pattern breaches the back boundary into water hazard territory. **Correction:** Immediately step down club model strength. Drop into a controlled 3/4 swing utility profile to force your entire dispersion pattern short of the green collar line."
        elif "Left" in hazard_type or "Right" in hazard_type:
            threat_triggered = True
            remedy_text = f"Lateral hazard boundary ({hazard_type}) identified near landing window. Ensure target line tracking offset emphasizes center-green alignments exclusively to offset basic wind drift offsets."

        if threat_triggered:
            st.markdown(f"<div class='alert-card'>⚠️ <b>HIGH EXPOSURE RISK DETECTED:</b><br><small>{remedy_text}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='safe-card'>✅ <b>DISPERSION CONTAINED:</b><br><small>Your complete predictive miss window (both short and long errors) sits comfortably inside the safety limits of the green design framework.</small></div>", unsafe_allow_html=True)
            
    else:
        st.markdown("<span style='color:#FCA5A5;'>*No options matched mathematical safety windows. Check baseline data configs.*</span>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("##### Alternative Backups In Range:")
    for opt in scored_options[1:4]:
        st.markdown(f"• {opt['Club']} ({opt['Swing']}) — Carry: **{opt['Carry']:.1f}y** | Range Error: {opt['Diff']:+.1f}y")
        
    st.markdown("</div>", unsafe_allow_html=True)
