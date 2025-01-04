import streamlit as st
import sounddevice as sd
import wavio
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from datetime import datetime
import os
import time
import pandas as pd 

from utils import AudioProcessor, HealthAnalyzer, SecurityManager, ReportGenerator
from database import Database, MockDatabase

# Initialize components
audio_processor = AudioProcessor()
health_analyzer = HealthAnalyzer()
security_manager = SecurityManager()
report_generator = ReportGenerator()
db = MockDatabase()  # Use MockDatabase for local development

# Page configuration
st.set_page_config(
    page_title="VocalDiagnose",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .risk-high { color: #FF4B4B; font-weight: bold; }
    .risk-medium { color: #FFA500; font-weight: bold; }
    .risk-low { color: #00CC00; font-weight: bold; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def record_audio(duration=5):
    fs = 22050
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    with st.spinner(f"Recording for {duration} seconds..."):
        sd.wait()
    return recording, fs

def save_audio(recording, fs, filename):
    wavio.write(filename, recording, fs, sampwidth=2)

def analyze_voice(audio_path, test_type):
    features = audio_processor.extract_features(audio_path)
    risk_level, risk_score = health_analyzer.analyze_health(features, test_type)
    return risk_level, risk_score

def display_waveform(audio_data, fs):
    time = np.linspace(0, len(audio_data) / fs, len(audio_data))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=audio_data.flatten()))
    fig.update_layout(
        title="Voice Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude"
    )
    st.plotly_chart(fig)
import sqlite3
import uuid
import bcrypt

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect('health_monitor.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create the `users` table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    medical_history TEXT
)
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table `users` created successfully.")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = c.fetchone()
        conn.close()
        
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[2]):
            st.session_state['user_id'] = user_data[0]
            st.session_state['login_status'] = True
            st.rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.subheader("Register")
    name = st.text_input("Full Name")
    username = st.text_input("Username", key="reg_username")
    password = st.text_input("Password", type="password", key="reg_password")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    medical_history = st.text_area("Medical History")
    
    if st.button("Register"):
        try:
            conn = sqlite3.connect('health_monitor.db')
            c = conn.cursor()
            user_id = str(uuid.uuid4())
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            c.execute("""
                INSERT INTO users (user_id, username, password, name, age, gender, medical_history)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, username, hashed_password, name, age, gender, medical_history))
            
            conn.commit()
            conn.close()
            st.success("Registration successful! Please login.")
        except sqlite3.IntegrityError:
            st.error("Username already exists")

def main():

    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False
    

    if not st.session_state.get('login_status', False):
        st.title("🎙️ VocalDiagnose")
        # Use tabs for Login and Register pages
        tabs = st.tabs(["Login", "Register"])
        
        with tabs[0]:
            login()  # Call the login function when the Login tab is selected
        
        with tabs[1]:
            register()
    else:

        tabs = st.tabs(["Home", "Voice Analysis", "History", "Profile"])
        
        with tabs[0]:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.title("🎙️ VocalDiagnose")
                st.markdown("""
                ## AI-Powered Voice Health Screening
                Get instant health insights through voice analysis
                """)
                
                # Stats
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    st.markdown("""
                    <div class='metric-card'>
                        <h3>1,234</h3>
                        <p>Users Screened</p>
                    </div>
                    """, unsafe_allow_html=True)
                with stats_col2:
                    st.markdown("""
                    <div class='metric-card'>
                        <h3>89%</h3>
                        <p>Accuracy Rate</p>
                    </div>
                    """, unsafe_allow_html=True)
                with stats_col3:
                    st.markdown("""
                    <div class='metric-card'>
                        <h3>24/7</h3>
                        <p>Availability</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Placeholder for animation
                pass
        
        with tabs[1]:
            st.title("Voice Analysis")
            
            test_type = st.selectbox(
                "Select Test Type",
                ["breathing", "cough", "speech"],
                format_func=lambda x: x.title()
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("Start Recording"):
                    recording, fs = record_audio()
                    
                    # Save audio
                    filename = f"temp_{int(time.time())}.wav"
                    save_audio(recording, fs, filename)
                    
                    # Display waveform
                    display_waveform(recording, fs)
                    
                    # Analyze voice
                    risk_level, risk_score = analyze_voice(filename, test_type)
                    
                    # Display results
                    st.subheader("Analysis Results")
                    st.markdown(f"Risk Level: <span class='risk-{risk_level.lower()}'>{risk_level}</span>", 
                            unsafe_allow_html=True)
                    st.progress(min(max(risk_score / 100, 0.0), 1.0))
                    
                    # Generate and display report
                    user_data = {
                        'name': 'John Doe',  # Replace with actual user data
                        'age': 35,
                        'gender': 'Male'
                    }
                    
                    test_results = {
                        'test_type': test_type,
                        'risk_level': risk_level,
                        'risk_score': risk_score
                    }
                    
                    report = report_generator.generate_report(user_data, test_results)
                    st.text_area("Health Report", report, height=300)
                    
                    # Clean up
                    os.remove(filename)
            
            with col2:
                st.subheader("Instructions")
                st.markdown(f"""
                ### {test_type.title()} Test
                1. Find a quiet environment
                2. Position yourself 30cm from the microphone
                3. Follow the prompt when recording starts
                4. Stay still during recording
                5. Complete the full recording
                """)
        
        with tabs[2]:
            st.title("Test History")
            
            # Mock history data
            history_data = pd.DataFrame({
                'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * 3,
                'Test Type': ['Breathing', 'Speech', 'Cough'],
                'Risk Level': ['Low', 'Medium', 'Low'],
                'Risk Score': [25, 55, 30]
            })
            
            # Display history
            st.dataframe(history_data)
            
            # Trend Analysis
            st.subheader("Risk Score Trends")
            fig = go.Figure()
            fig.add_trace(go.Line(x=history_data['Date'], 
                                y=history_data['Risk Score'],
                                name='Risk Score'))
            st.plotly_chart(fig)
            
            # Export options
            if st.button("Export History"):
                csv = history_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="test_history.csv",
                    mime="text/csv"
                )
        
        with tabs[3]:
            st.title("User Profile")
            
            # Load profile data (mock)
            profile = {
                'name': 'John Doe',
                'age': 35,
                'gender': 'Male',
                'phone': '+91 1234567890',
                'emergency_contact': '+91 9876543210',
                'medical_history': ['None'],
                'language': 'English'
            }
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name", profile['name'])
                age = st.number_input("Age", min_value=0, max_value=120, value=profile['age'])
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                    index=["Male", "Female", "Other"].index(profile['gender']))
                
            with col2:
                phone = st.text_input("Phone", profile['phone'])
                emergency = st.text_input("Emergency Contact", profile['emergency_contact'])
                language = st.selectbox("Preferred Language", 
                                    ["English", "Hindi", "Tamil", "Telugu", "Bengali"],
                                    index=["English", "Hindi", "Tamil", "Telugu", "Bengali"].index(profile['language']))
            
            st.subheader("Medical History")
            conditions = st.multiselect(
                "Select all that apply",
                ["None", "Asthma", "COPD", "Tuberculosis", "Heart Disease", "Diabetes"],
                default=profile['medical_history']
            )
            
            if st.button("Update Profile"):
                st.success("Profile updated successfully!")

if __name__ == "__main__":
    main()
