import streamlit as st
import os
import time
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient

# 1. Page Config (Wide layout is crucial for Bento grids)
st.set_page_config(page_title="IoT Data Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- HEADER BENTO ---
st.title("📟 :rainbow[IoT Command Center]")
st.markdown("Streamlit + **InfluxDB 3 Core** + Mosquitto Dashboard")

INFLUX_URL = "http://influxdb3-core:8181"
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = "admin"
INFLUX_DATABASE = "sensor_data"

if not INFLUX_TOKEN:
    st.warning("Warning: INFLUX_TOKEN is missing! Check your .env file.")

st.info("💡 **Prototype Mode:** ts finally working gang. Data shown is randomly generated.")

# --- CACHE DATA (Prevents chart flickering during st.rerun) ---
@st.cache_data
def get_mock_data():
    num_periods = 24
    time_data = pd.date_range(start="2023-10-02 00:00:00", periods=num_periods, freq="h")
    time_data_past = pd.date_range(start="2023-10-01 00:00:00", periods=num_periods, freq="h")

    temp_data = np.round(np.random.uniform(low=15.0, high=100.0, size=num_periods), 1)
    temp_data_past = np.round(np.random.uniform(low=15.0, high=100.0, size=num_periods), 1)

    df = pd.DataFrame({'time': time_data, 'temperature': temp_data})
    df2 = pd.DataFrame({'past_time': time_data_past, 'past_temperature': temp_data_past})

    chart_data = pd.DataFrame({
        'Yesterday': temp_data_past,
        'Today': temp_data
    }, index=df['time'].dt.strftime('%H:%M')) 

    combined_df = pd.concat([df, df2], axis=1)
    return chart_data, combined_df

chart_data, combined_df = get_mock_data()


# ==========================================
# 🍱 BENTO BOX GRID LAYOUT
# ==========================================

# --- ROW 1: METRIC CARDS ---
# We use 4 columns to create 4 small top-level bento boxes
m1, m2, m3, m4 = st.columns(4)

m1.metric("🌡️ Temperature", "45°C", "-9°C", border=True)
m2.metric("💨 Fan Speed", "1200 rpm", "150 rpm", border=True)
m3.metric("💧 Humidity", "67%", "-5%", border=True)
m4.metric("⚡ System Load", "42%", "3%", border=True, delta_color="inverse")

st.write("") # Small spacer

# --- ROW 2: MAIN CONTENT ---
# We use a 2.5 to 1 ratio so the chart is much larger than the prediction box
col_chart, col_predict = st.columns([2.5, 1])

# Box 1: Chart & Data (Left side)
with col_chart.container(border=True, height=450):
    st.markdown("### 📈 Sensor Telemetry")
    
    tab1, tab2 = st.tabs(["Chart View", "Data Table View"])

    with tab1:
        st.line_chart(chart_data, height=300, color=["#fd0", "#f0f"])

    with tab2:
        st.dataframe(combined_df, height=300, use_container_width=True)


# Box 2: Prediction Status (Right side)
def predict():
    return np.random.randint(3)

with col_predict.container(border=True, height=450):
    st.markdown("### 🤖 Edge AI Status")
    
    # Use st.empty() inside the bento box to swap messages smoothly 
    # without making the box expand or jump around
    status_placeholder = st.empty()
    
    # 1. Show spinner inside the placeholder
    with status_placeholder.container():
        st.write("") # Spacer
        with st.spinner("Analyzing telemetry...", show_time=True):
             time.sleep(2)
             
    # 2. Get prediction
    prediction = predict()
    
    # 3. Overwrite the spinner with the result
    with status_placeholder.container():
        st.write("") # Spacer
        if prediction == 0:
            st.success("📉 **Fan speed decreased.**")
        elif prediction == 1:
            st.warning("⚖️ **Fan speed unchanged.**")
        else:
            st.error("📈 **Fan speed increased.**")
            
        st.caption("Next prediction in 3 seconds...")
        
    # 4. Wait, then rerun the app
    time.sleep(3)
    st.rerun()