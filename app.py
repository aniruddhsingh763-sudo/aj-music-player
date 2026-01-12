import streamlit as st
import yt_dlp
import random

# Page Configuration
st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 Original UI: Grid Pattern & Neon Glass Layout
st.markdown("""
    <style>
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            linear-gradient(rgba(0, 255, 127, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 127, 0.05) 1px, transparent 1px);
        background-size: 35px 35px, 35px 35px;
        color: white; 
    }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div.stButton > button {
        background: rgba(20, 20, 40, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.6) !important;
        border-radius: 12px !important;
        height: 60px !important;
        width: 100% !important;
        border-bottom: 4px solid #00ff7f !important;
    }
    .song-card { 
        background: rgba(255,
