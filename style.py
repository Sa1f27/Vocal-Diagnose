import streamlit as st

def apply_styles():
    st.markdown(
        """<style>
        /* Background color */
        .stApp {
            background-color: #F5EFFF;
        }

        /* Headers and subheaders */
        h1, h2, h3 {
            color: #A294F9;
            font-family: 'Arial', sans-serif;
        }

        /* Text and labels */
        p, label, .stMarkdown {
            color: #4A4A4A;
            font-family: 'Verdana', sans-serif;
        }

        /* Buttons */
        .stButton > button {
            background-color: #A294F9;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 16px;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #8A76E5;
        }

        /* Tabs */
        div[data-testid="stHorizontalBlock"] > div {
            background-color: #ECE8FF;
            border-radius: 10px;
            padding: 5px;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: #D9CBFF;
        }

        /* File uploader */
        .stFileUploader {
            background-color: #ECE8FF;
            border: 2px dashed #A294F9;
        }

        /* Success messages */
        .stSuccess {
            background-color: #E5F8E0;
            border-left: 4px solid #52B788;
        }

        /* Error messages */
        .stError {
            background-color: #FFE2E2;
            border-left: 4px solid #E74C3C;
        }

        </style>""",
        unsafe_allow_html=True
    )
