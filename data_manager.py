"""
Data Manager Module
Handles loading, processing, and managing energy consumption data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config


class DataManager:
    """Manages energy consumption data from CSV file"""
    
    def __init__(self):
        """Initialize the DataManager"""
        self.df = None
        self.processed_df = None
        
    def load_data(self):
        """Load data from CSV file"""
        try:
            # Load the dataset
            self.df = pd.read_csv(config.DATASET_FILE)
            
            # Convert datetime column to datetime type
            self.df[config.DATETIME_COL] = pd.to_datetime(self.df[config.DATETIME_COL])
            
            # Sort by datetime
            self.df = self.df.sort_values(config.DATETIME_COL)
            
            # Remove any missing values
            self.df = self.df.dropna()
            
            print(f"✓ Data loaded successfully: {len(self.df)} records")
            return True
            
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            return False
    
    def prepare_features(self):
        """Extract features from datetime for machine learning"""
        try:
            # Create a copy for processing
            self.processed_df = self.df.copy()
            
            # Extract time-based features
            self.processed_df['year'] = self.processed_df[config.DATETIME_COL].dt.year
            self.processed_df['month'] = self.processed_df[config.DATETIME_COL].dt.month
            self.processed_df['day'] = self.processed_df[config.DATETIME_COL].dt.day
            self.processed_df['hour'] = self.processed_df[config.DATETIME_COL].dt.hour
            self.processed_df['day_of_week'] = self.processed_df[config.DATETIME_COL].dt.dayofweek
            self.processed_df['day_of_year'] = self.processed_df[config.DATETIME_COL].dt.dayofyear
            
            # Create cyclical features for hour and month (better for ML)
            self.processed_df['hour_sin'] = np.sin(2 * np.pi * self.processed_df['hour'] / 24)
            self.processed_df['hour_cos'] = np.cos(2 * np.pi * self.processed_df['hour'] / 24)
            self.processed_df['month_sin'] = np.sin(2 * np.pi * self.processed_df['month'] / 12)
            self.processed_df['month_cos'] = np.cos(2 * np.pi * self.processed_df['month'] / 12)
            
            print("✓ Features prepared successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error preparing features: {str(e)}")
            return False
    
    def get_current_usage(self):
        """Get the most recent energy usage data"""
        if self.df is None or len(self.df) == 0:
            return None
        
        latest = self.df.iloc[-1]
        return {
            'datetime': latest[config.DATETIME_COL],
            'energy_mw': latest[config.ENERGY_COL],
            'energy_kwh': latest[config.ENERGY_COL] * 1000,  # Convert MW to kWh
            'cost': latest[config.ENERGY_COL] * 1000 * config.ENERGY_COST_PER_KWH
        }
    
    def get_daily_stats(self, date=None):
        """Get statistics for a specific day"""
        if self.df is None:
            return None
        
        if date is None:
            date = self.df[config.DATETIME_COL].max().date()
        
        # Filter data for the specific date
        daily_data = self.df[self.df[config.DATETIME_COL].dt.date == date]
        
        if len(daily_data) == 0:
            return None
        
        return {
            'date': date,
            'total_energy': daily_data[config.ENERGY_COL].sum(),
            'avg_energy': daily_data[config.ENERGY_COL].mean(),
            'max_energy': daily_data[config.ENERGY_COL].max(),
            'min_energy': daily_data[config.ENERGY_COL].min(),
            'total_cost': daily_data[config.ENERGY_COL].sum() * 1000 * config.ENERGY_COST_PER_KWH
        }
    
    def get_weekly_stats(self):
        """Get statistics for the last 7 days"""
        if self.df is None:
            return None
        
        # Get last 7 days of data
        end_date = self.df[config.DATETIME_COL].max()
        start_date = end_date - timedelta(days=7)
        
        weekly_data = self.df[
            (self.df[config.DATETIME_COL] >= start_date) & 
            (self.df[config.DATETIME_COL] <= end_date)
        ]
        
        if len(weekly_data) == 0:
            return None
        
        # Group by date
        daily_totals = weekly_data.groupby(
            weekly_data[config.DATETIME_COL].dt.date
        )[config.ENERGY_COL].sum()
        
        return {
            'start_date': start_date.date(),
            'end_date': end_date.date(),
            'total_energy': weekly_data[config.ENERGY_COL].sum(),
            'avg_daily_energy': daily_totals.mean(),
            'total_cost': weekly_data[config.ENERGY_COL].sum() * 1000 * config.ENERGY_COST_PER_KWH,
            'daily_data': daily_totals
        }
    
    def get_hourly_pattern(self):
        """Get average energy consumption by hour of day"""
        if self.df is None:
            return None
        
        # Calculate average consumption for each hour
        hourly_avg = self.df.groupby(
            self.df[config.DATETIME_COL].dt.hour
        )[config.ENERGY_COL].mean()
        
        return hourly_avg
    
    def get_training_data(self):
        """Get prepared data for model training"""
        if self.processed_df is None:
            return None, None
        
        # Features for training
        feature_cols = ['hour', 'day_of_week', 'month', 'day_of_year',
                       'hour_sin', 'hour_cos', 'month_sin', 'month_cos']
        
        X = self.processed_df[feature_cols]
        y = self.processed_df[config.ENERGY_COL]
        
        return X, y
    
    def simulate_device_usage(self, device_name, hours):
        """Simulate energy consumption and cost for a device"""
        if device_name not in config.DEVICES:
            return None
        
        # Get device power consumption in Watts
        power_watts = config.DEVICES[device_name]
        
        # Calculate energy consumption in kWh
        energy_kwh = (power_watts * hours) / 1000
        
        # Calculate cost
        cost = energy_kwh * config.ENERGY_COST_PER_KWH
        
        return {
            'device': device_name,
            'power_watts': power_watts,
            'hours': hours,
            'energy_kwh': round(energy_kwh, 2),
            'cost': round(cost, 2)
        }
    
