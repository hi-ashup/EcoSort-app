import streamlit as st
import time
from modules.styles import load_custom_css, custom_metric
from modules.gemini_vision import analyze_image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EcoScan Intelligent Sorter",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

load_custom_css()

# --- INITIALIZATION ---
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

# --- HEADER (Matches the reference 'EcoScan' top bar) ---
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    # Mimic the logo in reference
    st.markdown("""
    <div style='background: #34d399; padding: 10px; border-radius: 8px; display: inline-block; box-shadow: 0 0 15px rgba(52,211,153,0.5);'>
        <h2 style='margin:0; color:#111827 !important;'>♻️</h2>
    </div>
    """, unsafe_allow_html=True)
with col_head2:
    st.markdown("<h2 style='padding-top: 10px;'>EcoScan <span style='color:#34d399'>Neural Sorter</span></h2>", unsafe_allow_html=True)

st.markdown("---")

# --- MAIN WORKSPACE ---
col_left, col_right = st.columns([1, 1.2], gap="large")

# LEFT COLUMN: INPUT & PREVIEW
with col_left:
    st.markdown("#### 📡 OPTICAL INPUT")
    
    # Input Area - Dark Card
    with st.container():
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        
        # Dual Input Toggle
        mode = st.radio("Input Source", ["Live Camera", "Upload File"], horizontal=True, label_visibility="collapsed")
        
        img_file = None
        if mode == "Live Camera":
            img_file = st.camera_input("Scanner Feed")
        else:
            img_file = st.file_uploader("Drop file here", type=['jpg', 'png', 'jpeg'])

        # Show Scan Button if image present
        if img_file:
            st.markdown("---")
            # Image Preview styled
            st.image(img_file, use_container_width=True, caption="TARGET ACQUIRED")
            
            # API Key Input (Cleaner)
            api_key = st.text_input("Enter Gemini API Key", type="password", placeholder="Paste key to activate scanner")
            
            if st.button("RUN NEURAL ANALYSIS", use_container_width=True):
                if not api_key:
                    st.warning("⚠️ API KEY REQUIRED")
                else:
                    with st.spinner("SCANNING MOLECULAR STRUCTURE..."):
                        # Short delay for effect
                        time.sleep(1)
                        result = analyze_image(img_file, api_key)
                        st.session_state.analysis_data = result
                        st.rerun()
                        
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN: RESULTS (Based on reference layout)
with col_right:
    data = st.session_state.analysis_data
    
    if data:
        if "error" in data:
            st.error(data['error'])
        else:
            # --- MAIN CLASSIFICATION CARD ---
            # Using HTML to mimic that big Yellow icon and text in reference
            bin_color = data.get('dustbinColor', 'General')
            # Mapping color names to hex for the Glow
            glow_map = {"Green": "#22c55e", "Blue": "#3b82f6", "Red": "#ef4444", "Yellow": "#facc15"}
            active_glow = glow_map.get(bin_color, "#94a3b8")

            st.markdown(f"""
            <div class="css-card" style="border-left: 5px solid {active_glow};">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <div style="
                        background-color: {active_glow}; 
                        width: 60px; height: 60px; 
                        border-radius: 12px; 
                        display: flex; align-items: center; justify-content: center;
                        font-size: 30px;
                        box-shadow: 0 0 20px {active_glow}80;
                        color: #111;">
                        🗑️
                    </div>
                    <div>
                        <span style="font-size: 0.9rem; color: {active_glow}; font-weight: bold; letter-spacing: 1px;">IDENTIFICATION SUCCESS</span>
                        <h2 style="margin: 0;">{data.get('itemName', 'Object')}</h2>
                        <p style="margin: 0; color: #94a3b8;">{data.get('category', 'Unknown Material')}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- STATS ROW ---
            row1, row2 = st.columns(2)
            with row1:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                custom_metric("Recyclability", f"{data.get('recyclabilityScore')}%", "#34d399")
                st.progress(data.get('recyclabilityScore')/100)
                st.markdown('</div>', unsafe_allow_html=True)
            with row2:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                custom_metric("Disposal Bin", bin_color.upper(), active_glow)
                st.caption(f"Requires {bin_color} Sorting Stream")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- DETAILED INFO TABS (Reference Left-style Nav implemented as tabs) ---
            tab_mat, tab_how, tab_eco = st.tabs(["🧬 COMPOSITION", "📋 INSTRUCTIONS", "💡 UPCYCLING"])
            
            with tab_mat:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                for m in data.get('materialComposition', []):
                    st.write(f"**{m.get('material')}**")
                    st.progress(m.get('percentage', 0)/100)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab_how:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                for idx, step in enumerate(data.get('disposalInstructions', [])):
                    st.info(f"Step {idx+1}: {step}")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab_eco:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                for idea in data.get('upcyclingIdeas', []):
                    st.markdown(f"#### {idea.get('title')}")
                    st.caption(f"Difficulty: {idea.get('difficulty')}")
                    st.write(idea.get('description'))
                    st.divider()
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        # IDLE STATE
        st.markdown("""
        <div class="css-card" style="text-align: center; padding: 50px; opacity: 0.7;">
            <h3>Awaiting Data Stream</h3>
            <p>Upload an image or activate the optical scanner to begin analysis.</p>
        </div>
        """, unsafe_allow_html=True)