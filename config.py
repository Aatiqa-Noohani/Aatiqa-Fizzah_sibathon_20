"""
Configuration file for Smart Energy Management System
Contains all system settings and constants
"""

# File paths
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'energy_model.pkl'

# Energy pricing (cost per kWh in currency units)
ENERGY_COST_PER_KWH = 0.12

# Device categories and their average consumption (in Watts)
DEVICES = {
    'Air Conditioner': 1500,
    'Refrigerator': 150,
    'Washing Machine': 500,
    'Television': 100,
    'Laptop': 50,
    'LED Lights': 10,
    'Microwave': 1200,
    'Water Heater': 2000,
    'Fan': 75,
    'Desktop Computer': 200
}

# Chart settings
CHART_COLORS = {
    'primary': '#2E86DE',
    'secondary': '#EE5A6F',
    'success': '#26DE81',
    'warning': '#FED330',
    'info': '#45AAF2'
}

# UI Settings
WINDOW_TITLE = "Smart Energy Management System"
WINDOW_SIZE = "1200x700"
BG_COLOR = "#F5F6FA"
BUTTON_COLOR = "#2E86DE"
BUTTON_TEXT_COLOR = "white"
FONT_FAMILY = "Arial"

# Prediction settings
PREDICTION_DAYS = 7  # Number of days to predict ahead
TRAINING_TEST_SPLIT = 0.2  # 20% for testing

# Report settings
REPORT_TYPES = ['Daily', 'Weekly', 'Monthly']

# Dataset column names
DATETIME_COL = 'Datetime'
ENERGY_COL = 'AEP_MW'
