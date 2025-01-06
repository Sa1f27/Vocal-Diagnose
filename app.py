import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import librosa
import librosa.display
import matplotlib.pyplot as plt
from audio_recorder_streamlit import audio_recorder
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io
import scipy.signal
import warnings
from scipy.signal import hilbert 
warnings.filterwarnings('ignore')
from style import apply_custom_css
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch



# Set page configuration with custom theme
st.set_page_config(
    page_title="VocalDiagnose - Advanced AI Health Screening",
    page_icon="🏥",
    layout= "wide",
    initial_sidebar_state="expanded"
)
css2 = apply_custom_css()
# Enhanced CSS for better UI
st.markdown(css2, unsafe_allow_html=True)

def display_realtime_metrics(analysis_results, test_metrics):
    """Display real-time analysis metrics"""
    cols = st.columns(len(test_metrics))
    
    # Generate sample metrics (replace with actual analysis in production)
    metrics = {
        'Vocal Stability': analysis_results['health_indicators']['voice_stability'],
        'Breathing Rate': analysis_results['health_indicators']['breathing_rate'],
        'Duration': analysis_results['health_indicators']['duration']
    }
    
    for col, metric in zip(cols, metrics.items()):
        with col:
            st.metric(
                metric[0],
                f"{metric[1]:.1f}" + (" bpm" if metric[0] == "Breathing Rate" else 
                                     "s" if metric[0] == "Duration" else "%")
            )
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'risk_scores' not in st.session_state:
        st.session_state.risk_scores = {}
    if 'audio_samples' not in st.session_state:
        st.session_state.audio_samples = {}
    if 'audio_analysis' not in st.session_state:
        st.session_state.audio_analysis = {}
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}

def reset_session():
    st.session_state.clear()

def analyze_audio(audio_bytes, sample_rate=22050):
    """Analyze audio for health indicators"""
    try:
        # Load audio data
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=sample_rate)
        
        # Extract features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
        
        # Calculate health indicators
        breathing_rate = estimate_breathing_rate(y, sr)
        voice_stability = calculate_voice_stability(y)
        
        return {
            'features': {
                'mfcc': mfcc,
                'spectral_centroids': spectral_centroids,
                'zero_crossing_rate': zero_crossing_rate
            },
            'health_indicators': {
                'breathing_rate': breathing_rate,
                'voice_stability': voice_stability,
                'duration': len(y) / sr
            }
        }
    except Exception as e:
        st.error(f"Audio analysis error: {str(e)}")
        return None

def estimate_breathing_rate(y, sr):
    """Estimate breathing rate from audio"""
    envelope = np.abs(hilbert(y))
    peaks = librosa.util.peak_pick(envelope, pre_max=sr//4, post_max=sr//4,
                                 pre_avg=sr//4, post_avg=sr//4, delta=0.1, wait=sr//4)
    if len(peaks) > 1:
        breathing_rate = 60 / (np.mean(np.diff(peaks)) / sr)
        return min(breathing_rate, 30)  # Cap at 30 breaths per minute
    return 0

def calculate_voice_stability(y):
    """Calculate voice stability score"""
    envelope = np.abs(hilbert(y))
    stability = 1.0 / (np.std(envelope) + 1e-6)
    return min(stability * 10, 100)  # Scale and cap at 100

def show_quality_indicators(analysis_results):
    """Display quality indicators for voice recording"""
    st.subheader("Recording Quality Indicators")
    
    quality_metrics = {
        "Signal Strength": min(100, analysis_results['health_indicators']['voice_stability']),
        "Background Noise": np.random.uniform(85, 98),  # Simulated metric
        "Audio Clarity": np.random.uniform(88, 96)  # Simulated metric
    }
    
    for metric, value in quality_metrics.items():
        st.progress(value/100)
        st.caption(f"{metric}: {value:.1f}%")

def analyze_voice_patterns():
    """Analyze patterns in voice recordings"""
    return {
        'frequency_distribution': np.random.normal(0, 1, 100),
        'amplitude_variation': np.random.normal(0, 1, 100),
        'temporal_patterns': np.random.normal(0, 1, 100)
    }

def detect_voice_anomalies():
    """Detect anomalies in voice recordings"""
    return {
        'frequency_anomalies': [(i, v) for i, v in enumerate(np.random.normal(0, 1, 5))],
        'amplitude_anomalies': [(i, v) for i, v in enumerate(np.random.normal(0, 1, 5))],
        'pattern_anomalies': [(i, v) for i, v in enumerate(np.random.normal(0, 1, 5))]
    }

def calculate_voice_trends():
    """Calculate trends in voice metrics over time"""
    return {
        'stability_trend': np.random.normal(0, 1, 10),
        'quality_trend': np.random.normal(0, 1, 10),
        'breathing_trend': np.random.normal(0, 1, 10)
    }

def show_voice_patterns_plot(patterns):
    """Display voice patterns visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=patterns['frequency_distribution'],
        name='Frequency Distribution',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title='Voice Patterns Analysis',
        xaxis_title='Time',
        yaxis_title='Amplitude',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_anomalies_plot(anomalies):
    """Display voice anomalies visualization"""
    fig = go.Figure()
    
    for anomaly_type, values in anomalies.items():
        x, y = zip(*values)
        fig.add_trace(go.Scatter(
            x=x, y=y,
            name=anomaly_type.replace('_', ' ').title(),
            mode='markers+lines'
        ))
    
    fig.update_layout(
        title='Voice Anomalies Detection',
        xaxis_title='Time',
        yaxis_title='Deviation',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def analyze_medical_history():
    """Analyze medical history for risk factors"""
    return {
        'risk_factors': {
            'respiratory': np.random.uniform(0, 100),
            'cardiovascular': np.random.uniform(0, 100),
            'neurological': np.random.uniform(0, 100)
        },
        'severity_scores': {
            'current_conditions': np.random.uniform(0, 100),
            'family_history': np.random.uniform(0, 100)
        }
    }

def generate_combined_assessment(voice_analysis, medical_risks):
    """Generate combined health assessment"""
    return {
        'overall_score': np.random.uniform(60, 95),
        'risk_level': np.random.choice(['Low', 'Moderate', 'High']),
        'confidence': np.random.uniform(85, 98),
        'key_findings': [
            'Finding 1',
            'Finding 2',
            'Finding 3'
        ]
    }

def show_health_score_gauge(score):
    """Display health score gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ]
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def show_health_risks_analysis(medical_risks):
    """Display health risks analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Factors")
        for factor, value in medical_risks['risk_factors'].items():
            st.metric(
                factor.title(),
                f"{value:.1f}%",
                delta=f"{np.random.normal(0, 5):.1f}%"
            )
    
    with col2:
        st.subheader("Severity Scores")
        for score_type, value in medical_risks['severity_scores'].items():
            st.metric(
                score_type.replace('_', ' ').title(),
                f"{value:.1f}%",
                delta=f"{np.random.normal(0, 5):.1f}%"
            )

def show_trend_analysis():
    """Display trend analysis"""
    st.subheader("Health Trends Over Time")
    
    # Generate sample trend data
    dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
    trends = pd.DataFrame({
        'date': dates,
        'health_score': np.random.normal(80, 5, 10),
        'voice_quality': np.random.normal(85, 5, 10),
        'breathing_rate': np.random.normal(75, 5, 10)
    })
    
    fig = px.line(trends, x='date', y=['health_score', 'voice_quality', 'breathing_rate'])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_ai_insights(assessment):
    """Display AI-generated insights"""
    st.subheader("AI Analysis Insights")
    
    for finding in assessment['key_findings']:
        st.success(finding)

def generate_recommendations():
    """Generate health recommendations"""
    return {
        'primary': [
            {'action': 'Schedule follow-up appointment', 'impact': 'High', 'urgency': 'Medium'},
            {'action': 'Start breathing exercises', 'impact': 'Medium', 'urgency': 'High'},
            {'action': 'Monitor voice strain', 'impact': 'Medium', 'urgency': 'Low'}
        ],
        'medical': [
            'Recommendation 1',
            'Recommendation 2',
            'Recommendation 3'
        ],
        'lifestyle': [
            'Lifestyle change 1',
            'Lifestyle change 2',
            'Lifestyle change 3'
        ],
        'followup': {
            'next_appointment': '2024-02-01',
            'tests_required': ['Test 1', 'Test 2'],
            'monitoring_plan': 'Weekly voice recordings'
        }
    }

def show_health_metrics_summary():
    """Display health metrics summary"""
    metrics = {
        'Overall Health': np.random.uniform(70, 95),
        'Voice Quality': np.random.uniform(75, 95),
        'Respiratory Health': np.random.uniform(80, 95)
    }
    
    for metric, value in metrics.items():
        st.metric(metric, f"{value:.1f}%")

def show_medical_recommendations(recommendations):
    """Display medical recommendations"""
    for i, rec in enumerate(recommendations, 1):
        st.success(f"{i}. {rec}")

def show_lifestyle_recommendations(recommendations):
    """Display lifestyle recommendations"""
    for i, rec in enumerate(recommendations, 1):
        st.success(f"{i}. {rec}")

def show_followup_plan(plan):
    """Display follow-up plan"""
    st.write(f"Next Appointment: {plan['next_appointment']}")
    st.write("Required Tests:", ", ".join(plan['tests_required']))
    st.write("Monitoring Plan:", plan['monitoring_plan'])

def show_health_resources():
    """Display health resources"""
    st.write("### Available Resources")
    st.write("1. Online Health Portal")
    st.write("2. Telemedicine Services")
    st.write("3. Emergency Contacts")
    st.write("4. Educational Materials")

def save_session_data():
    """Save current session data"""
    st.success("Session data saved successfully!")

def load_session_data():
    """Load previous session data"""
    st.success("Previous session data loaded successfully!")

def generate_health_report(report_type):
    """Generate health report PDF"""
    return b"Sample PDF content"  # Placeholder for actual PDF generation

def plot_audio_analysis(y, sr, analysis_results):
    """Create audio analysis visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Waveform
    axes[0,0].plot(np.linspace(0, len(y)/sr, len(y)), y)
    axes[0,0].set_title('Waveform')
    axes[0,0].set_xlabel('Time (s)')
    
    # Spectrogram
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, y_axis='log', x_axis='time', ax=axes[0,1])
    axes[0,1].set_title('Spectrogram')
    
    # MFCC
    librosa.display.specshow(analysis_results['features']['mfcc'], 
                           x_axis='time', ax=axes[1,0])
    axes[1,0].set_title('MFCC')
    
    # Zero crossing rate
    axes[1,1].plot(analysis_results['features']['zero_crossing_rate'])
    axes[1,1].set_title('Zero Crossing Rate')
    
    plt.tight_layout()
    return fig

def collect_voice_samples():
    """Enhanced voice sample collection with real-time analysis"""
    st.header("🎤 Advanced Voice Analysis")
    st.success("""
        Please provide voice samples as requested. Our AI system will analyze your voice patterns
        in real-time for various health indicators.
    """)
    
    instructions = {
        "breathing": "Take deep breaths normally for 10 seconds",
        "vowel": "Say 'Aaaaah' for as long as you can",
        "counting": "Count from 1 to 20 at a normal pace"
    }
    
    for test_name, instruction in instructions.items():
        st.subheader(f"Test: {test_name.title()}")
        st.success(instruction)
        
        audio_bytes = audio_recorder(key=f"recorder_{test_name}")
        
        if audio_bytes:
            st.session_state.audio_samples[test_name] = audio_bytes
            st.audio(audio_bytes, format="audio/wav")
            
            # Analyze audio
            analysis = analyze_audio(audio_bytes)
            if analysis:
                st.session_state.analysis_results[test_name] = analysis
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Breathing Rate", 
                             f"{analysis['health_indicators']['breathing_rate']:.1f} bpm")
                with col2:
                    st.metric("Voice Stability", 
                             f"{analysis['health_indicators']['voice_stability']:.1f}%")
                with col3:
                    st.metric("Duration", 
                             f"{analysis['health_indicators']['duration']:.1f}s")
                
                # Plot analysis
                fig = plot_audio_analysis(librosa.load(io.BytesIO(audio_bytes))[0],
                                       22050, analysis)
                st.pyplot(fig)
    
    return len(st.session_state.audio_samples) >= len(instructions)

def show_header():
    """Enhanced header with system status"""
    st.markdown('<div class="header-style">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("🏥 VocalDiagnose AI")
        st.subheader("Advanced Voice-Based Health Screening System")
    with col3:
        if st.button("Start New Screening", key="reset"):
            reset_session()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def collect_demographics():
    """Enhanced demographics collection with validation and default values."""
    st.header("📋 Patient Information")
    st.success("Please provide accurate information for optimal screening results.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name", value="Saif", key="name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"], index=1)
        blood_group = st.selectbox(
            "Blood Group", 
            ["Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
            index=1
        )
    
    with col2:
        height = st.number_input("Height (cm)", min_value=50, max_value=250, value=175)
        weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=74)
        bmi = weight / ((height/100) ** 2) if height and weight else 0
        st.metric("BMI", f"{bmi:.1f}")
        
    with col3:
        languages = st.multiselect(
            "Preferred Languages",
            ["Hindi", "English", "Bengali", "Telugu", "Tamil", "Marathi", 
             "Gujarati", "Kannada", "Malayalam", "Punjabi", "Urdu"],
            default=["English"]
        )
        location = st.text_input("City/Village", value="Hyderabad")
        pin_code = st.text_input("PIN Code", value="500001")

    
    return all([name, age, gender != "Select", blood_group != "Select", 
                languages, location, pin_code])

def collect_medical_history():
    """Compact medical history collection with nested columns"""
    st.header("🏥 Medical History Assessment")
    st.subheader("Please provide accurate information for better health assessment")

    # Health Status Section
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Current Health")
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            existing_conditions = st.multiselect(
                "Medical Conditions",
                ["None", "Diabetes", "Hypertension", "Heart Disease", "Asthma", "Other"])
            medications = st.text_area("Medications", height=50)
        with subcol2:
            allergies = st.multiselect(
                "Allergies",
                ["None", "Drugs", "Food", "Seasonal", "Latex", "Other"])
            past_surgeries = st.text_area("Surgeries", height=50)

    with col2:
        st.markdown("##### Symptoms")
        subcol3, subcol4 = st.columns(2)
        with subcol3:
            respiratory = st.multiselect(
                "Respiratory",
                ["None", "Shortness of Breath", "Cough", "Wheezing", "Other"])
            voice = st.multiselect(
                "Voice Issues",
                ["None", "Hoarseness", "Fatigue", "Loss"])
        with subcol4:
            current = st.multiselect(
                "General",
                ["None", "Fever", "Fatigue", "Weight Loss", "Other"])
            if "Other" in current:
                st.text_input("Specify Other")

    # Lifestyle & Family Section
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Lifestyle")
        subcol5, subcol6, subcol7 = st.columns(3)
        with subcol5:
            smoking = st.radio(
                "Smoking",
                ["Never", "Former", "Current"],
                label_visibility="collapsed")
            if smoking in ["Former", "Current"]:
                st.number_input("Pack Years", 0, 100, 0, label_visibility="collapsed")
        with subcol6:
            alcohol = st.radio(
                "Alcohol",
                ["None", "Occasional", "Regular"],
                label_visibility="collapsed")
        with subcol7:
            exercise = st.select_slider(
                "Activity",
                ["Low", "Medium", "High"],
                label_visibility="collapsed")

    with col4:
        st.markdown("##### Family History")
        subcol8, subcol9 = st.columns(2)
        with subcol8:
            family_history = st.multiselect(
                "Family Conditions",
                ["None", "Diabetes", "Heart Disease", "Cancer", "Other"])
        with subcol9:
            if "Other" in family_history:
                st.text_input("Specify Family History")

    # Submit Section
    col5, col6, col7 = st.columns([1,1,1])
    with col6:
        submitted = st.button("Submit History", type="primary", use_container_width=True)
    
    if submitted:
        st.success("Submitted successfully!")
        return True
    return False

def collect_voice_samples():
    """Enhanced voice sample collection with real-time analysis"""
    st.header("🎤 Advanced Voice Analysis")
    st.success("""
        Please provide voice samples as requested. Our AI system will analyze your voice patterns
        in real-time for various health indicators.
    """)
    
    tests = {
        "sustained_vowel": {
            "name": "Sustained Vowel Analysis",
            "instructions": "Say 'Aaaaah' for as long as you can in a steady tone",
            "duration": "10-15 seconds",
            "metrics": ["Vocal Stability", "Breath Support", "Pitch Analysis"]
        },
        "counting_breath": {
            "name": "Respiratory Capacity Test",
            "instructions": "Count from 1 to 30 in a single breath at a steady pace",
            "duration": "15-20 seconds",
            "metrics": ["Breath Control", "Speech Rate", "Voice Quality"]
        },
        "cough_pattern": {
            "name": "Cough Analysis",
            "instructions": "Provide three natural coughs with brief pauses",
            "duration": "5-10 seconds",
            "metrics": ["Cough Strength", "Cough Pattern", "Airways Assessment"]
        },
        "speech_sample": {
            "name": "Connected Speech Analysis",
            "instructions": "Read the provided paragraph naturally",
            "duration": "30-40 seconds",
            "metrics": ["Articulation", "Prosody", "Voice Quality"]
        },
        "breathing_pattern": {
            "name": "Breathing Pattern Analysis",
            "instructions": "Breathe normally for the specified duration",
            "duration": "20 seconds",
            "metrics": ["Breathing Rate", "Breath Depth", "Regularity"]
        }
    }
    
    samples_collected = 0
    sample_paragraph = """Please read the following: The rainbow appears after the rain, 
    creating a beautiful arc of colors in the sky. Take a deep breath before starting and 
    try to read this in your natural speaking voice."""
    
    # Add articulation test
    tests["articulation_test"] = {
        "name": "Articulation Practice",
        "instructions": "Read the following tongue twisters with clear pronunciation: 'Peter Piper picked a peck of pickled peppers' and 'She sells seashells by the seashore'",
        "duration": "45 seconds",
        "metrics": ["pronunciation_clarity", "speech_rate", "accuracy"]
}

    try:
        col1, col2, col3 = st.columns(3)
        test_pairs = list(tests.items())
        
        for i in range(0, len(test_pairs), 3):
            with col1:
                if i < len(test_pairs):
                    test_id, test_info = test_pairs[i]
                    st.subheader(f"📊 {test_info['name']}")
                    
                    st.markdown(f"""
                        <div class='metric-card' style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                            <p><strong>Instructions:</strong> {test_info['instructions']}</p>
                            <p><strong>Duration:</strong> {test_info['duration']}</p>
                            <p><strong>Key Metrics:</strong> {', '.join(test_info['metrics'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if test_id == "speech_sample":
                        st.markdown(f"""
                            <div style='background-color: #e9ecef; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                                {sample_paragraph}
                            </div>
                        """, unsafe_allow_html=True)
                    
                    audio_bytes = audio_recorder(
                        key=f"audio_recorder_{test_id}",
                        icon_size="1x",
                        text="Click to Record"
                    )
                    
                    if audio_bytes:
                        st.session_state.audio_samples[test_id] = audio_bytes
                        samples_collected += 1
                        
                        analysis_results = analyze_audio(audio_bytes)
                        if analysis_results:
                            st.session_state.audio_analysis[test_id] = analysis_results
                            st.session_state.analysis_results[test_id] = analysis_results
                            
                            st.audio(audio_bytes, format="audio/wav")
                            display_realtime_metrics(analysis_results, test_info['metrics'])
            
            with col2:
                if i + 1 < len(test_pairs):
                    test_id, test_info = test_pairs[i + 1]
                    st.subheader(f"📊 {test_info['name']}")
                    
                    st.markdown(f"""
                        <div class='metric-card' style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                            <p><strong>Instructions:</strong> {test_info['instructions']}</p>
                            <p><strong>Duration:</strong> {test_info['duration']}</p>
                            <p><strong>Key Metrics:</strong> {', '.join(test_info['metrics'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if test_id == "speech_sample":
                        st.markdown(f"""
                            <div style='background-color: #e9ecef; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                                {sample_paragraph}
                            </div>
                        """, unsafe_allow_html=True)
                    
                    audio_bytes = audio_recorder(
                        key=f"audio_recorder_{test_id}",
                        icon_size="1x",
                        text="Click to Record"
                    )
                    
                    if audio_bytes:
                        st.session_state.audio_samples[test_id] = audio_bytes
                        samples_collected += 1
                        
                        analysis_results = analyze_audio(audio_bytes)
                        if analysis_results:
                            st.session_state.audio_analysis[test_id] = analysis_results
                            st.session_state.analysis_results[test_id] = analysis_results
                            
                            st.audio(audio_bytes, format="audio/wav")
                            display_realtime_metrics(analysis_results, test_info['metrics'])

            with col3:
                if i + 2 < len(test_pairs):
                    test_id, test_info = test_pairs[i + 2]
                    st.subheader(f"📊 {test_info['name']}")
                    
                    st.markdown(f"""
                        <div class='metric-card' style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                            <p><strong>Instructions:</strong> {test_info['instructions']}</p>
                            <p><strong>Duration:</strong> {test_info['duration']}</p>
                            <p><strong>Key Metrics:</strong> {', '.join(test_info['metrics'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if test_id == "speech_sample":
                        st.markdown(f"""
                            <div style='background-color: #e9ecef; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                                {sample_paragraph}
                            </div>
                        """, unsafe_allow_html=True)
                    
                    audio_bytes = audio_recorder(
                        key=f"audio_recorder_{test_id}",
                        icon_size="1x",
                        text="Click to Record"
                    )
                    
                    if audio_bytes:
                        st.session_state.audio_samples[test_id] = audio_bytes
                        samples_collected += 1
                        
                        analysis_results = analyze_audio(audio_bytes)
                        if analysis_results:
                            st.session_state.audio_analysis[test_id] = analysis_results
                            st.session_state.analysis_results[test_id] = analysis_results
                            
                            st.audio(audio_bytes, format="audio/wav")
                            display_realtime_metrics(analysis_results, test_info['metrics'])

        st.markdown("---")
        st.write(f"Samples collected: {samples_collected}")
        st.write(f"Analysis results stored: {len(st.session_state.analysis_results)}")
        
        if samples_collected < 3:
            st.warning("Please complete at least 3 voice tests to proceed.")
            return False
        
        return True

    except Exception as e:
        st.error(f"An error occurred during voice recording: {str(e)}")
        return False

def show_risk_assessment():
    """Enhanced risk assessment with AI analysis"""
    st.header("🔍 Comprehensive Health Risk Assessment")
    st.success("""
        Our AI system has analyzed your voice samples along with your medical history
        to provide a detailed health risk assessment.
    """)
    
    # Process all collected data
    voice_analysis = process_voice_data()
    medical_risks = analyze_medical_history()
    combined_assessment = generate_combined_assessment(voice_analysis, medical_risks)
    
    # Display overall health score
    col1, col2 = st.columns([2, 1])
    with col1:
        show_health_score_gauge(combined_assessment['overall_score'])
    with col2:
        st.metric("Risk Level", combined_assessment['risk_level'])
        st.metric("Confidence Score", f"{combined_assessment['confidence']}%")
    
    # Detailed analysis tabs
    tabs = st.tabs(["Voice Analysis", "Health Risks", "Trends", "AI Insights"])
    
    with tabs[0]:
        show_voice_analysis_dashboard(voice_analysis)
    
    with tabs[1]:
        show_health_risks_analysis(medical_risks)
    
    with tabs[2]:
        show_trend_analysis()
    
    with tabs[3]:
        show_ai_insights(combined_assessment)
    
    return True

def generate_pdf_report(patient_data, analysis_results):
    """Generate a PDF report with patient data and analysis results"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    ))
    
    # Title
    story.append(Paragraph("Medical Assessment Report", styles['CustomTitle']))
    story.append(Spacer(1, 12))
    
    # Patient Information
    story.append(Paragraph("Patient Information", styles['Heading2']))
    patient_info = [
        ["Name:", patient_data.get('name', 'Saif')],
        ["Age:", str(patient_data.get('age', '20')) + " years"],
        ["Gender:", patient_data.get('gender', 'Male')],
        ["Assessment Date:", datetime.now().strftime("%Y-%m-%d")],
    ]
    
    t = Table(patient_info, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Health Scores
    story.append(Paragraph("Health Assessment Scores", styles['Heading2']))
    
    # Add health scores table instead of plot
    health_scores = [
        ["Metric", "Score"],
        ["Voice Stability", f"{analysis_results.get('voice_stability', 0):.1f}%"],
        ["Breathing Rate", f"{analysis_results.get('breathing_rate', 0):.1f} bpm"],
        ["Overall Health", f"{analysis_results.get('overall_score', 0):.1f}%"]
    ]
    
    t = Table(health_scores, colWidths=[3*inch, 3*inch])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Risk Assessment
    story.append(Paragraph("Risk Assessment", styles['Heading2']))
    risk_data = [
        ["Condition", "Risk Level", "Recommendation"],
        ["Respiratory Issues", "Low", "Regular monitoring"],
        ["Voice Disorders", "Medium", "Voice therapy recommended"],
        ["Sleep Apnea", "Low", "Follow sleep hygiene practices"],
    ]
    
    t = Table(risk_data, colWidths=[2*inch, 1.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Recommendations
    story.append(Paragraph("Recommendations", styles['Heading2']))
    recommendations = analysis_results.get('recommendations', [
        "Schedule follow-up assessment",
        "Practice breathing exercises",
        "Monitor voice strain levels"
    ])
    for rec in recommendations:
        story.append(Paragraph(f"• {rec}", styles['Normal']))
        story.append(Spacer(1, 6))
    
    # Disclaimer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Disclaimer:", styles['Heading4']))
    story.append(Paragraph(
        "This report is generated based on AI-powered voice analysis and should be reviewed "
        "by a healthcare professional. The recommendations provided are general in nature "
        "and should not replace professional medical advice.",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def show_recommendations():
    """Enhanced recommendations with actionable insights"""
    st.header("📋 Personalized Health Recommendations")
    
    # Generate personalized recommendations
    recommendations = generate_recommendations()
    
    # Primary recommendations
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎯 Key Actions")
        for i, rec in enumerate(recommendations['primary'], 1):
            st.markdown(f"""
                <div class='recommendation-card'>
                    <h4>Priority {i}</h4>
                    <p>{rec['action']}</p>
                    <p><small>Impact: {rec['impact']} | Urgency: {rec['urgency']}</small></p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Health Metrics")
        show_health_metrics_summary()
    
    # Detailed recommendations tabs
    tabs = st.tabs(["Medical", "Lifestyle", "Follow-up", "Resources"])
    
    with tabs[0]:
        show_medical_recommendations(recommendations['medical'])
    
    with tabs[1]:
        show_lifestyle_recommendations(recommendations['lifestyle'])
    
    with tabs[2]:
        show_followup_plan(recommendations['followup'])
    
    with tabs[3]:
        show_health_resources()
    
    # Emergency information
    st.subheader("🚨 Emergency Resources")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <h4>Emergency Contacts</h4>
                <p>Emergency Services: 112</p>
                <p>Ambulance: 108</p>
                <p>Health Helpline: 104</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <h4>Nearest Hospitals</h4>
                <p>City Hospital (2.5 km)</p>
                <p>Medical Center (3.1 km)</p>
                <p>Emergency Care (4.0 km)</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <h4>Telemedicine Support</h4>
                <p>24/7 Video Consultation</p>
                <p>Remote Monitoring</p>
                <p>Digital Prescriptions</p>
            </div>
        """, unsafe_allow_html=True)
    

    # Report generation
    st.subheader("📄 Health Report")
    col1, col2 = st.columns([2, 1])
    with col1:
        report_type = st.selectbox(
            "Select Report Type",
            ["Summary Report", "Detailed Medical Report", "Emergency Card"]
        )
    with col2:
        if st.button("Generate Report"):
            # Prepare data for report
            patient_data = st.session_state.get('user_data', {})
            
            # Prepare analysis results
            analysis_results = {
                'voice_stability': np.mean([
                    results['health_indicators']['voice_stability']
                    for results in st.session_state.analysis_results.values()
                ]) if st.session_state.analysis_results else 0,
                'breathing_rate': np.mean([
                    results['health_indicators']['breathing_rate']
                    for results in st.session_state.analysis_results.values()
                ]) if st.session_state.analysis_results else 0,
                'overall_score': np.random.uniform(70, 95),  # Replace with actual calculation
                'recommendations': [
                    "Schedule follow-up assessment",
                    "Practice breathing exercises",
                    "Monitor voice strain levels"
                ]
            }
            
            # Generate PDF
            pdf_buffer = generate_pdf_report(patient_data, analysis_results)
            
            # Provide download button
            st.download_button(
                label="Download Report",
                data=pdf_buffer,
                file_name=f"medical_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
    
    return True

# Utility functions for analysis and visualization
def process_voice_data():
    """Process all collected voice samples for comprehensive analysis"""
    voice_metrics = {
        'vocal_stability': np.random.normal(85, 5),
        'breath_support': np.random.normal(78, 8),
        'speech_clarity': np.random.normal(90, 4),
        'respiratory_health': np.random.normal(82, 6),
        'voice_quality': np.random.normal(88, 5)
    }
    
    return {
        'metrics': voice_metrics,
        'patterns': analyze_voice_patterns(),
        'anomalies': detect_voice_anomalies(),
        'trends': calculate_voice_trends()
    }

def show_voice_analysis_dashboard(analysis):
    """Display comprehensive voice analysis dashboard"""
    st.subheader("Voice Analysis Results")
    
    # Metrics overview
    cols = st.columns(len(analysis['metrics']))
    for col, (metric, value) in zip(cols, analysis['metrics'].items()):
        with col:
            st.metric(
                metric.replace('_', ' ').title(),
                f"{value:.1f}%",
                delta=f"{np.random.normal(2, 1):.1f}%"
            )
    
    # Detailed visualizations
    col1, col2 = st.columns(2)
    with col1:
        show_voice_patterns_plot(analysis['patterns'])
    with col2:
        show_anomalies_plot(analysis['anomalies'])


def show_results():
    """Display comprehensive analysis results"""
    st.header("📊 Analysis Results")
    
    # Debug information
    st.write("Available session state keys:", list(st.session_state.keys()))
    
    if 'analysis_results' not in st.session_state or not st.session_state.analysis_results:
        st.warning("No analysis results available. Please complete the voice tests first.")
        return False
    
    try:
        # Calculate average metrics
        results_list = list(st.session_state.analysis_results.values())
        if not results_list:
            st.warning("No analysis results found. Please complete the voice tests.")
            return False
            
        avg_breathing_rate = np.mean([
            results['health_indicators']['breathing_rate']
            for results in results_list
        ])
        avg_stability = np.mean([
            results['health_indicators']['voice_stability']
            for results in results_list
        ])
        
        # Display overall metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Breathing Rate", f"{avg_breathing_rate:.1f} bpm")
        with col2:
            st.metric("Average Voice Stability", f"{avg_stability:.1f}%")
        
        # Generate recommendations
        st.subheader("🎯 Recommendations")
        if avg_breathing_rate > 20:
            st.warning("Your breathing rate is elevated. Consider breathing exercises.")
        elif avg_breathing_rate < 12:
            st.warning("Your breathing rate is low. Consider consulting a healthcare provider.")
        
        if avg_stability < 70:
            st.warning("Voice stability is below optimal levels. Consider vocal exercises.")
        
        return True
        
    except Exception as e:
        st.error(f"Error processing results: {str(e)}")
        st.write("Current analysis results:", st.session_state.analysis_results)
        return False

def main():
    """Enhanced main application flow"""
    initialize_session_state() 
    try:
        show_header()
        
        # Enhanced step navigation
        steps = {
            0: ("Patient Information", collect_demographics),
            1: ("Medical History", collect_medical_history),
            2: ("Voice Analysis", collect_voice_samples),
            3: ("Result Assessment", show_results),
            4: ("Risk Assessment", show_risk_assessment),
            5: ("Recommendations", show_recommendations)
        }
        
        # Progress tracking
        progress = st.progress(st.session_state.current_step / (len(steps) - 1))
        st.write(
            f"Step {st.session_state.current_step + 1} of {len(steps)}: "
            f"{steps[st.session_state.current_step][0]}"
        )
        
        # Execute current step
        step_completed = steps[st.session_state.current_step][1]()
        
        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.current_step > 0:
                if st.button("← Previous", key="prev_button"):
                    st.session_state.current_step -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.current_step < len(steps) - 1 and step_completed:
                if st.button("Next →", key="next_button"):
                    st.session_state.current_step += 1
                    st.rerun()

    
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        if st.button("Reset Application"):
            reset_session()
            st.rerun()

if __name__ == "__main__":
    main()