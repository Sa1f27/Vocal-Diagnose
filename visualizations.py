import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

class Visualizer:
    def __init__(self):
        self.color_map = {
            'High': '#FF4B4B',
            'Medium': '#FFA500',
            'Low': '#00CC00'
        }
    
    def create_waveform(self, audio_data, fs):
        time = np.linspace(0, len(audio_data) / fs, len(audio_data))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=audio_data.flatten(),
            line=dict(color='#FF4B4B', width=1)
        ))
        fig.update_layout(
            title="Voice Waveform",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            template="plotly_white",
            height=300
        )
        return fig
    
    def create_spectrogram(self, audio_data, fs):
        spectrogram = librosa.feature.melspectrogram(y=audio_data.flatten(), sr=fs)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
        
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=spectrogram_db,
            colorscale='Viridis'
        ))
        fig.update_layout(
            title="Spectrogram",
            yaxis_title="Frequency",
            xaxis_title="Time",
            height=300
        )
        return fig
    
    def create_risk_gauge(self, risk_score):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_score,
            title = {'text': "Risk Score"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': self._get_risk_color(risk_score)},
                'steps': [
                    {'range': [0, 40], 'color': 'lightgray'},
                    {'range': [40, 70], 'color': 'gray'},
                    {'range': [70, 100], 'color': 'darkgray'}
                ]
            }
        ))
        fig.update_layout(height=250)
        return fig
    
    def create_history_trend(self, history_data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history_data['Date'],
            y=history_data['Risk Score'],
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='#FF4B4B')
        ))
        fig.update_layout(
            title="Risk Score Trend",
            xaxis_title="Date",
            yaxis_title="Risk Score",
            template="plotly_white",
            height=300
        )
        return fig
    
    def _get_risk_color(self, score):
        if score > 70:
            return self.color_map['High']
        elif score > 40:
            return self.color_map['Medium']
        return self.color_map['Low']