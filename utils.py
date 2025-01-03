import librosa
import numpy as np
import pandas as pd
import tensorflow as tf
import plotly.graph_objects as go
import plotly.express as px
from scipy.io import wavfile
import soundfile as sf
import requests
from datetime import datetime
import json
import os
from cryptography.fernet import Fernet

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050
        self.duration = 5
        
    def extract_features(self, audio_path):
        y, sr = librosa.load(audio_path, duration=self.duration)
        
        # Extract features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral = librosa.feature.spectral_centroid(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        zero_crossing = librosa.feature.zero_crossing_rate(y)
        
        # Combine features
        features = {
            'mfcc_mean': np.mean(mfccs, axis=1),
            'mfcc_var': np.var(mfccs, axis=1),
            'spectral_mean': np.mean(spectral),
            'chroma_mean': np.mean(chroma),
            'zero_crossing_mean': np.mean(zero_crossing)
        }
        
        return features

class HealthAnalyzer:
    def __init__(self):
        self.risk_thresholds = {
            'breathing': {'high': 0.7, 'medium': 0.4},
            'cough': {'high': 0.75, 'medium': 0.45},
            'speech': {'high': 0.65, 'medium': 0.35}
        }
    
    def analyze_health(self, features, test_type):
        # Demo analysis - replace with actual model
        feature_values = np.concatenate([v.flatten() for v in features.values()])
        risk_score = np.mean(feature_values)
        normalized_score = (risk_score + 1) / 2  # Normalize to 0-1
        
        thresholds = self.risk_thresholds[test_type]
        if normalized_score > thresholds['high']:
            return 'High', normalized_score * 100
        elif normalized_score > thresholds['medium']:
            return 'Medium', normalized_score * 100
        return 'Low', normalized_score * 100

class SecurityManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(json.dumps(data).encode())
        
    def decrypt_data(self, encrypted_data):
        return json.loads(self.cipher_suite.decrypt(encrypted_data).decode())

class ReportGenerator:
    def __init__(self):
        self.template = """
        VocalDiagnose Health Report
        Date: {date}
        
        Patient Information:
        Name: {name}
        Age: {age}
        Gender: {gender}
        
        Test Results:
        Type: {test_type}
        Risk Level: {risk_level}
        Risk Score: {risk_score:.2f}%
        
        Recommendations:
        {recommendations}
        
        Next Steps:
        {next_steps}
        """
    
    def generate_report(self, user_data, test_results):
        recommendations = self.get_recommendations(test_results['risk_level'])
        next_steps = self.get_next_steps(test_results['risk_level'])
        
        report = self.template.format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name=user_data['name'],
            age=user_data['age'],
            gender=user_data['gender'],
            test_type=test_results['test_type'],
            risk_level=test_results['risk_level'],
            risk_score=test_results['risk_score'],
            recommendations='\n'.join(recommendations),
            next_steps='\n'.join(next_steps)
        )
        return report
    
    def get_recommendations(self, risk_level):
        recommendations = {
            'High': [
                "Immediate medical consultation recommended",
                "Monitor symptoms closely",
                "Prepare medical history for doctor visit"
            ],
            'Medium': [
                "Schedule a check-up within next 7 days",
                "Record daily symptoms",
                "Follow prescribed medication schedule"
            ],
            'Low': [
                "Continue regular health monitoring",
                "Maintain healthy lifestyle",
                "Schedule routine check-up"
            ]
        }
        return recommendations.get(risk_level, [])
    
    def get_next_steps(self, risk_level):
        steps = {
            'High': [
                "Contact emergency services if symptoms worsen",
                "Book immediate telehealth consultation",
                "Prepare for in-person medical visit"
            ],
            'Medium': [
                "Book follow-up appointment",
                "Continue monitoring through app",
                "Prepare questions for doctor consultation"
            ],
            'Low': [
                "Schedule next screening in 30 days",
                "Continue regular voice recordings",
                "Update health diary regularly"
            ]
        }
        return steps.get(risk_level, [])