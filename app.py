import streamlit as st
import pandas as pd
import numpy as np

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie", layout="wide")

# Custom CSS for full-bleed golf course photographic background and readable text layers
st.markdown("""
    <style>
    /* Full-screen high-end golf course background overlooking a fairway */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.55)), 
                    url('https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #F8FAFC;
    }
    
    /* Transparent blur styling for the sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(8, 28, 16, 0.85) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Clean text styling to blend beautifully with the imagery */
    label, p, h3, h4, h5 {
        color: #F1F5F9 !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.8);
    }
    
    /* High-contrast dashboard control backdrop boxes */
    .dashboard-panel {
        background-color: rgba(15, 34, 23, 0.8);
        backdrop-filter: blur(8px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(43, 91, 63, 0.6);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    
    /* Translucent container formatting for the main data grid */
    .stDataFrame {
        background-color: rgba(8, 28, 16, 0.7);
        border-radius: 8px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Virtual Personal Caddie")
st.markdown("Your data-driven strategic partner on the course. Adjust your stock yardages and environmental constraints live.")
st.markdown("---")

# --- 1. SIDEBAR CONFIGURATION ---
st.sidebar.header("Pre-Round & Bag Setup")

global_wind_dir = st.sidebar.selectbox("Pre-Round Wind Baseline Direction", ["North", "South", "East", "West", "Variable"], key="sidebar_wind_dir")

# Temperature variable tracking
air_temp = st.sidebar.slider("Current Air Temperature (°F)", 30, 110, 75, step=5, key="sidebar_temp")

st.sidebar.markdown("---")
st.sidebar.subheader("Live Stock Bag Distances (Full Swings)")

# Updated baselines matching your updated metrics (Driver: 285y, 3-Wood: 260y)
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
    
    live_dist = st.number_input("Target Distance to Pin (Yards)", min_value=1, max_value=600, value=153, key="shot_distance_input")
    shot_wind_relation = st.selectbox("Wind Relative Direction For This Shot", ["None", "Straight Into", "Straight Downwind", "Crosswind"], key="shot_wind_rel_input")
    live_wind_mph = st.slider("Current Wind Velocity (MPH)", 0, 40, 12, key="shot_wind_speed_input")

    # Environmental Matrix Algorithm Calculations
    # 1. Wind Physics Calculation (1.2x penalty into wind, 0.6x gain downwind)
    wind_adjustment = 0.0
    if shot_wind_relation == 'Straight Into':
        wind_adjustment = float(live_wind_mph) * 1.2  
    elif shot_wind_relation == 'Straight Downwind':
        wind_adjustment = float(live_wind_mph) * -0.6
        
    # 2. Temperature Physics Calculation (2 yards per 10 degrees variance from 75)
    temp_variance = float(air_temp) - 75.0
    temp_adjustment = -(temp_variance / 10.0) * 2.0  # Cold air requires more yardage, warm air requires less
    
    adjusted_distance = float(live_dist) + wind_adjustment + temp_adjustment

    st.markdown("---")
    st.markdown(f"#### Play-As Target: **{adjusted_distance:.1f} Yards**")
    st.markdown(f"• Wind Offset: {wind_adjustment:+.1f}y | Temperature Offset: {temp_adjustment:+.1f}y")
    st.markdown(f"• Base System: Global **{global_wind_dir}** Wind Blueprint")
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
        grip_down_val = stock_val * 0.95        # Stands as distinct 5% distance step
        three_quarter_val = stock_val * 0.85    # Stands as distinct 15% distance step
        
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
    
    # Locate execution targets closest to the adjusted yardage
    matches = []
    for item in matrix_data:
        for mode in ["Full Stock", "Grip Down (-5%)", "3/4 Swing (-15%)"]:
            dist = item[mode]
            diff = abs(dist - adjusted_distance)
            if diff <= 7.0: 
                matches.append((diff, item["Club"], mode, dist))
                
    # Sort options by absolute accuracy
    matches.sort(key=lambda x: x[0])
    
    if matches:
        for diff, club_name, shot_type, final_yards in matches[:3]:
            st.markdown(f"• **{club_name}** executed as a *{shot_type}* — Flies **{final_yards:.1f}y** (Variance: {diff:+.1f}y)")
    else:
        st.markdown("*No exact calculation matches found within a 7-yard window. Reference the full matrix table above.*")
    st.markdown("</div>", unsafe_allow_html=True)
