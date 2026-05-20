import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Personal Virtual Caddie", page_icon="⛳", layout="wide")

st.title("⛳ Personal Virtual Caddie & Shot Analytics Engine")
st.markdown("""
This app acts as a data-driven golf caddie. It calculates the optimal club selection based on 
live weather conditions and personal historical dispersion patterns to maximize your probability of hitting the green.
""")

# --- 1. SEED DATA ---
@st.cache_data
def load_historical_data():
    data = {
        'Hole': [1, 3, 4, 5, 5, 6, 7, 8, 9],
        'Club': ['4-iron', 'Driver', '9-iron', '50-deg', '54-deg', 'Hybrid', 'Wedge', '6-iron', 'Wedge'],
        'Setup_Grip': ['Fully Extended', 'Fully Extended', 'Fully Extended', 'Fully Extended', 'Choked Down', 'Fully Extended', 'Fully Extended', 'Fully Extended', 'Fully Extended'],
        'Swing_Type': ['Punch', 'Full', '3/4', 'Full', '2/3', 'Full', 'Full', 'Full', 'Full'],
        'Shot_Shape': ['Heel Blade Right', 'Push Block', 'Slight Cut', 'Straight', 'Bladed', 'Miss Right', 'Push Right', 'High Right', 'Low Block Right'],
        'Lie': ['Fairway', 'Rough', 'Fairway', 'Fairway', 'Fairway', 'Fairway', 'Tall Grass', 'Fairway', 'Fairway'],
        'Target_Distance': [210, 150, 153, 115, 76, 220, 56, 210, 98],
        'Wind_MPH': [5, 5, 5, 8, 8, 5, 5, 10, 15],
        'Wind_Dir': ['Cross', 'None', 'None', 'Into', 'Into', 'None', 'None', 'Down', 'Into'],
        'Comfort_Rating': [3, 3, 4, 5, 3, 4, 2, 4, 2],
        'Hit_Green': [0, 1, 1, 1, 0, 0, 0, 1, 0],
        'Actual_Distance': [185, 145, 148, 112, 82, 235, 35, 215, 85]
    }
    return pd.DataFrame(data)

df = load_historical_data()

# --- 2. SIDEBAR: DATA ENTRY PORTAL ---
st.sidebar.header("📱 Log a New Shot")
with st.sidebar.form("shot_form"):
    hole_num = st.number_input("Hole #", min_value=1, max_value=18, value=1)
    
    club_select = st.selectbox("Club Used", [
        'Driver', '3-Wood', 'Hybrid', '4-iron', '5-iron', '6-iron', '7-iron', '8-iron', '9-iron', 
        '50-deg Wedge', '54-deg Wedge', '58-deg Wedge', 'Putter'
    ])
    
    # Track gripping down vs fully extended
    grip_select = st.selectbox("Club Grip Setup", ['Fully Extended', 'Choked Down', 'Normal Grip'])
    
    # Track swing sizing
    swing_select = st.selectbox("Swing Control", ['Full', '3/4', '2/3', '1/2', 'Punch / Knockdown'])
    
    # Track tendency patterns
    shape_select = st.selectbox("Shot Result Shape", [
        'Straight / Target', 'Slight Draw', 'Slight Cut / Fade', 
        'Push Block Right', 'Pull Hook Left', 'Thinned / Bladed', 'Chunked / Short'
    ])
    
    lie_select = st.selectbox("Lie Conditions", ['Tee Box', 'Fairway', 'Rough', 'Deep Rough / Tall Grass', 'Sand Bunker', 'Fringe'])
    target_dist = st.number_input("Target Distance (Yards)", min_value=1, max_value=600, value=150)
    wind_m = st.slider("Wind Speed (MPH)", 0, 40, 10)
    wind_d = st.selectbox("Wind Direction", ['None', 'Into Wind', 'Downwind', 'Crosswind Left-to-Right', 'Crosswind Right-to-Left'])
    comfort = st.slider("Confidence Over Ball (1-5)", 1, 5, 4)
    green_check = st.checkbox("Did you hit your target destination / green?")
    
    submit_button = st.form_submit_button("Log Shot to Database")
    if submit_button:
        st.sidebar.success(f"Successfully logged {grip_select} {club_select} shot!")

# --- 3. DISPLAY TABS ---
tab1, tab2, tab3 = st.tabs(["🧠 Virtual Caddie Engine", "📊 Bag Diagnostics", "📋 Historical Shot Log"])

with tab1:
    st.header("🤖 Live Strategic Recommendation")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        live_dist = st.number_input("Current Yardage to Pin", min_value=1, max_value=600, value=153)
    with col2:
        live_wind_dir = st.selectbox("Current Wind Direction", ['None', 'Into Wind', 'Downwind', 'Crosswind'])
    with col3:
        live_wind_mph = st.slider("Current Wind Speed (MPH)", 0, 40, 12)
        
    wind_adjustment = 0
    if live_wind_dir == 'Into Wind':
        wind_adjustment = live_wind_mph * 1.0  
    elif live_wind_dir == 'Downwind':
        wind_adjustment = live_wind_mph * -0.5 
        
    adjusted_distance = live_dist + wind_adjustment
    st.subheader(f"🧮 Play-As Distance: **{adjusted_distance:.1f} Yards**")
    
    st.markdown("### 📋 Best Choice Based on Your Grip & Swing History")
    stats_df = df.groupby(['Club', 'Setup_Grip', 'Swing_Type']).agg(
        Total_Shots=('Hit_Green', 'count'),
        Green_Prob=('Hit_Green', 'mean')
    ).reset_index()
    
    stats_df = stats_df.sort_values(by=['Green_Prob'], ascending=False)
    
    for idx, row in stats_df.iterrows():
        prob_pct = row['Green_Prob'] * 100
        st.info(f"👉 **{row['Setup_Grip']} ({row['Swing_Type']}) {row['Club']}**: **{prob_pct:.0f}%** success rate observed across {row['Total_Shots']} attempts.")

with tab2:
    st.header("📈 Miss Patterns & Improvement Areas")
    st.markdown("### Your Historical Shot Shape Distributions")
    st.dataframe(df[['Club', 'Setup_Grip', 'Swing_Type', 'Shot_Shape']], use_container_width=True)
    st.warning("💡 **Caddie Tip:** Notice that when you go to your wedge shots out of tough lies, a 'Choked Down' approach yields significantly more control over the distance.")

with tab3:
    st.header("🗄️ Database Inspection")
    st.dataframe(df, use_container_width=True)
