def apply_custom_css():
    return """
    <style>
    /* Global Styles */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #E3FDFD 0%, #CBF1F5 100%);
    color: #2B4F4F;  /* Darker shade for better text contrast */
}

/* Header Styling */
.header-style {
    background: linear-gradient(90deg, #2B4F4F 0%, #1D3535 100%);  /* Dark teal for header */
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(113, 201, 206, 0.2);
}

.header-style h1 {
    color: #E3FDFD !important;
    font-size: 2.5rem !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header-style h2 {
    color: #CBF1F5 !important;
    font-size: 1.5rem !important;
    opacity: 0.9;
}

/* Section Headers */
[data-testid="stHeader"] {
    background-color: transparent;
}

h1, h2, h3 {
    color: #2B4F4F !important;  /* Darker teal for headers */
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}

/* Cards and Containers */
.metric-card {
    background: rgba(255, 255, 255, 0.95);  /* More opaque for better readability */
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(113, 201, 206, 0.15);
    border-left: 4px solid #71C9CE;
    transition: transform 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.recommendation-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(113, 201, 206, 0.15);
    border-left: 4px solid #71C9CE;
}

/* Input Elements */
[data-testid="stTextInput"] input, 
[data-testid="stNumberInput"] input, 
[data-testid="stSelectbox"] {
    background-color: #FFFFFF !important;
    border: 2px solid rgba(166, 227, 233, 0.4) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    color: #2B4F4F !important;  /* Darker text for better contrast */
    transition: all 0.2s ease;
}

[data-testid="stTextInput"] input:focus, 
[data-testid="stNumberInput"] input:focus {
    border-color: #71C9CE !important;
    box-shadow: 0 0 0 2px rgba(113, 201, 206, 0.2) !important;
}

/* Buttons */
[data-testid="stButton"] button {
    background: linear-gradient(90deg, #71C9CE 0%, #A6E3E9 100%) !important;
    color: #2B4F4F !important;
    border: none !important;
    padding: 0.5rem 2rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(113, 201, 206, 0.2) !important;
}

[data-testid="stButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(113, 201, 206, 0.3) !important;
}

/* Progress Bar */
[data-testid="stProgress"] {
    height: 8px !important;
    border-radius: 4px !important;
    background-color: #CBF1F5 !important;
}

[data-testid="stProgress"] > div {
    background: linear-gradient(90deg, #71C9CE 0%, #A6E3E9 100%) !important;
    border-radius: 4px !important;
}

/* Info Boxes */
[data-testid="stInfo"] {
    background: #FFFFFF !important;
    color: #2B4F4F !important;
    border: 1px solid #A6E3E9 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Warning Boxes */
[data-testid="stWarning"] {
    background: rgba(255, 247, 230, 0.9) !important;  /* Warmer tone for warnings */
    color: #2B4F4F !important;
    border: 1px solid #FFE5B4 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(113, 201, 206, 0.15);
}

[data-testid="stMetricLabel"] {
    color: #2B4F4F !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #71C9CE !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* Tabs */
[data-testid="stTabs"] {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(113, 201, 206, 0.15);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    height: 40px;
    background-color: rgba(203, 241, 245, 0.3);
    border: none !important;
    color: #2B4F4F !important;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(166, 227, 233, 0.3);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #71C9CE !important;
    color: #FFFFFF !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2B4F4F !important;
    color: #E3FDFD !important;
    padding: 2rem 1rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdown"] {
    color: #E3FDFD !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.1);
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #E3FDFD !important;
}

/* Audio Recorder */
.audio-recorder {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    box-shadow: 0 2px 4px rgba(113, 201, 206, 0.15) !important;
    border: 2px solid rgba(166, 227, 233, 0.4) !important;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.header-style, .metric-card, .recommendation-card {
    animation: fadeIn 0.5s ease-out;
}

/* Select Box and Multiselect */
[data-testid="stMultiSelect"] div[role="button"],
[data-testid="stSelectbox"] div[role="button"] {
    background-color: #FFFFFF !important;
    border: 2px solid rgba(166, 227, 233, 0.4) !important;
    color: #2B4F4F !important;
}

/* Radio Buttons and Checkboxes */
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #2B4F4F !important;
}
</style>"""