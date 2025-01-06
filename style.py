def apply_custom_css():
    return """
    <style>
    /* Global Styles - Premium Dark Theme */
    [data-testid="stAppViewContainer"], 
    [data-testid="stMarkdown"] {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }

    /* Labels and Headers */
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
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        letter-spacing: 0.025em !important;
        margin-bottom: 0.5rem !important;
    }

    /* Input Field Text Colors */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stFileUploader"] input,
    [data-testid="stSearchBox"] input {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.975rem !important;
        transition: all 0.15s ease-in-out !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }

    /* Select Boxes and Multiselect */
    [data-testid="stSelectbox"] > div[role="button"],
    [data-testid="stMultiSelect"] > div[role="button"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }

    /* Dropdown options */
    [data-testid="stSelectbox"] ul,
    [data-testid="stMultiSelect"] ul {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }

    [data-testid="stSelectbox"] ul li:hover,
    [data-testid="stMultiSelect"] ul li:hover {
        background-color: #2D3F5D !important;
    }

    /* Selected options in multiselect */
    [data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #3B82F6 !important;
        border: none !important;
        border-radius: 4px !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stHeader"] {
        color: #F1F5F9 !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.3 !important;
    }

    h1 { font-size: 2.25rem !important; }
    h2 { font-size: 1.875rem !important; }
    h3 { font-size: 1.5rem !important; }
    h4 { font-size: 1.25rem !important; }
    h5 { font-size: 1.125rem !important; }
    h6 { font-size: 1rem !important; }

    /* Regular text */
    [data-testid="stMarkdown"] p,
    [data-testid="stText"] p,
    .element-container {
        color: #CBD5E1 !important;
        line-height: 1.6 !important;
    }

    /* Focus states */
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stSelectbox"] > div[role="button"]:focus,
    [data-testid="stMultiSelect"] > div[role="button"]:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        outline: none !important;
    }

    /* Data Tables */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* Alerts & Messages */
    [data-testid="stSuccess"] {
        background-color: rgba(16, 185, 129, 0.1) !important;
        color: #10B981 !important;
        border: 1px solid #10B981 !important;
    }

    [data-testid="stInfo"] {
        background-color: rgba(59, 130, 246, 0.1) !important;
        color: #60A5FA !important;
        border: 1px solid #3B82F6 !important;
    }

    [data-testid="stWarning"] {
        background-color: rgba(245, 158, 11, 0.1) !important;
        color: #F59E0B !important;
        border: 1px solid #F59E0B !important;
    }

    [data-testid="stError"] {
        background-color: rgba(239, 68, 68, 0.1) !important;
        color: #EF4444 !important;
        border: 1px solid #EF4444 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #334155 !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Code Blocks */
    [data-testid="stCodeBlock"] {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* Progress Bar */
    [data-testid="stProgress"] > div {
        background: linear-gradient(90deg, #3B82F6, #60A5FA) !important;
        border-radius: 999px !important;
    }

    /* Charts and Plots */
    [data-testid="stVegaLiteChart"],
    [data-testid="stPlotlyChart"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Special Containers */
    .metric-card, .recommendation-card {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Tooltips */
    [data-testid="stTooltipIcon"] {
        color: #60A5FA !important;
    }

    /* Mobile Optimization */
    @media (max-width: 768px) {
        h1 { font-size: 1.875rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }
        h4 { font-size: 1.125rem !important; }
        h5, h6 { font-size: 1rem !important; }
    }

    /* Hover Effects */
    [data-testid="stTextInput"] input:hover,
    [data-testid="stNumberInput"] input:hover,
    [data-testid="stTextArea"] textarea:hover,
    [data-testid="stSelectbox"] > div[role="button"]:hover,
    [data-testid="stMultiSelect"] > div[role="button"]:hover {
        border-color: #475569 !important;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1E293B;
    }

    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #64748B;
    }
    </style>
    """