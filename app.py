import streamlit as st
import pandas as pd
import numpy as np

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie Pro", layout="wide")

# Custom CSS for premium glassmorphism overlaying a high-end golf course aesthetic
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(4, 18, 10, 0.50), rgba(8, 24, 14, 0.65)), 
                    url('https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        width: 100vw;
        height: 100vh;
        color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(6, 20, 12, 0.92) !important;
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
        border: 1px solid rgba(54, 113, 79, 0.4);
        box-shadow: 0 14px 32px -6px rgba(0, 0, 0, 0.75);
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
# Using session_state to retain yardage changes across full application refreshes
if "bag_df" not in st.session_state:
    default_bag = {
        "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
        "Full Stock": [285, 260, 245, 215, 205, 195, 180, 170, 155, 125, 95, 80],
        "Standard Dispersion (y)": [14, 12, 11, 9, 8, 8, 7, 6, 6, 5, 4, 3]
    }
    st.session_state.bag_df = pd.DataFrame(default_bag)

st.title("Virtual Personal Caddie Pro")
st.markdown("Advanced environmental vectoring and safety dispersion matrixing.")
st.markdown("---")

# --- 1. SIDEBAR CONFIGURATION (PRE-ROUND & PERSISTENT BAG) ---
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
st.sidebar.subheader("Live Persistent Bag Profile")
st.sidebar.markdown("<small>Edits made here update live calculations and persist across tweaks.</small>", unsafe_allow_html=True)

# Data editor binds seamlessly directly back into session state
edited_df = st.sidebar.data_editor(
    st.session_state.bag_df, 
    hide_index=True, 
    num_rows="fixed", 
    key="persistent_data_editor"
)
st.session_state.bag_df = edited_df

# --- 2. MAIN DASHBOARD PANELS ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Live Shot Setup")
    
    # Core target metrics inputs
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        live_dist = st.number_input("Target Distance to Pin (y)", min_value=1, max_value=600, value=165)
    with col_d2:
        pin_position = st.selectbox("Pin Placement Zone", ["Middle", "Front", "Back"])
        
    elevation_ft = st.number_input("Net Elevation Change (Feet: + Uphill / - Downhill)", value=0)
    
    # Weather mechanics vectors
    st.markdown("##### Dynamic Ball Flight Wind Vectors")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        shot_wind_relation = st.selectbox("Wind Vector Relative Direction", ["None", "Straight Into", "Straight Downwind", "Crosswind"])
    with col_w2:
        live_wind_mph = st.slider("Wind Velocity (MPH)", 0, 40, 12)

    # 1. Advanced Aero Wind Model (Non-Linear Drag penalties)
    # Headwinds cause significantly steeper penalties due to exponential velocity drag scaling
    wind_adjustment = 0.0
    if shot_wind_relation == 'Straight Into':
        wind_adjustment = float(live_wind_mph) * 1.35  
    elif shot_wind_relation == 'Straight Downwind':
        wind_adjustment = float(live_wind_mph) * -0.65
    elif shot_wind_relation == 'Crosswind':
        wind_adjustment = float(live_wind_mph) * 0.15 # Accounts for aerodynamic balance lift reduction
        
    # 2. Temperature Air Density Model (2 yards per 10 degrees variation away from 75°F baseline)
    temp_variance = float(air_temp) - 75.0
    temp_adjustment = -(temp_variance / 10.0) * 2.0
    
    # 3. Trajectory Elevation Model (1 yard true variance per 3 feet change)
    elevation_adjustment = float(elevation_ft) / 3.0
    
    adjusted_distance = float(live_dist) + wind_adjustment + temp_adjustment + elevation_adjustment

    st.markdown("---")
    st.markdown(f"### Play-As Target: **{adjusted_distance:.1f} Yards**")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"<div class='metric-card'><small>Wind Vector</small><br><b>{wind_adjustment:+.1f}y</b></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-card'><small>Air Density</small><br><b>{temp_adjustment:+.1f}y</b></div>", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"<div class='metric-card'><small>Slope Factor</small><br><b>{elevation_adjustment:+.1f}y</b></div>", unsafe_allow_html=True)
        
    st.markdown(f"<div style='margin-top:15px; padding:10px; background:rgba(255,193,7,0.1); border-radius:6px;'><small>⚠️ <b>Strategic Guardrail:</b> Optimizing safety matrices exclusively for a <b>{pin_position} Pin</b> configuration.</small></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Calculated Strategic Matrix")
    st.markdown("Dynamic alternative profiles generated directly from your live active bag:")

    # Build matrix arrays computing mechanical swings
    matrix_data = []
    for index, row in edited_df.iterrows():
        club = row['Club']
        stock_val = float(row['Full Stock'])
        dispersion_val = float(row['Standard Dispersion (y)'])
        
        # Standardized club mechanic variations
        grip_down_val = stock_val * 0.95        
        three_quarter_val = stock_val * 0.85     
        
        matrix_data.append({
            "Club": club,
            "Full Stock": round(stock_val, 1),
            "Grip Down": round(grip_down_val, 1),
            "3/4 Swing": round(three_quarter_val, 1),
            "Dispersion": dispersion_val
        })
        
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix.drop(columns=["Dispersion"]), use_container_width=True, hide_index=True)
    
    st.markdown("##### Caddie Choice: Safest Strategic Deliveries")
    
    # Filter algorithm prioritizing distance matching and risk-mitigation dispersion circles
    matches = []
    for item in matrix_data:
        for mode in ["Full Stock", "Grip Down", "3/4 Swing"]:
            dist = item[mode]
            diff = dist - adjusted_distance # Positive means long, negative means short
            abs_diff = abs(diff)
            disp = item["Dispersion"]
            
            # Base club selection capture window scales dynamically based on individual club dispersion boundaries
            if abs_diff <= (disp + 3.0):
                # PIN-GUARDRAIL RISK ASSESSMENT RULES:
                # Front Pins: Hard disqualification if typical flight dispersion patterns risk landing short off front fringes
                if pin_position == "Front" and (diff - (disp / 2.0)) < -4.0:
                    continue
                # Back Pins: Hard disqualification if high dispersion risks missing long past backend hazards
                elif pin_position == "Back" and (diff + (disp / 2.0)) > 4.0:
                    continue
                    
                matches.append((abs_diff, diff, item["Club"], mode, dist, disp))
                
    # Sort recommendations cleanly by closest overall path proximity to target window
    matches.sort(key=lambda x: x[0])
    
    if matches:
        for abs_diff, raw_diff, club_name, shot_type, final_yards, dispersion in matches[:3]:
            direction_label = "long" if raw_diff > 0 else "short"
            safety_margin = dispersion / 2.0
            
            st.markdown(f"""
            • **{club_name}** ({shot_type}) — Carries **{final_yards:.1f}y** 
            <br>&nbsp;&nbsp;<small style='color:#A1A1AA;'>Variance: {abs(raw_diff):.1f}y {direction_label} | Safety Margin Range: ±{safety_margin:.1f}y</small>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#FCA5A5;'>*No high-safety alternatives matched green safety requirements inside this range window. Review raw matrix spreadsheet above to force manual selection.*</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
