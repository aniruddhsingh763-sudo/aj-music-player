import streamlit as st
import yt_dlp
import random
import logging

# 1. Technical Fix: Blocking logs
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO IMAGE UI: Neon Circuit Lines Background & Premium Design
st.markdown("""
    <style>
    /* 1. EXACT CIRCUIT PATTERN (Using SVG Overlay) */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"), 
            radial-gradient(circle at 10% 20%, rgba(138, 43, 226, 0.2) 0%, transparent 45%),
            radial-gradient(circle at 90% 80%, rgba(0, 255, 127, 0.15) 0%, transparent 45%);
        background-attachment: fixed;
        color: white; 
    }
    
    /* Neon Line Pattern Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0, 255, 127, 0.05) 39px, rgba(0, 255, 127, 0.05) 40px),
                          repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0, 255, 127, 0.05) 39px, rgba(0, 255, 127, 0.05) 40px);
        pointer-events: none;
        z-index: 0;
    }

    /* 2. TOP WHITE SEARCH BAR */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 15px !important;
        font-weight: bold !important;
        position: relative;
        z-index: 10;
    }

    /* 3. NEON BUTTONS (With Green Border-Bottom) */
    div.stButton > button {
        background: rgba(15, 15, 35, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.6) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 65px !important;
        width: 100% !important;
        border-bottom: 4px solid #00ff7f !important;
        transition: 0.3s;
        position: relative;
        z-index: 10;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important;
        box-shadow: 0 0 25px rgba(0, 255, 127, 0.4) !important;
    }

    /* 4. GLASS CARDS */
    .song-card { 
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        padding: 15px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
        position: relative;
        z-index: 10;
    }
    
    .neon-title { 
        color: #00ff7f; 
        font-weight: 900; 
        border-left: 5px solid #00ff7f;
        padding-left: 12px;
        margin: 25px 0 10px 0;
    }

    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & SEARCH ---
col_logo, col_text = st.columns([1, 4])
with col_logo:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; height:75px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f;">', unsafe_allow_html=True)
with col_text:
    st.markdown("<h2 style='margin:0;'>AJ BEATS STUDIO</h2><small style='color:#00ff7f;'>DISCOVER SOUNDSPHERES</small>", unsafe_allow_html=True)

user_search = st.text_input(label="Search", placeholder="🔍 Search Singer, Song or Playlist...", label_visibility="collapsed")

# --- CATEGORIES ---
st.markdown("<div class='neon-title'>Discover Soundspheres 🔥</div>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
mood = ""

with m1:
    if st.button("🚜 HARYANI TECHAN"): mood = "Latest Haryanvi Songs 2026"
with m2:
    if st.button("📻 OLD GOLD HITS"): mood = "90s Bollywood Evergreen"
with m3:
    if st.button("🕺 PUNJABI BEATS"): mood = "Top Punjabi Songs 2026"
with m4:
    if st.button("🌌 NEON PUNJABI"): mood = "New Punjabi Remix 2026"

final_query = user_search if user_search else (mood if mood else "Bollywood Trending 2026")

# --- MUSIC ENGINE ---
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_q' not in st.session_state: st.session_state['last_q'] = ""

ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_q']:
            with st.spinner('Loading Pattern...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_q'] = final_query

        for song in st.session_state['playlist']:
            st.markdown(f"""
                <div class="song-card">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; border:1px solid #00ff7f; object-fit:cover;">
                        <div>
                            <b style="font-size:15px; color:#fff;">{song.get('title')[:55]}</b><br>
                            <small style="color:#00ff7f;">{song.get('uploader')}</small>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.audio(song.get('url'), format='audio/mp3', loop=True)
    except:
        st.error("Refresh Karo!")

st.markdown("<br><center><small style='color:#333;'>AJ BEATS v60.0 • Pattern Edition</small></center>", unsafe_allow_html=True)
