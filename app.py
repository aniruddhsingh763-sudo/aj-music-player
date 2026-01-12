import streamlit as st
import yt_dlp
import random
import logging

# 1. Backend Clean-up: Sabhi errors block
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO UI: Neon Circuit Background & Premium Glass Layout
st.markdown("""
    <style>
    /* Exact Background: Deep Blue with Neon Purple/Green Circuit Lines */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(138, 43, 226, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(0, 255, 127, 0.1) 0%, transparent 40%),
            linear-gradient(rgba(138, 43, 226, 0.05) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(138, 43, 226, 0.05) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 35px 35px, 35px 35px;
        color: white; 
    }
    
    /* Search Bar - Top White Glass (As per Image) */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 15px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    /* Category Buttons - Neon Purple Outline with Green Bottom */
    div.stButton > button {
        background: rgba(20, 20, 40, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.6) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 60px !important;
        width: 100% !important;
        text-transform: uppercase;
        border-bottom: 3px solid #00ff7f !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important;
        box-shadow: 0 0 15px rgba(0, 255, 127, 0.5) !important;
    }

    /* Glass Panels for Songs (Rounded as per image) */
    .song-card { 
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        padding: 15px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .neon-header { 
        color: #00ff7f; 
        font-weight: 900; 
        text-transform: uppercase; 
        border-left: 5px solid #00ff7f;
        padding-left: 10px;
        margin: 25px 0 10px 0;
    }

    /* Audio Player Glow */
    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Memory for Syncing
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_q' not in st.session_state: st.session_state['last_q'] = ""

# --- 1. HEADER (Ditto Image Profile) ---
t1, t2 = st.columns([1, 4])
with t1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; height:75px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit:cover;">', unsafe_allow_html=True)
with t2:
    st.markdown("<h2 style='margin:0;'>Aj BEATs Studio</h2><small style='color:#00ff7f; letter-spacing:1px;'>UNIVERSAL STUDIO</small>", unsafe_allow_html=True)

# --- 2. SEARCH BAR (Top Layout) ---
st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search songs or artists...", label_visibility="collapsed")

# --- 3. DISCOVER MOODS (Grid Layout) ---
st.markdown("<div class='neon-header'>DISCOVER SOUNDSPHERES 🔥</div>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
mood = ""

with m1:
    if st.button("🚜 HARYANI TECHAN"):
        mood = "Latest Haryanvi Songs 2026"
with m2:
    if st.button("📻 OLD GOLD HITS"):
        mood = "90s Bollywood Evergreen"
with m3:
    if st.button("🕺 PUNJABI BEATS"):
        mood = "Top Punjabi Songs 2026"
with m4:
    if st.button("🌌 NEON PUNJABI"):
        mood = "New Punjabi Remix 2026"

final_query = user_search if user_search else (mood if mood else "Trending Bollywood 2026")

# --- 4. PLAYER ENGINE (With Loop per Song) ---
st.markdown("<div class='neon-header'>ACTIVE STUDIO 🎧</div>", unsafe_allow_html=True)

ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_q']:
            with st.spinner('Syncing...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_q'] = final_query

        for song in st.session_state['playlist']:
            with st.container():
                # Song Card ditto image jaisa
                st.markdown(f"""
                    <div class="song-card">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; border:1px solid #00ff7f; object-fit:cover;">
                            <div style="flex-grow:1;">
                                <b style="font-size:15px; color:#fff;">{song.get('title')[:55]}</b><br>
                                <small style="color:#00ff7f;">{song.get('uploader')}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # LOOP SWITCH (Ditto image jaisa player ke thik upar)
                auto_lp = st.toggle(f"AUTO-LOOP Enabled", value=True, key=f"lp_{song.get('id')}")
                st.audio(song.get('url'), format='audio/mp3', loop=auto_lp)

    except:
        st.error("Studio Sync Error! Refresh please.")

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v40.0 • No Ads</small></center>", unsafe_allow_html=True)
