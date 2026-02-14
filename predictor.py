"""
Predictor Module
Handles machine learning model training and predictions
"""

import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import config


class EnergyPredictor:
    """Machine Learning predictor for energy consumption"""
    
    def __init__(self):
        """Initialize the predictor"""
        self.model = None
        self.is_trained = False
        self.metrics = {}
        
    def train_model(self, X, y):
        """
        Train the Linear Regression model
        
        Args:
            X: Feature matrix
            y: Target values (energy consumption)
        """
        try:
            print("\n" + "="*50)
            print("TRAINING ENERGY PREDICTION MODEL")
            print("="*50)
            
            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=config.TRAINING_TEST_SPLIT, 
                random_state=42
            )
            
            print(f"Training samples: {len(X_train)}")
            print(f"Testing samples: {len(X_test)}")
            
            # Create and train the model
            self.model = LinearRegression()
            self.model.fit(X_train, y_train)
            
            # Make predictions on test set
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            self.metrics = {
                'mae': mean_absolute_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred)
            }
            
            self.is_trained = True
            
            print("\n✓ Model trained successfully!")
            print(f"  Mean Absolute Error: {self.metrics['mae']:.2f} MW")
            print(f"  Root Mean Squared Error: {self.metrics['rmse']:.2f} MW")
            print(f"  R² Score: {self.metrics['r2']:.4f}")
            print("="*50 + "\n")
            
            return True
            
        except Exception as e:
            print(f"✗ Error training model: {str(e)}")
            return False
    
    def predict(self, features):
        """
        Make a prediction using the trained model
        
        Args:
            features: Feature array or dictionary
            
        Returns:
            Predicted energy consumption
        """
        if not self.is_trained or self.model is None:
            print("✗ Model not trained yet!")
            return None
        
        try:
            # Convert dictionary to array if needed
            if isinstance(features, dict):
                feature_order = ['hour', 'day_of_week', 'month', 'day_of_year',
                               'hour_sin', 'hour_cos', 'month_sin', 'month_cos']
                features = np.array([[features[f] for f in feature_order]])
            
            # Make prediction
            prediction = self.model.predict(features)
            return prediction[0]
            
        except Exception as e:
            print(f"✗ Error making prediction: {str(e)}")
            return None
    
    def predict_next_day(self, current_datetime):
        """
        Predict energy consumption for the next 24 hours
        
        Args:
            current_datetime: Starting datetime for predictions
            
        Returns:
            List of predictions for next 24 hours
        """
        if not self.is_trained:
            return None
        
        predictions = []
        
        for hour in range(24):
            # Calculate features for this hour
            future_time = current_datetime + pd.Timedelta(hours=hour)
            
            features = {
                'hour': future_time.hour,
                'day_of_week': future_time.dayofweek,
                'month': future_time.month,
                'day_of_year': future_time.dayofyear,
                'hour_sin': np.sin(2 * np.pi * future_time.hour / 24),
                'hour_cos': np.cos(2 * np.pi * future_time.hour / 24),
                'month_sin': np.sin(2 * np.pi * future_time.month / 12),
                'month_cos': np.cos(2 * np.pi * future_time.month / 12)
            }
            
            pred = self.predict(features)
            predictions.append({
                'datetime': future_time,
                'hour': future_time.hour,
                'prediction': pred
            })
        
        return predictions
    
    def predict_next_week(self, current_datetime):
        """
        Predict daily average energy consumption for the next 7 days
        
        Args:
            current_datetime: Starting datetime for predictions
            
        Returns:
            List of daily predictions for next 7 days
        """
        if not self.is_trained:
            return None
        
        daily_predictions = []
        
        for day in range(1, 8):
            # Predict for each hour of the day
            day_predictions = []
            
            for hour in range(24):
                future_time = current_datetime + pd.Timedelta(days=day, hours=hour)
                
                features = {
                    'hour': future_time.hour,
                    'day_of_week': future_time.dayofweek,
                    'month': future_time.month,
                    'day_of_year': future_time.dayofyear,
                    'hour_sin': np.sin(2 * np.pi * future_time.hour / 24),
                    'hour_cos': np.cos(2 * np.pi * future_time.hour / 24),
                    'month_sin': np.sin(2 * np.pi * future_time.month / 12),
                    'month_cos': np.cos(2 * np.pi * future_time.month / 12)
                }
                
                pred = self.predict(features)
                day_predictions.append(pred)
            
            # Calculate daily average
            daily_avg = np.mean(day_predictions)
            
            daily_predictions.append({
                'date': (current_datetime + pd.Timedelta(days=day)).date(),
                'day_number': day,
                'prediction': daily_avg
            })
        
        return daily_predictions
    
    def save_model(self, filepath=None):
        """Save the trained model to a file"""
        if not self.is_trained:
            print("✗ No trained model to save!")
            return False
        
        if filepath is None:
            filepath = config.MODEL_FILE
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'metrics': self.metrics
                }, f)
            print(f"✓ Model saved to {filepath}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving model: {str(e)}")
            return False
    
    def load_model(self, filepath=None):
        """Load a trained model from a file"""
        if filepath is None:
            filepath = config.MODEL_FILE
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.metrics = data['metrics']
                self.is_trained = True
            
            print(f"✓ Model loaded from {filepath}")
            return True
            
        except FileNotFoundError:
            print(f"ℹ No saved model found at {filepath}")
            return False
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return False
    
    def get_model_info(self):
        """Get information about the trained model"""
        if not self.is_trained:
            return None
        
        return {
            'trained': self.is_trained,
            'metrics': self.metrics,
            'coefficients': len(self.model.coef_) if self.model else 0
        }


# Import pandas here to avoid issues
import pandas as pd
