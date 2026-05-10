import streamlit as st
import os
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
st.info("Ensure you have generated an Admin token from your InfluxDB 3 instance and pasted it into Telegraf and Streamlit configs.")