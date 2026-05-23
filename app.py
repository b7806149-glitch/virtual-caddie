import streamlit as st
import pandas as pd
import numpy as np

# Set up wide screen view
st.set_page_config(page_title="Strategic Flight Command", layout="wide")

# High-end tactical glassmorphism theme styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(10, 25, 17, 0.75), rgba(4, 12, 8, 0.9)), 
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
    
    .tactical-panel {
        background-color: rgba(12, 36, 22, 0.88);
        backdrop-filter: blur(12px);
        padding: 24px;
        border-radius: 14px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
        margin-bottom: 25px;
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

# --- SIDEBAR: MANUAL ENVIRONMENTAL CONTROL CENTER ---
st.sidebar.header("Manual Environmental Sync")
air_temp = st.sidebar.slider("Air Temperature (°F)", 30, 110, 75, step=5)
wind_speed = st.sidebar.slider("Wind Velocity (MPH)", 0, 40, 10, step=1)
wind_deg = st.sidebar.slider("Wind Source Direction Bearing (°)", 0, 360, 0, step=5, help="0° is North, 180° is South")

st.sidebar.markdown("---")
st.sidebar.subheader("Live Bag Settings")
edited_bag = st.sidebar.data_editor(st.session_state.bag_df, hide_index=True, num_rows="fixed")
st.session_state.bag_df = edited_bag

# Global Physics Modifiers
temp_adj = -((float(air_temp) - 75.0) / 10.0) * 2.0

st.title("Strategic Design Command Center")
st.markdown("Probability-based execution mapping from tee to green.")
st.markdown("---")

# --- GLOBAL HOLE ARCHITECTURE INPUTS ---
st.markdown("<div class='tactical-panel'>", unsafe_allow_html=True)
st.subheader("Hole Dimension & Target Line Alignment")
col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    hole_length = st.number_input("Total Hole Length / Distance from Current Position (y)", min_value=50, max_value=650, value=424)
with col_h2:
    target_line_heading = st.slider("Hole Target Line Heading Direction (°)", 0, 360, 0, step=5, help="The straight-line direction the hole runs.")
with col_h3:
    elevation_ft = st.number_input("Elevation Change (Feet: +Uphill / -Downhill)", value=0)

slope_adj = float(elevation_ft) / 3.0

# Calculate wind relation vector
diff_deg = (wind_deg - target_line_heading) % 360
if 45 <= diff_deg < 135: relation = "Crosswind (Left to Right)"
elif 135 <= diff_deg < 225: relation = "Straight Downwind"
elif 225 <= diff_deg < 315: relation = "Crosswind (Right to Left)"
else: relation = "Straight Into"

st.markdown(f"**Atmospheric Influence Profile:** {relation} @ {wind_speed} MPH | **Air Density Shift:** {temp_adj:+.1f}y | **Slope Adjustment:** {slope_adj:+.1f}y")
st.markdown("</div>", unsafe_allow_html=True)


# --- TWO-PHASE STRATEGIC PLAYBOARD ---
col_left, col_right = st.columns(2, gap="large")

with col_left:
    # ==========================================
    # PHASE 1: THE TEE SHOT BLUEPRINT
    # ==========================================
    st.markdown("<div class='tactical-panel'>", unsafe_allow_html=True)
    st.subheader("Phase 1: Tee Shot Risk Analyzer")
    st.markdown("<small>Evaluate options to find the most secure, predictable landing area.</small>", unsafe_allow_html=True)
    
    club_options = edited_bag["Club"].tolist()
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        tee_club_1 = st.selectbox("Aggressive Option", club_options, index=0) # Driver
    with col_sel2:
        tee_club_2 = st.selectbox("Conservative Layback", club_options, index=2) # Hybrid

    def process_shot_prediction(club_name, bag_data):
        row = bag_data[bag_data["Club"] == club_name].iloc[0]
        stock = float(row["Full Stock"])
        disp = float(row["Base Dispersion (y)"])
        
        aero = 0.85 if any(g in club_name for g in ["Driver", "3-Wood", "Hybrid"]) else 1.0
        wind_penalty = 0.0
        if "Straight Into" in relation: wind_penalty = float(wind_speed) * 1.30 * aero
        elif "Straight Downwind" in relation: wind_penalty = -float(wind_speed) * 0.60 * (1 / aero)
        
        expected_carry = stock - wind_penalty + (-temp_adj)
        remaining = max(0.0, float(hole_length) - expected_carry)
        return expected_carry, remaining, disp

    carry_1, rem_1, disp_1 = process_shot_prediction(tee_club_1, edited_bag)
    carry_2, rem_2, disp_2 = process_shot_prediction(tee_club_2, edited_bag)

    col_box1, col_box2 = st.columns(2)
    with col_box1:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03); border-left:4px solid #F43F5E; padding:12px; border-radius:4px;'>
            <b>{tee_club_1} Strategy</b><br>
            Carry: <b>{carry_1:.1f}y</b><br>
            Approach Left: <b>{rem_1:.1f}y</b><br>
            Expected Error: <b>±{disp_1}y</b>
        </div>
        """, unsafe_allow_html=True)
    with col_box2:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03); border-left:4px solid #34D399; padding:12px; border-radius:4px;'>
            <b>{tee_club_2} Strategy</b><br>
            Carry: <b>{carry_2:.1f}y</b><br>
            Approach Left: <b>{rem_2:.1f}y</b><br>
            Expected Error: <b>±{disp_2}y</b>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    
    # User overrides remaining yardage based on actual tee result or specific targets
    st.markdown("##### Select Operational Second Shot Yardage:")
    approach_source = st.radio("Feeding Mechanism:", ["Use Remaining from Option A", "Use Remaining from Option B", "Manual Entry Override"], horizontal=True)
    
    if "Option A" in approach_source:
        active_approach_dist = rem_1
        active_tee_disp = disp_1
    elif "Option B" in approach_source:
        active_approach_dist = rem_2
        active_tee_disp = disp_2
    else:
        active_approach_dist = st.number_input("Enter Manual Approach Distance (y)", value=150)
        active_tee_disp = 10.0
        
    st.markdown(f"Targeting Distance Locked for Approach Phase: **{active_approach_dist:.1f} Yards**")
    st.markdown("</div>", unsafe_allow_html=True)


with col_right:
    # ==========================================
    # PHASE 2: THE GREEN APPROACH MATRIX
    # ==========================================
    st.markdown("<div class='tactical-panel'>", unsafe_allow_html=True)
    st.subheader("Phase 2: Green Target & Miss Mapping")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        pin_location = st.selectbox("Pin Placement Zone", ["Middle", "Tucked Front Left", "Tucked Front Right", "Tucked Back Left", "Tucked Back Right"])
        approach_club = st.selectbox("Select Approach Club Choice", club_options, index=7) # Default 8-iron
    with col_g2:
        hazard_profile = st.selectbox("Immediate Severe Penalty Threat", ["None", "Left Side Hazard", "Right Side Hazard", "Front False Front / Bunker", "Back Deep Hazard"])

    # Map flag locations internally on standard coordinate scale
    pin_x, pin_y = 0, 0
    if "Left" in pin_location: pin_x = -8
    if "Right" in pin_location: pin_x = 8
    if "Front" in pin_location: pin_y = -10
    if "Back" in pin_location: pin_y = 10

    # Fetch approach club specs
    app_row = edited_bag[edited_bag["Club"] == approach_club].iloc[0]
    app_stock = float(app_row["Full Stock"])
    app_disp = float(app_row["Base Dispersion (y)"])
    
    # Recalculate wind drop for approach swing profile
    app_aero = 1.3 if any(w in approach_club for w in ["Wedge", "9-iron", "8-iron"]) else 1.0
    app_wind_penalty = 0.0
    if "Straight Into" in relation: app_wind_penalty = float(wind_speed) * 1.30 * app_aero
    elif "Straight Downwind" in relation: app_wind_penalty = -float(wind_speed) * 0.60 * (1 / app_aero)
    
    # True delivery distance expectation 
    app_true_carry = app_stock - app_wind_penalty + (-temp_adj) - slope_adj

    # RUN MONTE CARLO TARGET PATTERN OPTIMIZER
    green_w, green_l = 12.5, 17.5
    best_ax, best_ay = 0.0, 0.0
    max_safety_val = -1000.0
    final_gir_pct = 0.0

    for tx in range(-12, 13, 1):
        for ty in range(-15, 16, 1):
            np.random.seed(42)
            sim_x = np.random.normal(tx, app_disp / 3.0, 200)
            sim_y = np.random.normal(ty, app_disp / 2.5, 200)
            
            green_hits = 0
            penalties = 0
            
            for sx, sy in zip(sim_x, sim_y):
                if (abs(sx) <= green_w) and (abs(sy) <= green_l):
                    green_hits += 1
                else:
                    if "Left" in hazard_profile and sx < -green_w: penalties += 3.5
                    if "Right" in hazard_profile and sx > green_w: penalties += 3.5
                    if "Front" in hazard_profile and sy < -green_l: penalties += 2.5
                    if "Back" in hazard_profile and sy > green_l: penalties += 2.5
            
            pct = (green_hits / 200.0) * 100.0
            score_metric = pct - penalties
            
            if score_metric > max_safety_val:
                max_safety_val = score_metric
                best_ax, best_ay = tx, ty
                final_gir_pct = pct

    # Resolve target shift adjustments
    shift_x = best_ax - pin_x
    shift_y = best_ay - pin_y
    optimal_play_yardage = active_approach_dist + shift_y

    st.markdown(f"""
    <div style='background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.3); padding:14px; border-radius:6px;'>
        <b>Optimized Target Execution Line:</b><br>
        • Adjusted Swing Target Distance: <b>{optimal_play_yardage:.1f} Yards</b><br>
        • Wind-Corrected Club Delivery: <b>{app_true_carry:.1f} Yards</b> ({approach_club})<br>
        • Aim Alignment Shift: <b>{abs(shift_x):.1f}y {"RIGHT" if shift_x > 0 else "LEFT"}</b> of Flag Line<br>
        • Safe Green Probability: <b>{final_gir_pct:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)

    # OUTPUT DYNAMIC VISUAL SPATIAL CHART
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    st.markdown("##### Green Landing Space Mapping Array:")
    
    map_rows = []
    for ry in range(16, -17, -4):
        row_str = ""
        for cx in range(-12, 13, 2):
            is_pin = (abs(cx - pin_x) <= 1) and (abs(ry - pin_y) <= 2)
            is_tgt = (abs(cx - best_ax) <= 1) and (abs(ry - best_ay) <= 2)
            is_grn = (abs(cx) <= green_w) and (abs(ry) <= green_l)
            
            if is_pin and is_tgt: row_str += " [PX] "
            elif is_pin: row_str += "  [P]  "
            elif is_tgt: row_str += "  [X]  "
            elif is_grn: row_str += "  [G]  "
            else:
                if "Left" in hazard_profile and cx < -green_w: row_str += "  🌊  "
                elif "Right" in hazard_profile and cx > green_w: row_str += "  🌊  "
                elif "Front" in hazard_profile and ry < -green_l: row_str += "  ░░  "
                elif "Back" in hazard_profile and ry > green_l: row_str += "  🌲  "
                else: row_str += "  ..  "
        map_rows.append(row_str)
        
    st.code("\n".join(map_rows), language="text")

    # PREDICTED MISS MANAGEMENT LOGIC
    st.markdown("##### Boundary Window Diagnostics (Where to Miss & By How Much):")
    short_miss = app_true_carry - (app_disp / 2.0)
    long_miss = app_true_carry + (app_disp / 2.0)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.02); padding:10px; border-radius:6px; border-left:4px solid #60A5FA;'>
            <small><b>Acceptable Short Miss Bounds</b></small><br>
            Carry: <b>{short_miss:.1f}y</b><br>
            Result vs Pin: <b>{short_miss - active_approach_dist:+.1f}y</b>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.02); padding:10px; border-radius:6px; border-left:4px solid #F43F5E;'>
            <small><b>Acceptable Long Miss Bounds</b></small><br>
            Carry: <b>{long_miss:.1f}y</b><br>
            Result vs Pin: <b>{long_miss - active_approach_dist:+.1f}y</b>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
