import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

class EnergyAI:
    def __init__(self, data_path):
        """
        Initializes the AI by loading the Household Power Consumption dataset.
        Handles missing values marked as '?' and fixes date/time formats.
        """
        print(f"Loading dataset from: {data_path}...")
        
        # 1. Load data and treat '?' as NaN (Not a Number)
        self.df = pd.read_csv(data_path, na_values='?', low_memory=False)
        
        # 2. Fill missing values using interpolation 
        # (This estimates gaps based on surrounding values, ideal for time-series)
        numeric_cols = ['Global_active_power', 'Global_reactive_power', 'Voltage', 
                        'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
        self.df[numeric_cols] = self.df[numeric_cols].interpolate(method='linear')
        
        # 3. Pre-processing: Combine Date and Time for analysis
        # Dayfirst=True is used because your dataset uses DD/MM/YYYY
        self.df['datetime'] = pd.to_datetime(self.df['Date'] + ' ' + self.df['Time'], dayfirst=True)
        
        # Sort by time to ensure the forecast trend is accurate
        self.df = self.df.sort_values('datetime').reset_index(drop=True)

    def get_forecast(self, window=1000):
        """
        AI to predict the next 10 minutes of usage using Linear Regression.
        Uses the last 'window' of rows to find the most current trend.
        """
        # We focus on the most recent data points for short-term forecasting
        recent_data = self.df.tail(window)
        
        X = np.array(range(len(recent_data))).reshape(-1, 1)
        y = recent_data['Global_active_power'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict the next 10 steps (minutes)
        future_X = np.array(range(len(recent_data), len(recent_data) + 10)).reshape(-1, 1)
        predictions = model.predict(future_X)
        return predictions

    def calculate_metrics(self):
        """Calculates core dashboard metrics: Voltage, Consumption, and CO2 Savings"""
        avg_voltage = self.df['Voltage'].mean()
        total_power_kw = self.df['Global_active_power'].sum()
        
        # Convert total power (minutes of kW) to kWh (kilowatt-hours)
        total_kwh = total_power_kw / 60
        
        # Eco-impact logic: 1kWh approx 0.4kg CO2. Goal of 15% savings.
        co2_saved = (total_kwh * 0.4) * 0.15 
        
        return {
            "Average Voltage (V)": round(avg_voltage, 2),
            "Total Consumption (kWh)": round(total_kwh, 2),
            "Estimated CO2 Saved (kg)": round(co2_saved, 2)
        }

# --- Execution Block ---
if __name__ == "__main__":
    # Ensure your CSV file is in the same folder as this script
    FILE_NAME = 'household_power_consumption.csv'
    
    try:
        # Initialize the AI
        ai = EnergyAI(FILE_NAME)
        
        # Calculate Metrics
        metrics = ai.calculate_metrics()
        print("\n--- CORE METRICS ---")
        for key, value in metrics.items():
            print(f"{key}: {value}")
            
        # Get Forecast
        forecast = ai.get_forecast()
        print("\n--- 10-MINUTE POWER FORECAST (kW) ---")
        for i, val in enumerate(forecast, 1):
            print(f"Minute {i}: {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: File '{FILE_NAME}' not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")