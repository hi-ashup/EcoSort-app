import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
            /* FONTS & GLOBAL SETTINGS */
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

            .stApp {
                background-color: #0E1117; /* Very Dark Blue-Grey */
                font-family: 'Outfit', sans-serif;
            }

            /* TEXT OVERRIDES */
            h1, h2, h3, h4, h5, h6 {
                color: #FFFFFF !important;
                font-weight: 600;
            }
            p, div, label, span {
                color: #e2e8f0; /* Light Gray for readability */
            }

            /* CUSTOM CARD CONTAINER */
            div.css-card {
                background-color: #1e2430; /* Lighter than background */
                border: 1px solid #2d3748;
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            div.css-card:hover {
                border-color: #34d399; /* Green Hover */
                transform: translateY(-2px);
            }

            /* SIDEBAR STYLING */
            [data-testid="stSidebar"] {
                background-color: #11151c;
                border-right: 1px solid #1f2937;
            }

            /* BUTTONS - GREEN PRIMARY */
            div.stButton > button {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white !important;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 1rem;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.39);
            }
            div.stButton > button:hover {
                background: #34d399;
                transform: scale(1.02);
            }

            /* CUSTOM TABS (Like the reference left menu) */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                background-color: transparent;
                border-radius: 8px;
                color: #94a3b8;
                font-weight: 600;
            }
            .stTabs [aria-selected="true"] {
                background-color: #1e293b;
                color: #34d399 !important; /* Neon Green */
                border-bottom-color: #34d399;
            }

            /* PROGRESS BAR */
            .stProgress > div > div > div > div {
                background-color: #facc15; /* Yellow */
            }

            /* INPUT FIELDS */
            .stTextInput > div > div > input {
                background-color: #1e293b;
                color: white;
                border-radius: 8px;
                border: 1px solid #334155;
            }

            /* SCANNER ANIMATION REDUCED OPACITY (Cleaner look) */
            @keyframes scan {
                0% { top: 0%; opacity: 0; }
                50% { opacity: 0.5; }
                100% { top: 100%; opacity: 0; }
            }
            .scanner-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(to bottom, transparent, rgba(52, 211, 153, 0.2), transparent);
                animation: scan 3s infinite linear;
                pointer-events: none;
                border-radius: 12px;
            }
            
            /* BADGES & STATUS */
            .highlight-green {
                color: #34d399;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            .highlight-yellow {
                color: #facc15;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
        </style>
    """, unsafe_allow_html=True)

def card_container(content):
    st.markdown(f"""
    <div class="css-card">
        {content}
    </div>
    """, unsafe_allow_html=True)

def custom_metric(label, value, color="#ffffff"):
    st.markdown(f"""
    <div style="display: flex; flex-direction: column;">
        <span style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">{label}</span>
        <span style="font-size: 1.5rem; font-weight: 700; color: {color};">{value}</span>
    </div>
    """, unsafe_allow_html=True)