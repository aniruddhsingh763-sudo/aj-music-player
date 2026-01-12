import streamlit as st
import yt_dlp
import logging

# ----------------- CONFIG -----------------
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(
    page_title="Aj Beats Studio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- GLOBAL CSS -----------------
st.markdown("""
<style>

/* FORCE MOBILE APP WIDTH */
.main .block-container {
    max-width: 420px;
    padding: 10px 14px;
    margin: auto;
}

/* BACKGROUND – NEON CIRCUIT */
.stApp { 
    background-color: #0b0b15;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(138,43,226,0.15) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(0,255,127,0.1) 0%, transparent 40%),
        linear-gradient(rgba(138,43,226,0.05) 1px, transparent 1px), 
        linear-gradient(90deg, rgba(138,43,226,0.05) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 35px 35px, 35px 35px;
    color: white; 
}

/* SEARCH BAR */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.95) !important;
    color: #111 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 12px 15px !important;
    font-weight: 600;
}

/* NEON HEADER */
.neon-header { 
    color: #00ff7f; 
    font-weight: 900; 
    text-transform: uppercase; 
    border-left: 5px solid #00ff7f;
    padding-left: 10px;
    margin: 22px 0 12px 0;
}

/* CATEGORY BUTTONS */
div.stButton > button {
    background: rgba(20,20,40,0.8) !important;
    color: white !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    height: 60px !important;
    width: 100% !important;
    border: 1px solid rgba(138,43,226,0.6) !important;
    border-bottom: 3px solid #00ff7f !important;
    box-shadow: 0 0 18px rgba(138,43,226,0.4);
}

/* SONG CARD */
.song-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(16px);
    padding: 14px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-top: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

/* IOS STYLE TOGGLE */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}
.switch input {display:none;}
.slider {
  position: absolute;
  inset: 0;
  background-color: #444;
  border-radius: 24px;
  transition: .3s;
}
.slider:before {
  content: "";
  position: absolute;
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: .3s;
}
input:checked + .slider {
  background-color: #00ff7f;
}
input:checked + .slider:before {
  transform: translateX(20px);
}

/* AUDIO PLAYER LOOK */
audio {
  width: 100%;
  filter: invert(100%) hue-rotate(90deg) brightness(1.7);
}

/* HIDE STREAMLIT UI */
#MainMenu,
