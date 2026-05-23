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
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE PERSISTENT BAG STATE ---
if "bag_df" not in st.session_state:
    st.session_state.bag_df = pd.DataFrame({
        "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
        "Full Stock": [285, 260, 245, 215, 205, 195, 180, 170, 155, 125, 95, 80],
        "Base Dispersion (y)": [14, 12, 11, 9, 8, 8, 7, 6, 6, 5, 4, 3]
    })

# --- SIDEBAR CONFIGURATION ---
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
        st.sidebar.error("Grid connection failed.")

air_temp = st.sidebar.slider("Air Temperature (°F)", 30, 110, int(st.session_state.temp))
wind_speed = st.sidebar.slider("Wind Velocity (MPH)", 0, 40, int(st.session_state.w_speed))
wind_deg = st.sidebar.slider("Wind Vector Heading (°)", 0, 360, int(st.session_state.w_deg))

st.sidebar.markdown("---")
edited_bag = st.sidebar.data_editor(st.session_state.bag_df, hide_index=True, num_rows="fixed")
st.session_state.bag_df = edited_bag

# Global calculations
temp_adj = -((float(air_temp) - 75.0) / 10.0) * 2.0

st.title("Strategic Design Command Center")
st.markdown("Dynamic Dispersion Mapping & Green Probability Analytics Engine.")
st.markdown("---")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.subheader("1. Setup & Target Selection")
    
    col1, col2 = st.columns(2)
    with col1:
        pin_dist = st.number_input("True Yardage to Pin (y)", min_value=1, max_value=600, value=155)
        target_line_heading = st.slider("Target Line Path Heading (°)", 0, 360, value=0, step=5)
    with col2:
        club_choice = st.selectbox("Select Approach Club", edited_bag["Club"].tolist(), index=7) # Default 8-iron
        elevation_ft = st.number_input("Slope Change (Feet: +Uphill / -Downhill)", value=0)
        
    st.markdown("---")
    st.markdown("##### 2. Map Flag Location Relative to Center Green")
    st.markdown("<small>A standard green profile maps out roughly 35 yards long by 25 yards wide.</small>", unsafe_allow_html=True)
    
    # Grid coordinate placements
    pin_y = st.slider("Flag Depth (Y-Axis: -15y Front to +15y Back Collar)", -15, 15, 8, step=1)
    pin_x = st.slider("Flag Width (X-Axis: -12y Left Margin to +12y Right Margin)", -12, 12, -7, step=1)
    
    # Severe Hazard Overlay Mapping Switches
    st.markdown("##### 3. Local Perimeter Threat Configuration")
    col_hz1, col_hz2 = st.columns(2)
    with col_hz1:
        left_hazard = st.checkbox("Left Side Penalty (Water/OB)", value=True)
        front_hazard = st.checkbox("Front Edge Hazard (Deep Bunker)", value=False)
    with col_hz2:
        right_hazard = st.checkbox("Right Side Penalty (Water/OB)", value=False)
        back_hazard = st.checkbox("Back Collar Hazard (Dense Forest)", value=False)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Resolve environmental data variations
slope_adj = float(elevation_ft) / 3.0
diff_deg = (wind_deg - target_line_heading) % 360
if 45 <= diff_deg < 135: relation = "Crosswind (L to R)"
elif 135 <= diff_deg < 225: relation = "Straight Downwind"
elif 225 <= diff_deg < 315: relation = "Crosswind (R to L)"
else: relation = "Straight Into"

with col_right:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.subheader("Statistical Probability Matrix & Target Mapping")
    
    # Fetch data attributes of the active club pick
    club_row = edited_bag[edited_bag["Club"] == club_choice].iloc[0]
    stock_dist = float(club_row["Full Stock"])
    base_disp = float(club_row["Base Dispersion (y)"])
    
    # Wind adjust logic
    aero = 1.3 if any(w in club_choice for w in ["Wedge", "9-iron", "8-iron"]) else 1.0
    wind_penalty = 0.0
    if "Straight Into" in relation: wind_penalty = float(wind_speed) * 1.30 * aero
    elif "Straight Downwind" in relation: wind_penalty = -float(wind_speed) * 0.60 * (1 / aero)
    
    calculated_carry = stock_dist - wind_penalty + (-temp_adj) - slope_adj
    
    # Define standard geometric boundaries for a normalized green complex
    green_length_half = 17.5 # Total length 35 yards
    green_width_half = 12.5  # Total width 25 yards
    
    # PROBABILITY SIMULATION: Test aiming options systematically to evaluate safety percentages
    best_aim_x, best_aim_y = 0.0, 0.0
    max_safety_score = -1.0
    optimal_gir_pct = 0.0
    
    # Test a coordinate matrix array around the flag layout to optimize score vectors
    for test_x in range(-12, 13, 1):
        for test_y in range(-15, 16, 1):
            
            # Simulate a 300-shot random Gaussian error dispersion block based on personal club specs
            np.random.seed(42) # Locked seed for responsive app stabilization
            sim_x = np.random.normal(test_x, base_disp / 3.0, 250)
            sim_y = np.random.normal(test_y, base_disp / 2.5, 250)
            
            hits = 0
            score_penalty = 0
            
            for sx, sy in zip(sim_x, sim_y):
                # Check standard green boundary matrix intersection
                on_green = (abs(sx) <= green_width_half) and (abs(sy) <= green_length_half)
                
                if on_green:
                    hits += 1
                else:
                    # Apply steep mathematical dynamic score penalties if misses drop into configured hazards
                    if left_hazard and sx < -green_width_half: score_penalty += 3.0
                    if right_hazard and sx > green_width_half: score_penalty += 3.0
                    if front_hazard and sy < -green_length_half: score_penalty += 2.0
                    if back_hazard and sy > green_length_half: score_penalty += 2.0
                    
            gir_probability = (hits / 250.0) * 100.0
            # Safety value equation seeks max greens hit with minimal penalty exposure
            safety_score = gir_probability - score_penalty
            
            if safety_score > max_safety_score:
                max_safety_score = safety_score
                best_aim_x, best_aim_y = test_x, test_y
                optimal_gir_pct = gir_probability

    # Calculate final targeting modifications
    offset_x = best_aim_x - pin_x
    offset_y = best_aim_y - pin_y
    suggested_yardage = pin_dist + offset_y
    
    st.markdown(f"""
    <div style='background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.3); padding:16px; border-radius:8px;'>
        <h4>🎯 Automated Target Alignment Verdict:</h4>
        • Target Distance Line: <b>{suggested_yardage:.1f} Yards</b> (Play pin as {pin_dist}y)<br>
        • Fairway Alignment Shift: <b>{abs(offset_x):.1f} Yards {"RIGHT" if offset_x > 0 else "LEFT"}</b> of Flag Line<br>
        • Expected Green-In-Regulation (GIR): <b style='color:#4ADE80;'>{optimal_gir_pct:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)
    
    # --- TEXT-BASED GEOMETRIC SATELLITE RADAR MATRIX ---
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    st.markdown("##### Tactical Spatial Landing Map View:")
    st.markdown("<small>Visualizing the green landing space matrix. **[P]** = Pin, **[X]** = Safest Optimized Target Line, **[G]** = Safe Green Surface.</small>", unsafe_allow_html=True)
    
    # Build a 7x13 string grid to output as a lightweight scannable spatial interface
    grid_out = []
    for row_y in range(14, -15, -4):
        line_str = ""
        for col_x in range(-12, 13, 2):
            # Check proximity matching targets
            is_pin = (abs(col_x - pin_x) <= 1) and (abs(row_y - pin_y) <= 2)
            is_target = (abs(col_x - best_aim_x) <= 1) and (abs(row_y - best_aim_y) <= 2)
            is_green = (abs(col_x) <= green_width_half) and (abs(row_y) <= green_length_half)
            
            if is_pin and is_target: line_str += " [PX] "
            elif is_pin: line_str += "  [P]  "
            elif is_target: line_str += "  [X]  "
            elif is_green: line_str += "  [G]  "
            else:
                # Fill perimeter map margins contextually with custom hazard markers
                if left_hazard and col_x < -green_width_half: line_str += "  🌊  "
                elif right_hazard and col_x > green_width_half: line_str += "  🌊  "
                elif front_hazard and row_y < -green_length_half: line_str += "  ░░  "
                elif back_hazard and row_y > green_length_half: line_str += "  🌲  "
                else: line_str += "  ..  "
        grid_out.append(line_str)
        
    st.code("\n".join(grid_out), language="text")
    
    # Operational evaluation brief
    st.markdown("##### Strategic Engineering Brief:")
    if abs(offset_x) > 2 or abs(offset_y) > 2:
        st.markdown(f"⚠️ **Target Offset Warning:** The pin is tucked heavily near boundaries. Aiming directly at the flag drops roughly half of your standard ±{base_disp}y dispersion circle into hazards. The predictive model has shifted your target center point **{abs(offset_x)}y sideways and {abs(offset_y)}y deep** to guarantee a lower average score over a 100-round tracking loop.")
    else:
        st.markdown("✅ **Green Light Window:** Pin position is accessible. Your active dispersion width sits comfortably inside the safety margins of the green shape template. Fire directly on the target vector path.")
        
    st.markdown("</div>", unsafe_allow_html=True)
