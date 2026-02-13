import streamlit as st
import pandas as pd
import plotly.express as px
from model import EnergyAI

# --- CONFIGURATION & UI THEME ---
st.set_page_config(page_title="Smart Energy AI", layout="wide")

# Classic UI Styling with CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    div[data-testid="stExpander"] { border: none; background-color: #1f2937; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND CONNECTIVITY ---
# Initializing the AI model with the local CSV
ai = EnergyAI('data/house_hold_consumption.csv')
v_mean, p_total, co2 = ai.calculate_metrics()
