import streamlit as st
import pandas as pd
import numpy as np

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie", layout="wide")

# Custom CSS for full-canvas image background and readable text panels
st.markdown("""
    <style>
    /* Force the golf course picture to expand seamlessly across the entire screen */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.55)), 
                    url('https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        width: 100vw;
        height: 100vh;
        color: #F8FAFC;
    }
    
    /* Transparent blur styling for the sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(8, 28, 16, 0.88) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Clean high-contrast text styling */
    label, p, h3, h4, h5 {
        color: #F1F5F9 !important;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.9);
    }
    
    /* Blended translucent panel boxes */
    .dashboard-panel {
        background-color: rgba(12, 30, 18, 0.82);
        backdrop-filter: blur(8px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(43, 91, 63, 0.5);
        box-shadow: 0 12px 28px -5px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }
    
    /* Translucent layout formatting for the data tables */
    .stDataFrame {
        background-color: rgba(8, 28, 16, 0.75);
        border-radius: 8px;
        padding: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Virtual Personal Caddie")
st.markdown("Your data-driven strategic partner on the course. Adjust your stock yardages and environmental constraints live.")
st.markdown("---")

# --- 1. SIDEBAR CONFIGURATION ---
st.sidebar.header("Pre-Round & Bag Setup")

global_wind_dir = st.sidebar.selectbox("Pre-Round Wind Baseline Direction", ["North", "South", "East", "West", "Variable"], key="sidebar_wind_dir")
air_temp = st.sidebar.slider("Current Air Temperature (°F)", 30, 110, 75, step=5, key="sidebar_temp")

st.sidebar.markdown("---")
st.sidebar.subheader("Live Stock Bag Distances (Full Swings)")

# Baseline club matrix mapping
default_bag = {
    "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
    "Full Hard": [295, 270, 260, 220, 210, 200, 185, 175, 160, 130, 105, 85],
    "Full Stock": [285, 260, 245, 215, 205, 195, 180, 170, 155, 125, 95, 80],
    "Full Light": [275, 250, 230, 210, 200, 190, 175, 165, 150, 120, 100, 75]
}
df_stock = pd.DataFrame(default_bag)
edited_df = st.sidebar.data_editor(df_stock, hide_index=True, num_rows="fixed", key="bag_data_editor")


# --- 2. MAIN DASHBOARD PANELS ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Live Shot Setup")
    
    # Core target metrics
    live_dist = st.number_input("Target Distance to Pin (Yards)", min_value=1, max_value=600, value=153, key="shot_distance_input")
    pin_position = st.selectbox("Pin Placement Zone", ["Middle", "Front", "Back"], key="pin_position_input")
    elevation_ft = st.number_input("Net Elevation Change (Feet: Use + for Uphill, - for Downhill)", value=0, key="elevation_input")
    
    # Weather mechanics
    shot_wind_relation = st.selectbox("Wind Relative Direction For This Shot", ["None", "Straight Into", "Straight Downwind", "Crosswind"], key="shot_wind_rel_input")
    live_wind_mph = st.slider("Current Wind Velocity (MPH)", 0, 40, 12, key="shot_wind_speed_input")

    # Environmental Matrix Calculations
    # 1. Wind Model Calculation (1.2y penalty into wind, 0.6y gain downwind)
    wind_adjustment = 0.0
    if shot_wind_relation == 'Straight Into':
        wind_adjustment = float(live_wind_mph) * 1.2  
    elif shot_wind_relation == 'Straight Downwind':
        wind_adjustment = float(live_wind_mph) * -0.6
        
    # 2. Temperature Model Calculation (2 yards per 10 degrees variance from 75 baseline)
    temp_variance = float(air_temp) - 75.0
    temp_adjustment = -(temp_variance / 10.0) * 2.0
    
    # 3. Elevation Model Calculation (1 yard of distance adjustment per 3 feet of elevation)
    elevation_adjustment = float(elevation_ft) / 3.0
    
    adjusted_distance = float(live_dist) + wind_adjustment + temp_adjustment + elevation_adjustment

    st.markdown("---")
    st.markdown(f"#### Play-As Target: **{adjusted_distance:.1f} Yards**")
    st.markdown(f"• Wind: {wind_adjustment:+.1f}y | Temp: {temp_adjustment:+.1f}y | Slope: {elevation_adjustment:+.1f}y")
    st.markdown(f"• Strategy Guardrails: Optimized for a **{pin_position} Pin** location.")
    st.markdown("</div>", unsafe_allow_html=True)


with col_right:
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    st.subheader("Calculated Matrix Options")
    st.markdown("Computed alternatives derived entirely from your normal **Full Stock** profile:")

    # Build matrix arrays for pure mathematical mapping
    matrix_data = []
    for index, row in edited_df.iterrows():
        club = row['Club']
        stock_val = float(row['Full Stock'])
        
        # Explicit calculations based on user mechanics profiles
        grip_down_val = stock_val * 0.95        
        three_quarter_val = stock_val * 0.85    
        
        matrix_data.append({
            "Club": club,
            "Full Stock": round(stock_val, 1),
            "Grip Down (-5%)": round(grip_down_val, 1),
            "3/4 Swing (-15%)": round(three_quarter_val, 1)
        })
        
    df_matrix = pd.DataFrame(matrix_data)
    
    # Display the comprehensive distance breakdown table
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    
    st.markdown("##### Closest Strategic Matches To Target:")
    
    # Filter algorithm evaluating both target distance and green buffer zones
    matches = []
    for item in matrix_data:
        for mode in ["Full Stock", "Grip Down (-5%)", "3/4 Swing (-15%)"]:
            dist = item[mode]
            diff = dist - adjusted_distance # Positive means long, negative means short
            abs_diff = abs(diff)
            
            # Base selection window of 7 yards variance
            if abs_diff <= 7.0:
                # Pin Placement Guardrail Rules:
                # If front pin, disqualify clubs that fly short (diff < 0) to avoid rolling off front edge.
                if pin_position == "Front" and diff < -1.0:
                    continue
                # If back pin, disqualify clubs that fly long (diff > 0) to avoid bouncing off back edge.
                elif pin_position == "Back" and diff > 1.0:
                    continue
                    
                matches.append((abs_diff, diff, item["Club"], mode, dist))
                
    # Sort options by absolute proximity to the play-as number
    matches.sort(key=lambda x: x[0])
    
    if matches:
        for abs_diff, raw_diff, club_name, shot_type, final_yards in matches[:3]:
            direction_label = "long" if raw_diff > 0 else "short"
            st.markdown(f"• **{club_name}** ({shot_type}) — Flies **{final_yards:.1f}y** (Misses {abs(raw_diff):.1f}y {direction_label})")
    else:
        st.markdown("*No safe options found matching pin location rules within a 7-yard window. Review the matrix grid above.*")
    st.markdown("</div>", unsafe_allow_html=True)
