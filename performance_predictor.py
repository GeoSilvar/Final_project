import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class StudentPerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.features = [
            'attendance_rate', 
            'previous_scores_avg',
            'assessment_count',
            'special_needs_level',
            'days_since_enrollment'
        ]
    
    def train(self, student_data: List[Dict]):
        """Train the performance prediction model"""
        try:
            df = pd.DataFrame(student_data)
            
            # Feature engineering
            X = df[self.features]
            y = df['current_performance']
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_scaled, y)
            
            logger.info("Performance prediction model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
    
    def predict(self, student_features: Dict) -> Optional[float]:
        """Predict student performance score"""
        if not self.model:
            logger.error("Model not trained yet")
            return None
        
        try:
            # Prepare features
            feature_vector = np.array([[student_features[feature] for feature in self.features]])
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            prediction = self.model.predict(feature_vector_scaled)[0]
            return max(0, min(100, prediction))  # Clamp between 0-100
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
    
    def detect_attendance_anomalies(self, attendance_data: List[float]) -> List[bool]:
        """Detect attendance anomalies using simple statistical methods"""
        if len(attendance_data) < 5:
            return [False] * len(attendance_data)
        
        mean_attendance = np.mean(attendance_data)
        std_attendance = np.std(attendance_data)
        
        anomalies = []
        for attendance in attendance_data:
            # Flag as anomaly if more than 2 standard deviations from mean
            is_anomaly = abs(attendance - mean_attendance) > 2 * std_attendance
            anomalies.append(is_anomaly)
        
        return anomalies