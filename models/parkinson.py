import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import parselmouth
import librosa
from nolds import dfa
import joblib
from style import apply_custom_css
# Set page config
st.set_page_config(page_title="Parkinson's Voice Detection", page_icon="🎤")

css2 = apply_custom_css()
# Enhanced CSS for better UI
st.markdown(css2, unsafe_allow_html=True)

def record_audio(duration=5, sample_rate=44100):
    """Record audio for the specified duration"""
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate,
                       channels=1)
    sd.wait()  # Wait until recording is finished
    st.write("Recording finished!")
    return audio_data, sample_rate

def save_audio(audio_data, sample_rate):
    """Save the recorded audio to a WAV file"""
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "recorded_audio.wav")
    
    # Save the audio data
    with wave.open(temp_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    
    return temp_path

def extract_features(wav_file):
    """Extract features from audio file"""
    # Load audio file
    sound = parselmouth.Sound(wav_file)
    y, sr = librosa.load(wav_file, sr=None)
    
    # Pitch analysis
    pitch = librosa.pyin(y, fmin=75, fmax=500)[0]
    
    if pitch is not None and len(pitch[~np.isnan(pitch)]) > 0:
        valid_pitch = pitch[~np.isnan(pitch)]
        fo = np.mean(valid_pitch)
        fhi = np.max(valid_pitch)
        flo = np.min(valid_pitch)
    else:
        fo = fhi = flo = 0
    
    try:
        # Create pitch object for measurements
        pitch_obj = sound.to_pitch()
        pulses = parselmouth.praat.call([sound, pitch_obj], "To PointProcess (cc)")
        
        # Jitter measurements
        jitter_percent = parselmouth.praat.call(pulses, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        jitter_abs = parselmouth.praat.call(pulses, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
        rap = parselmouth.praat.call(pulses, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
        ppq = parselmouth.praat.call(pulses, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
        ddp = 3 * rap
        
        # Shimmer calculations
        shimmer = parselmouth.praat.call([sound, pulses], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        shimmer_db = parselmouth.praat.call([sound, pulses], "Get shimmer (local, dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq3 = parselmouth.praat.call([sound, pulses], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq5 = parselmouth.praat.call([sound, pulses], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq = parselmouth.praat.call([sound, pulses], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        dda = 3 * apq3
        
    except Exception as e:
        st.error(f"Error in voice measurements: {str(e)}")
        jitter_percent = jitter_abs = rap = ppq = ddp = 0
        shimmer = shimmer_db = apq3 = apq5 = apq = dda = 0
    
    # Noise measurements
    try:
        harmonicity = sound.to_harmonicity_ac()
        hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)
        nhr = 1 / (hnr + 1e-6) if hnr > 0 else 0
    except:
        hnr = nhr = 0
    
    # Additional measures
    try:
        dfa_val = dfa(y)
    except:
        dfa_val = 0
    
    if pitch is not None and len(pitch[~np.isnan(pitch)]) > 1:
        valid_pitch = pitch[~np.isnan(pitch)]
        spread1 = np.std(valid_pitch)
        spread2 = np.mean(np.diff(valid_pitch))
        d2 = np.var(valid_pitch)
        ppe = np.std(np.log(valid_pitch + 1e-6))
    else:
        spread1 = spread2 = d2 = ppe = 0
    
    features = [
        fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp,
        shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr,
        0,  # status
        dfa_val, spread1, spread2, d2, ppe
    ]
    return np.array(features)

def predict_parkinsons(features, model_path):
    """Make prediction using the extracted features"""
    try:
        model = joblib.load(model_path)
        features_2d = features.reshape(1, -1)
        prediction = model.predict(features_2d)
        probability = model.predict_proba(features_2d)[0][1] * 100
        return prediction[0], probability
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None, None

def main():
    st.title("🎤 Parkinson's Voice Detection")
    st.write("""
    This app records your voice and analyzes it for potential signs of Parkinson's disease.
    Please speak continuously for the duration of the recording.
    """)
    
    # Model path input
    model_path = st.text_input(
        "Enter path to your model file (.pkl):",
        "parkinsons_model.pkl"
    )
    
    # Recording duration slider
    duration = st.slider(
        "Recording duration (seconds)",
        min_value=3,
        max_value=10,
        value=5
    )
    
    # Recording button
    if st.button("Start Recording"):
        if not os.path.exists(model_path):
            st.error("Model file not found. Please check the path.")
            return
            
        with st.spinner("Recording..."):
            audio_data, sample_rate = record_audio(duration=duration)
            
        # Save the audio
        with st.spinner("Processing audio..."):
            wav_path = save_audio(audio_data, sample_rate)
            st.audio(wav_path)
            
            # Extract features and make prediction
            features = extract_features(wav_path)
            prediction, probability = predict_parkinsons(features, model_path)
            
            if prediction is not None:
                # Display results
                st.header("Results")
                result = "Parkinson's Disease Detected" if prediction == 1 else "No Parkinson's Disease Detected"
                
                if prediction == 1:
                    st.error(f"Result: {result}")
                else:
                    st.success(f"Result: {result}")
                    
                st.write(f"Confidence: {probability:.2f}%")
                
                # Display key measurements
                st.subheader("Voice Measurements")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Fundamental frequency:", f"{features[0]:.2f} Hz")
                    st.write("Jitter (local):", f"{features[3]:.4f}%")
                    st.write("Shimmer (local):", f"{features[8]:.4f}%")
                with col2:
                    st.write("HNR:", f"{features[15]:.2f}")
                    st.write("DFA:", f"{features[17]:.4f}")
                
                # Cleanup
                try:
                    os.remove(wav_path)
                except:
                    pass
            else:
                st.error("Analysis failed. Please try recording again.")

if __name__ == "__main__":
    main()