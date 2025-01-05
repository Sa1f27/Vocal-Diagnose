def apply_custom_css():
    return """
    <style>
    /* Global Styles */
    [data-testid="stAppViewContainer"], 
    [data-testid="stMarkdown"] {
        background: linear-gradient(135deg, #FAF3E0 0%, #E8E1C8 100%);
    }

    /* Labels and Headers - Dark */
    label,
    [data-testid="stLabel"],
    [data-testid="stSelectbox"] label,
    [data-testid="stMultiSelect"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stDateInput"] label,
    [data-testid="stTimeInput"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stFileUploader"] label,
    [data-testid="stSearchBox"] label {
        color: #1A237E !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.5);
    }

    /* Input Field Text Colors */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stFileUploader"] input,
    [data-testid="stSearchBox"] input {
        background-color: #6B8E23 !important;  /* Olive background */
        border: 2px solid #556B2F !important;
        color: #FFFFFF !important;  /* White text */
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }

    /* Select Boxes and Multiselect */
    [data-testid="stSelectbox"] > div[role="button"],
    [data-testid="stMultiSelect"] > div[role="button"] {
        background-color: #6B8E23 !important;
        border: 2px solid #556B2F !important;
        color: #FFFFFF !important;
    }

    /* Dropdown options */
    [data-testid="stSelectbox"] ul,
    [data-testid="stMultiSelect"] ul {
        background-color: #6B8E23 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSelectbox"] ul li,
    [data-testid="stMultiSelect"] ul li {
        color: #FFFFFF !important;
    }

    /* Selected options in multiselect */
    [data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #556B2F !important;
        color: #FFFFFF !important;
    }

    /* Multiselect selected items text */
    [data-testid="stMultiSelect"] div[data-baseweb="tag"] span {
        color: #FFFFFF !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stHeader"] {
        color: #1A237E !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.5);
    }

    /* Regular text */
    [data-testid="stMarkdown"] p,
    [data-testid="stText"] p,
    .element-container {
        color: #2C3E50 !important;
    }

    /* Placeholder text */
    input::placeholder,
    textarea::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }

    /* Focus states */
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stSelectbox"] > div[role="button"]:focus,
    [data-testid="stMultiSelect"] > div[role="button"]:focus {
        border-color: #8BA978 !important;
        box-shadow: 0 0 0 2px rgba(139, 169, 120, 0.2) !important;
    }

    /* Caption Text */
    [data-testid="stCaption"] {
        color: #1A237E !important;
        font-weight: 600 !important;
    }

    /* Data Tables */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
    }

    [data-testid="stTable"] {
        background-color: #FFFFFF !important;
    }

    /* Alerts & Messages */
    [data-testid="stSuccess"] {
        background-color: #DFF2BF !important;
        color: #4F8A10 !important;
        border: 2px solid #4F8A10 !important;
    }

    [data-testid="stInfo"] {
        background-color: #FFFFFF !important;
        color: #2C3E50 !important; /* Dark Text */
        border: 2px solid #6B8E23 !important;
    }

    [data-testid="stWarning"] {
        background-color: #FEEFB3 !important;
        color: #9F6000 !important;
        border: 2px solid #9F6000 !important;
    }

    [data-testid="stError"] {
        background-color: #FFD2D2 !important;
        color: #D8000C !important;
        border: 2px solid #D8000C !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E8E1C8 !important;
        border-right: 2px solid #6B8E23 !important;
    }

    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 2px solid #6B8E23 !important;
        border-radius: 8px !important;
    }

    /* Code Blocks */
    [data-testid="stCodeBlock"] {
        background-color: #FFFFFF !important;
        border: 2px solid #6B8E23 !important;
        border-radius: 8px !important;
    }

    /* Forms */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 2px solid #6B8E23 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* Progress Bar */
    [data-testid="stProgress"] > div {
        background-color: #6B8E23 !important;
    }

    /* Tooltips */
    [data-testid="stTooltipIcon"] {
        color: #6B8E23 !important;
    }

    /* Status */
    [data-testid="stStatus"] {
        background-color: #FFFFFF !important;
        border: 2px solid #6B8E23 !important;
    }

    /* Spinner */
    [data-testid="stSpinner"] {
        color: #6B8E23 !important;
    }

    /* Buttons */
    button[data-testid="stButton"] {
        color: #FFFFFF !important; /* Light Text */
        background-color: #6B8E23 !important;
        border: 2px solid #556B2F !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }

    button[data-testid="stButton"]:hover {
        background-color: #8BA978 !important;
    }

    /* Special Containers */
    .metric-card, .recommendation-card {
        background-color: #FFFFFF;
        border: 2px solid #6B8E23;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Charts and Plots */
    [data-testid="stVegaLiteChart"],
    [data-testid="stPlotlyChart"] {
        background-color: #FFFFFF !important;
        border: 2px solid #6B8E23 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    </style>
    """
