import streamlit as st
import pandas as pd
import time
from modules.styles import load_custom_css, card_start, card_end
from modules.gemini_vision import analyze_image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD STYLES ---
load_custom_css()

# --- STATE MANAGEMENT ---
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "is_analyzing" not in st.session_state:
    st.session_state.is_analyzing = False

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown("<h1>ECO<span style='color:white'>SORT</span> <span style='font-size:0.6em; color:#00a3ff; vertical-align:super'>V1.0</span></h1>", unsafe_allow_html=True)
    
    st.markdown("### 🔑 SECURITY NODE")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter Google Gemini API Key")
    
    if not api_key:
        st.warning("⚠️ API KEY REQUIRED")
    else:
        st.success("🟢 SYSTEM ONLINE")
        
    st.markdown("---")
    st.markdown("<div class='mono' style='font-size:12px; color:#6b7280'>SYS_ID: ES-2025-X1<br>STATUS: MONITORING</div>", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
# 2 Columns: Optical HUD (Input) | Diagnostic Report (Output)
col_left, col_right = st.columns([1, 1.5], gap="large")

with col_left:
    st.markdown("### 👁️ OPTICAL FEED")
    
    tab_cam, tab_up = st.tabs(["LIVE FEED", "DATA UPLOAD"])
    
    img_input = None
    
    with tab_cam:
        # Camera logic
        cam_img = st.camera_input("Scanner Active")
        if cam_img:
            img_input = cam_img
            
    with tab_up:
        # Upload logic
        up_img = st.file_uploader("Upload Artifact", type=["jpg", "png", "jpeg"])
        if up_img:
            img_input = up_img

    if img_input:
        # Simulate Scanning UI
        st.markdown(f'<div class="scanner-overlay"></div>', unsafe_allow_html=True)
        st.image(img_input, caption="TARGET LOCKED", use_container_width=True)
        
        analyze_btn = st.button("INITIATE NEURAL ANALYSIS", type="primary", use_container_width=True)
        
        if analyze_btn:
            if not api_key:
                st.error("ACCESS DENIED: MISSING API KEY")
            else:
                with st.spinner("PROCESSING NEURAL HANDSHAKE..."):
                    # Simulate scan delay for effect
                    time.sleep(1.5)
                    st.session_state.analysis_data = analyze_image(img_input, api_key)

# --- RIGHT COLUMN: ANALYSIS REPORT ---
with col_right:
    st.markdown("### 📊 DIAGNOSTIC REPORT")

    data = st.session_state.analysis_data

    if data:
        if "error" in data:
            st.error(f"SYSTEM FAILURE: {data['error']}")
        else:
            # 1. HEADER SECTION
            row1_1, row1_2, row1_3 = st.columns(3)
            with row1_1:
                card_start(border_color="#00a3ff")
                st.markdown(f"<div class='mono' style='font-size:12px'>DETECTED OBJECT</div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:white; margin:0'>{data.get('itemName', 'Unknown')}</h3>", unsafe_allow_html=True)
                card_end()
            with row1_2:
                card_start(border_color="#21e065")
                score = data.get('recyclabilityScore', 0)
                st.markdown(f"<div class='mono' style='font-size:12px'>RECYCLABILITY</div>", unsafe_allow_html=True)
                st.metric("Index", f"{score}%", label_visibility="collapsed")
                card_end()
            with row1_3:
                # Bin Color logic
                bin_color = data.get('dustbinColor', 'General')
                css_color = {"Green": "#22c55e", "Blue": "#3b82f6", "Red": "#ef4444", "Yellow": "#eab308"}.get(bin_color, "#6b7280")
                card_start(border_color=css_color)
                st.markdown(f"<div class='mono' style='font-size:12px'>DISPOSAL PROTOCOL</div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:{css_color}; margin:0'>BIN: {bin_color.upper()}</h3>", unsafe_allow_html=True)
                card_end()

            st.markdown("<br>", unsafe_allow_html=True)

            # 2. INTELLIGENCE TABS
            tab1, tab2, tab3 = st.tabs(["🧬 MATERIAL INTEL", "🛡️ DISPOSAL", "💡 UPCYCLING LAB"])

            with tab1:
                st.markdown("##### MATERIAL BREAKDOWN")
                materials = data.get('materialComposition', [])
                if materials:
                    for item in materials:
                        st.text(f"{item['material'].upper()}")
                        st.progress(item['percentage'] / 100)
                else:
                    st.info("No detailed composition data available.")
                
                card_start("Environmental Impact", border_color="#ef4444")
                st.write(data.get('environmentalImpact', 'Calculating...'))
                card_end()

            with tab2:
                st.markdown("##### STEP-BY-STEP PROTOCOL")
                steps = data.get('disposalInstructions', [])
                for i, step in enumerate(steps):
                    card_start()
                    st.markdown(f"<span class='mono' style='color:#00a3ff'>STEP 0{i+1}:</span> {step}", unsafe_allow_html=True)
                    card_end()

            with tab3:
                st.markdown("##### R&D PROJECTS")
                ideas = data.get('upcyclingIdeas', [])
                for idea in ideas:
                    with st.expander(f"✨ PROJECT: {idea.get('title', 'Project')}"):
                        st.markdown(f"**Difficulty:** {idea.get('difficulty', 'Unknown')}")
                        st.write(idea.get('description'))

    else:
        # IDLE STATE VISUAL
        card_start(border_color="#111827")
        st.markdown("""
        <div style='text-align: center; color: #374151; padding: 50px;'>
            <h3>AWAITING INPUT</h3>
            <p class='mono'>Connect camera or upload data to initialize system.</p>
        </div>
        """, unsafe_allow_html=True)
        card_end()