import streamlit as st
import pandas as pd
import numpy as np

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie Pro", layout="wide")

# Custom CSS for premium glassmorphism overlaying a high-end golf course aesthetic
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

# --- 1. SIDEBAR CONFIGURATION ---
st.sidebar.header("Pre-Round & Bag Setup")

col_lat, col_lon = st.sidebar.columns(2)
with col_lat:
    air_temp = st.sidebar.slider("Air Temp (°F)", 30, 110, 75, step=5)
with col_lon:
    st.sidebar.markdown("<div style='padding-top:22px;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Reset Bag Defaults"):
        del st.session_state.bag_df
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Live Active Bag Profile")

edited_df = st.sidebar.data_editor(
    st.session_state.bag_df, 
    hide_index=True, 
    num_rows="fixed", 
    key="persistent_data_editor"
)
st.session_state.bag_df = edited_df

# Extract live values dynamically for background physics modeling
try:
    driver_stock = float(edited_df.loc[edited_df['Club'] == 'Driver', 'Full Stock'].values[0])
    driver_disp = float(edited_df.loc[edited_df['Club'] == 'Driver', 'Base Dispersion (y)'].values[0])
    hybrid_stock = float(edited_df.loc[edited_df['Club'] == 'Hybrid', 'Full Stock'].values[0])
    hybrid_disp = float(edited_df.loc[edited_df['Club'] == 'Hybrid', 'Base Dispersion (y)'].values[0])
except IndexError:
    driver_stock, driver_disp = 285, 14
    hybrid_stock, hybrid_disp = 245, 11

# --- 2. MAIN DASHBOARD PANELS ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # PANEL A: Live Shot Setup
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
    
    st.markdown("##### Dynamic Ball Flight Wind Vectors")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        shot_wind_relation = st.selectbox("Wind Vector Relative Direction", ["None", "Straight Into", "Straight Downwind", "Crosswind"])
    with col_w2:
        live_wind_mph = st.slider("Wind Velocity (MPH)", 0, 40, 12)

    # Global Environmental Calculations (Base)
    temp_variance = float(air_temp) - 75.0
    temp_adjustment = -(temp_variance / 10.0) * 2.0
    elevation_adjustment = float(elevation_ft) / 3.0
    
    base_play_as = float(live_dist) + temp_adjustment + elevation_adjustment
    
    st.markdown("---")
    st.markdown(f"### Play-As Target Base: **{base_play_as:.1f} Yards**")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"<div class='metric-card'><small>Air Density</small><br><b>{temp_adjustment:+.1f}y</b></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-card'><small>Slope Factor</small><br><b>{elevation_adjustment:+.1f}y</b></div>", unsafe_allow_html=True)
    with col_m3:
        lie_label = ball_lie.split(" ")[0]
        st.markdown(f"<div class='metric-card'><small>Selected Lie</small><br><b>{lie_label}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- NEW ADDITION: HOLE STRATEGY OPTIMIZER ---
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Tee Shot Strategy & Risk Assessment")
    st.markdown("<small>Evaluate if stretching the driver pattern is statistically justified by the remaining approach window.</small>", unsafe_allow_html=True)
    
    hole_length = st.number_input("Total Hole Length / Distance to Target Window (y)", min_value=100, max_value=650, value=424)
    
    # Calculate tee shot wind adjustments using the advanced physics profiles
    tee_wind_adj_dr = float(live_wind_mph) * 0.85 if shot_wind_relation == "Straight Into" else (-float(live_wind_mph) * 0.45 if shot_wind_relation == "Straight Downwind" else 0)
    tee_wind_adj_hy = float(live_wind_mph) * 1.00 if shot_wind_relation == "Straight Into" else (-float(live_wind_mph) * 0.55 if shot_wind_relation == "Straight Downwind" else 0)
    
    expected_dr_dist = driver_stock - tee_wind_adj_dr + (-temp_adjustment)
    expected_hy_dist = hybrid_stock - tee_wind_adj_hy + (-temp_adjustment)
    
    rem_dr = max(0.0, float(hole_length) - expected_dr_dist)
    rem_hy = max(0.0, float(hole_length) - expected_hy_dist)
    gained_yards = expected_dr_dist - expected_hy_dist
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""
        <div style='background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2); padding:12px; border-radius:8px;'>
            <b style='color:#FCA5A5;'>Option A: Aggressive Driver</b><br>
            Est. Carry: <b>{expected_dr_dist:.1f}y</b><br>
            Approach Left: <b style='color:#FCA5A5;'>{rem_dr:.1f}y</b><br>
            Lateral Error Risk: <b>±{driver_disp}y</b>
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown(f"""
        <div style='background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.2); padding:12px; border-radius:8px;'>
            <b style='color:#86EFAC;'>Option B: Tactical Hybrid</b><br>
            Est. Carry: <b>{expected_hy_dist:.1f}y</b><br>
            Approach Left: <b style='color:#86EFAC;'>{rem_hy:.1f}y</b><br>
            Lateral Error Risk: <b>±{hybrid_disp}y</b>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    
    # Strategic analysis decision tree logic
    if rem_dr < 40:
        st.markdown(f"💡 **Strategic Advisory:** **Hybrid is heavily favored.** Driver leaves you under 40 yards ({rem_dr:.1f}y), which pushes you into awkward partial-wedge territory. Lay back to {rem_hy:.1f}y for a comfortable, high-spin full target swing.")
    elif gained_yards < 20:
        st.markdown(f"💡 **Strategic Advisory:** **Take the Hybrid.** Wind/temperature models have compressed the distance gap to only {gained_yards:.1f} yards. Taking on the wider driver dispersion circle (±{driver_disp}y) yields negligible position benefits.")
    elif rem_hy > 210 and rem_dr <= 175:
        st.markdown(f"🔥 **Strategic Advisory:** **Driver is highly viable.** Laying back with hybrid leaves a grueling {rem_hy:.1f}y approach (long iron/wood). Driver targets a manageable short-iron window of {rem_dr:.1f}y. The extra risk significantly improves your green-in-regulation probability.")
    else:
        st.markdown(f"⚖️ **Strategic Advisory:** **Balanced Choice.** Driver gains {gained_yards:.1f} yards over the hybrid, leaving a short iron ({rem_dr:.1f}y vs {rem_hy:.1f}y). Choose Driver if the fairway boundary is wide; lean on Hybrid if hazard lines are tight.")
        
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Calculated Strategic Matrix")
    st.markdown("Dynamic alternative profiles generated with advanced club aero and lie modifiers:")

    matrix_data = []
    for index, row in edited_df.iterrows():
        club = row['Club']
        stock_val = float(row['Full Stock'])
        base_dispersion = float(row['Base Dispersion (y)'])
        
        if any(w in club for w in ["Wedge", "9-iron", "8-iron"]):
            aero_mult = 1.3
        elif any(g in club for g in ["Driver", "3-Wood", "Hybrid"]):
            aero_mult = 0.85
        else:
            aero_mult = 1.0
            
        club_wind_adj = 0.0
        if shot_wind_relation == 'Straight Into':
            club_wind_adj = float(live_wind_mph) * 1.30 * aero_mult
        elif shot_wind_relation == 'Straight Downwind':
            club_wind_adj = float(live_wind_mph) * -0.60 * (1 / aero_mult)
        elif shot_wind_relation == 'Crosswind':
            club_wind_adj = float(live_wind_mph) * 0.15 * aero_mult

        lie_dist_mod = 1.0
        dispersion_mod = 1.0
        
        if "Flyer" in ball_lie:
            lie_dist_mod = 1.05
            dispersion_mod = 1.4
        elif "Heavy" in ball_lie:
            lie_dist_mod = 0.90
            dispersion_mod = 1.6
        elif "Bunker" in ball_lie:
            lie_dist_mod = 0.95
            dispersion_mod = 1.2
            
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
            st.markdown(f"""
            • **{club_name}** ({shot_type}) — Expected Flight: **{final_yards:.1f}y** <br>&nbsp;&nbsp;<small style='color:#A1A1AA;'>Pin Miss: {abs(raw_diff):.1f}y {direction_label} | Standard Shot Dispersion Range: ±{current_disp/2:.1f}y</small>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#FCA5A5;'>*No high-safety matches found with current lie/wind configuration for a {pin_position} pin.*</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
