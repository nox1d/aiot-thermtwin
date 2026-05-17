import streamlit as st
import os
import time
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient

st.set_page_config(page_title="IoT Data Dashboard", layout="wide")
st.title("Streamlit + :rainbow[InfluxDB 3 Core] + Mosquitto Dashboard")

INFLUX_URL = "http://influxdb3-core:8181"
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = "admin"
INFLUX_DATABASE = "sensor_data"

if not INFLUX_TOKEN:
    st.error("Error: INFLUX_TOKEN is missing! Check your .env file.")

st.write("ts :rainbow[finally] working gang")
st.info("This is a prototype. The data shown is randomly generated.")



with st.container(width=1000):
    num_periods = 24
    time_data = pd.date_range(start="2023-10-02 00:00:00", periods=num_periods, freq="h")
    time_data_past = pd.date_range(start="2023-10-01 00:00:00", periods=num_periods, freq="h")

    # 2. Generate mock temperature data (between 15.0°C and 100.0°C)
    temperature_data = np.round(np.random.uniform(low=15.0, high=100.0, size=num_periods), 1)
    temperature_data_past = np.round(np.random.uniform(low=15.0, high=100.0, size=num_periods), 1)

    # 3. Create the Pandas DataFrames
    df = pd.DataFrame({
        'time': time_data,
        'temperature': temperature_data
    })
    df2 = pd.DataFrame({
        'past_time': time_data_past,
        'past_temperature': temperature_data_past
    })

    # --- FIX: Combine data for the chart ---
    # We extract the 'Hour' as an index so that both days align nicely over a 24-hour X-axis
    chart_data = pd.DataFrame({
        'Yesterday': temperature_data_past,
        'Today': temperature_data
    }, index=df['time'].dt.strftime('%H:%M')) 

    # --- Streamlit UI ---
    tab1, tab2 = st.tabs(["Chart", "Dataframe"])

    # Plot the combined DataFrame (Plots 2 lines over 24 periods)
    tab1.line_chart(chart_data, height=400, color=["#fd0", "#f0f"])

    # Combine both dataframes side-by-side so df2 isn't left unused
    combined_df = pd.concat([df, df2], axis=1)
    tab2.dataframe(combined_df, height=400, use_container_width=True)

a, b = st.columns(2)
c, d = st.columns(2)

a.metric("Temperature", "45°C", "-9°C", border=True)
b.metric("Fan Speed", "1200 rpm", "150 rm", border=True)

c.metric("Humidity", "67%", "-5%", border=True)
d.metric("Some other sensor", "67", "67", border=True)


def predict():
    prediction = np.random.randint(3)
    return prediction

with st.container(height=300):
    st.markdown("**Model Prediction Status**")
    
    # 1. Show the loading spinner
    with st.spinner("Predicting...", show_time=True):
         time.sleep(2)
        
    # 2. Get prediction
    prediction = predict()
    
    # 3. Show message
    if prediction == 0:
        st.success("Fan speed decreased.")
    elif prediction == 1:
        st.warning("Fan speed unchanged.")
    else:
        st.error("Fan speed increased.")
        
    # 4. Give the user time to read the message, then rerun the entire app
    time.sleep(3)
    st.rerun()
