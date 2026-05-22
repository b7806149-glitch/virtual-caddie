import streamlit as st
import pandas as pd
import numpy as np

# Set up a wide layout
st.set_page_config(page_title="Virtual Personal Caddie", layout="wide")

# Custom CSS for an elite, clean Fairway theme without distracting card containers
st.markdown("""
    <style>
    /* Main App Background - Smooth Grass/Fairway Gradient */
    .stApp {
        background: linear-gradient(135deg, #0B2516 0%, #133A22 50%, #1B4D32 100%);
        color: #F8FAFC;
    }
    
    /* Sidebar styling adjustment for high contrast */
    [data-testid="stSidebar"] {
        background-color: #081C10 !important;
    }
    
    /* Clean text styling to blend beautifully with the background */
    label, p, h3, h4, h5 {
        color: #F1F5F9 !important;
    }
    
    /* Modern, unbordered strategic data tables */
    .stDataFrame {
        background-color: rgba(15, 34, 23, 0.4);
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Virtual Personal Caddie")
st.markdown("Your data-driven strategic partner on the course. Adjust your stock yardages and conditions live.")
st.markdown("---")

# --- 1. SIDEBAR CONFIGURATION ---
st.sidebar.header("Pre-Round & Bag Setup")

global_wind_dir = st.sidebar.selectbox("Pre-Round Wind Baseline Direction", ["North", "South", "East", "West", "Variable"])

st.sidebar.markdown("---")
st.sidebar.subheader("Live Stock Bag Distances (Full Swings)")

# Your updated yardage table baseline mapping
default_bag = {
    "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
    "Full Hard": [290, 240, 260, 220, 210, 200, 185, 175, 160, 130, 105, 85],
    "Full Stock": [280, 230, 245, 215, 205, 195, 180, 170, 155, 125, 95, 80],
    "Full Light": [270, 215, 230, 210, 200, 190, 175, 165, 150, 120, 100, 75]
}
df_stock = pd.DataFrame(default_bag)
edited_df = st.sidebar.data_editor(df_stock, hide_index=True, num_rows="fixed")


# --- 2. MAIN DASHBOARD ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("Live Shot Setup")
    
    live_dist = st.number_input("Target Distance to Pin (Yards)", min_value=1, max_value=600, value=153)
    shot_wind_relation = st.selectbox("Wind Relative Direction For This Shot", ["None", "Straight Into", "Straight Downwind", "Crosswind"])
    live_wind_mph = st.slider("Current Wind Velocity (MPH)", 0, 40, 12)

    # Calculate Play-As Yardage
    wind_adjustment = 0.0
    if shot_wind_relation == 'Straight Into':
        wind_adjustment = float(live_wind_mph) * 1.0  
    elif shot_wind_relation == 'Straight Downwind':
        wind_adjustment = float(live_wind_mph) * -0.5 
        
    adjusted_distance = float(live_dist) + wind_adjustment

    st.markdown("---")
    st.markdown(f"#### Play-As Target: **{adjusted_distance:.1f} Yards**")
    st.markdown(f"Baseline setup configured against a global **{global_wind_dir}** wind system.")


with col_right:
    st.subheader("Calculated Matrix Options")
    st.markdown("Computed alternatives derived entirely from your normal **Full Stock** profile:")

    # Build matrix arrays for pure mathematical mapping
    matrix_data = []
    
    for index, row in edited_df.iterrows():
        club = row['Club']
        stock_val = float(row['Full Stock'])
        
        # Exact requested profiles
        grip_down_val = stock_val * 0.95        # 5% distance reduction
        three_quarter_val = stock_val * 0.85    # 15% distance reduction
        
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
    
    # Algorithm Engine: Locate execution targets closest to the adjusted yardage
    matches = []
    for item in matrix_data:
        for mode in ["Full Stock", "Grip Down (-5%)", "3/4 Swing (-15%)"]:
            dist = item[mode]
            diff = abs(dist - adjusted_distance)
            if diff <= 7.0: # Filter options within a tight playability window
                matches.append((diff, item["Club"], mode, dist))
                
    # Sort options by absolute mathematical accuracy
    matches.sort(key=lambda x: x[0])
    
    if matches:
        for diff, club_name, shot_type, final_yards in matches[:3]:
            st.markdown(f"• **{club_name}** executed as a *{shot_type}* — Flies **{final_yards:.1f}y** (Variance: {diff:+.1f}y)")
    else:
        st.markdown("*No exact calculation matches found within a 7-yard window. Reference the full matrix table above.*")
