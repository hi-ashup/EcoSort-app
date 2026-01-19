import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
            /* FONTS */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Roboto+Mono:wght@400;700&display=swap');

            /* RESET & BASICS */
            .stApp {
                background-color: #05070a;
                font-family: 'Inter', sans-serif;
                color: #e0e0e0;
            }

            h1, h2, h3 {
                font-family: 'Inter', sans-serif;
                font-weight: 700;
                color: #ffffff;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            /* SIDEBAR */
            [data-testid="stSidebar"] {
                background-color: #0b0f15;
                border-right: 1px solid #111827;
            }
            [data-testid="stSidebar"] h1 {
                color: #21e065; /* THM Green */
                font-size: 24px;
            }

            /* UI COMPONENTS - CARDS */
            div.css-card {
                background-color: #111827;
                border: 1px solid #1f2937;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
                transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
            }
            div.css-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgba(33, 224, 101, 0.1);
                border-color: #21e065;
            }

            /* DIAGNOSTIC FONTS */
            .mono {
                font-family: 'Roboto Mono', monospace;
            }
            .status-ok {
                color: #21e065;
                font-weight: bold;
            }
            .status-cyber {
                color: #00a3ff;
                font-weight: bold;
            }
            .status-alert {
                color: #ef4444;
                font-weight: bold;
            }

            /* SCANNING ANIMATION FOR CAMERA */
            @keyframes scan {
                0% { top: 0%; opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { top: 100%; opacity: 0; }
            }
            .scanner-overlay {
                position: relative;
                width: 100%;
                height: 4px;
                background: #21e065;
                box-shadow: 0 0 10px #21e065;
                animation: scan 3s infinite linear;
                z-index: 10;
            }

            /* TABS Styling */
            button[data-baseweb="tab"] {
                background-color: transparent !important;
                color: #9ca3af !important;
                border-bottom: 2px solid transparent;
                font-family: 'Roboto Mono', monospace;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #21e065 !important;
                border-bottom: 2px solid #21e065;
            }

            /* METRIC CONTAINERS */
            div[data-testid="stMetricValue"] {
                color: #00a3ff;
                font-family: 'Roboto Mono', monospace;
            }

            /* PROGRESS BARS */
            .stProgress > div > div > div > div {
                background-color: #21e065;
            }
        </style>
    """, unsafe_allow_html=True)

def card_start(title=None, border_color="#1f2937"):
    """Starts a visual HTML card."""
    title_html = f"<h4 style='color:{border_color}; margin-top:0'>{title}</h4>" if title else ""
    st.markdown(f"""
    <div class="css-card" style="border-left: 3px solid {border_color}">
    {title_html}
    """, unsafe_allow_html=True)

def card_end():
    """Ends the visual HTML card."""
    st.markdown("</div>", unsafe_allow_html=True)