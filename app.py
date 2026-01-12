import streamlit as st
import yt_dlp
import random
import logging

# 1. Background fix
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 EXACT UI: Circuit Pattern, Neon Glow & Image Buttons
st.markdown("""
    <style>
    /* Exact Background: Deep Blue with Neon Grid Lines */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            linear-gradient(rgba(0, 255, 127, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 127, 0.05) 1px, transparent 1px),
            radial-gradient(circle at 15% 15%, rgba(138, 43, 226, 0.15) 0%, transparent 40%);
        background-size: 35px 35px, 35px 35px, 100% 100%;
        color: white; 
    }
    
    /* Search Bar - White Glass (Top) */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-weight: bold !important;
    }

    /* Neon Buttons: Image Style with Green Bottom */
    div.stButton > button {
        background: rgba(20, 20, 40, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.5) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 60px !important;
        width: 100% !important;
        border-bottom: 4px solid #00ff7f !important;
        text-transform: uppercase;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.5) !important;
    }

    /* Glass Song Cards */
    .song-box { 
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        padding: 15px; 
        border-radius: 18px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
    }
    
    .neon-text { 
        color: #00ff7f; 
        font-weight: 900; 
        border-left: 5px solid #00ff7f;
        padding-left: 10px;
        margin: 20px 0 10px 0;
    }

    /* Player Adjustments */
    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 8px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Memory
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_q' not in st.session_state: st.session_state['last_q'] = ""

# --- 1. HEADER & SEARCH ---
h1, h2 = st.columns([1, 4])
with h1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:70px; height:70px; border-radius:50%; border:2px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit:cover;">', unsafe_allow_html=True)
with h2:
    st.
