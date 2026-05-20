import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Personal Virtual Caddie", page_icon="⛳", layout="wide")

st.title("⛳ Personal Virtual Caddie")
st.markdown("Your data-driven strategic partner on the course. Adjust your stock yardages and conditions live.")

# --- 1. LIVE CONFIGURATION SETTINGS (EDITABLE BY USER) ---
st.sidebar.header("⚙️ Pre-Round & Bag Setup")

# Editable variable for grip down deduction percentage
grip_down_pct = st.sidebar.slider("Percentage distance lost when you 'Grip Down' (%)", 1, 15, 5)

# Global Wind baseline configuration
global_wind_dir = st.sidebar.selectbox("Pre-Round General Wind Direction", ["North", "South", "East", "West", "Variable"])

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Edit Your Stock Yardages Live")
st.sidebar.markdown("Double-click any cell below to change your yardages. The caddie will immediately use your new numbers.")

# Baseline dictionary for your club profiles
default_bag = {
    "Club": ["Driver", "3-Wood", "Hybrid", "4-iron", "5-iron", "6-iron", "7-iron", "8-iron", "9-iron", "50-deg Wedge", "54-deg Wedge", "58-deg Wedge"],
    "Full Hard": [275, 240, 220, 205, 195, 180, 168, 155, 142, 122, 105, 85],
    "Full Stock": [260, 230, 210, 195, 185, 170, 158, 145, 132, 112, 95, 75],
    "Full Light": [245, 215, 200, 185, 175, 160, 148, 135, 122, 102, 85, 65],
    "3/4 Swing": [210, 190, 175, 165, 155, 140, 130, 118, 105, 90, 75, 55]
}
df_stock = pd.DataFrame(default_bag)

# Streamlit Data Editor enables the user to change numbers directly inside the user interface
edited_df = st.sidebar.data_editor(df_stock, hide_index=True, num_rows="fixed")

# --- 2. MAIN APP DISPLAY ---
tab1, tab2 = st.tabs(["🧠 Virtual Caddie Engine", "📊 My Bag Diagnostics"])

# --- TAB 1: VIRTUAL CADDIE ---
with tab1:
    st.header("🤖 Live Strategic Recommendation")
    
    # Inform the direction of the wind on this specific shot
    col_dist, col_wdir, col_wmph = st.columns(3)
    with col_dist:
        live_dist = st.number_input("Target Distance to Pin (Yards)", min_value=1, max_value=600, value=153)
    with col_wdir:
        shot_wind_relation = st.selectbox("Wind Relative Direction For This Shot", ["None", "Straight Into", "Straight Downwind", "Crosswind"])
    with col_wmph:
        live_wind_mph = st.slider("Current Wind Velocity (MPH)", 0, 40, 12)
        
    # Weather accounting engine
    wind_adjustment = 0
    if shot_wind_relation == 'Straight Into':
        wind_adjustment = live_wind_mph * 1.0  
    elif shot_wind_relation == 'Straight Downwind':
        wind_adjustment = live_wind_mph * -0.5 
        
    adjusted_distance = live_dist + wind_adjustment
    
    st.markdown(f"### 🧮 Play-As Target: **{adjusted_distance:.1f} Yards**")
    st.caption(f"Baseline setup configured against a global **{global_wind_dir}** wind system.")
    
    st.markdown("---")
    st.subheader("📋 Your Caddie's Shot Options Matched To Target")

    # Generate recommendation cards dynamically using the live edited tables
    recommendations_found = 0
    
    # Process every club in the editable database matrix
    for index, row in edited_df.iterrows():
        club_name = row['Club']
        
        # Calculate options based on the user data layout
        modes = {
            "Full Hard Swing": row['Full Hard'],
            "Full Stock Swing": row['Full Stock'],
            "Full Light Swing": row['Full Light'],
            "3/4 Swing": row['3/4 Swing']
        }
        
        for mode_name, base_yardage in modes.items():
            # Standard Option
            if abs(base_yardage - adjusted_distance) <= 6:
                st.info(f"⛳ **{club_name}**: Normal Grip / **{mode_name}** (Carries ~{base_yardage}y)")
                recommendations_found += 1
                
            # Grip Down Option (Applies the deduction formula)
            grip_down_yardage = base_yardage * (1 - (grip_down_pct / 100))
            if abs(grip_down_yardage - adjusted_distance) <= 6:
                st.warning(f"⚠️ **{club_name}**: **Grip Down** / **{mode_name}** (Reduces target to ~{grip_down_yardage:.1f}y)")
                recommendations_found += 1

    if recommendations_found == 0:
        st.error("No exact standard stock yardage matches this distance. Check 'My Bag Diagnostics' to build a specialized wedge sequence or unique intermediate flight layout.")

# --- TAB 2: BAG DIAGNOSTICS ---
with tab2:
    st.header("📊 Total Bag Ranges & Calibration Matrix")
    
    # Metrics breakdown display at the top
    st.metric(label="Grip Down Distance Reduction Factor", value=f"- {grip_down_pct}%")
    st.markdown("This chart visualizes your active range limits across all layout profiles. Adjusting fields in the sidebar changes this chart automatically.")
    
    # Display complete range parameters cleanly
    display_diagnose_df = edited_df.copy()
    
    # Inject computed columns for transparency
    display_diagnose_df["3/4 Grip Down (Min)"] = (display_diagnose_df["3/4 Swing"] * (1 - (grip_down_pct / 100))).round(1)
    
    # Reorganize table presentation structure
    ordered_columns = ["Club", "3/4 Grip Down (Min)", "3/4 Swing", "Full Light", "Full Stock", "Full Hard"]
    st.dataframe(display_diagnose_df[ordered_columns], use_container_width=True, hide_index=True)
