import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

class EnergyPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.le_appliance = LabelEncoder()
        self.le_season = LabelEncoder()
        self.scaler = StandardScaler()

    def prepare_data(self, file_path):
        # Load dataset
        df = pd.read_csv(file_path)

        # Feature Engineering: Extract Hour from Time
        df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
        
        # Encoding categorical variables
        df['Appliance Type'] = self.le_appliance.fit_transform(df['Appliance Type'])
        df['Season'] = self.le_season.fit_transform(df['Season'])

        # Select Features and Target
        # Features: Appliance, Temperature, Season, Household Size, Hour
        X = df[['Appliance Type', 'Outdoor Temperature (°C)', 'Season', 'Household Size', 'Hour']]
        y = df['Energy Consumption (kWh)']

        return X, y

    def train(self, X, y):
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Feature Scaling
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train Model
        print("Training the Smart Energy Model...")
        self.model.fit(X_train_scaled, y_train)

        # Evaluation
        predictions = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        print(f"Model Training Complete.")
        print(f"Mean Absolute Error: {mae:.4f} kWh")
        print(f"R2 Score: {r2:.4f}")

    def save_model(self, model_path='energy_model.pkl', scaler_path='scaler.pkl'):
        # Save the model and the scaler for future deployment
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.le_appliance, 'le_appliance.pkl')
        joblib.dump(self.le_season, 'le_season.pkl')
        print("Models and encoders saved successfully.")

if __name__ == "__main__":
    predictor = EnergyPredictor()
    X, y = predictor.prepare_data('smart_home_energy_consumption_large.csv')
    predictor.train(X, y)
    predictor.save_model()
