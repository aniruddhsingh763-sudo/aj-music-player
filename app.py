import streamlit as st
import yt_dlp
import random
import logging

# 1. Technical Cleanup: Errors ko chupane ke liye
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO UI: Pattern, Colors, and Buttons
st.markdown("""
    <style>
    /* Exact Circuit Grid Background */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            linear-gradient(rgba(0, 255, 127, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 127, 0.05) 1px, transparent 1px);
        background-size: 35px 35px, 35px 35px;
        color: white; 
    }
    
    /* Search Bar - White Glass (Top) */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }

    /* Mood Buttons - Neon Grid with Green Bottom */
    div.stButton > button {
        background: rgba(20, 20, 40, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.6) !important;
        border-radius: 12px !important;
        height: 60px !important;
        width: 100% !important;
        border-bottom: 4px solid #00ff7f !important;
        text-transform: uppercase;
        font-weight: 800 !important;
    }

    /* Song Card Design - Rounded Glass */
    .song-box { 
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        padding: 15px; 
        border-radius: 18px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
    }
    
    .neon-label { 
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

# Session State for Search Persistence
if 'playlist' not in st.session_state: st.session_state.playlist = []
if 'last_q' not in st.session_state: st.session_state.last_q = ""

# --- 1. HEADER & SEARCH (Position: Top) ---
t_col1, t_col2 = st.columns([1, 4])
with t_col1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; height:75px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit: cover;">', unsafe_allow_html=True)
with t_col2:
    st.markdown("<h2 style='margin:0;'>AJ BEATS STUDIO</h2><small style='color:#00ff7f;'>DISCOVER SOUNDSPHERES</small>", unsafe_allow_html=True)

user_q = st.text_input("", placeholder="🔍 Search songs, artists or playlists...", key="top_search")

# --- 2. MOOD GRID ---
st.markdown("<div class='neon-label'>Discover Soundspheres 🔥</div>", unsafe_allow_html=True)
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

# Priority logic for Search
final_q = mood if mood else (user_q if user_q else "Trending Bollywood 2026")

# --- 3. FETCH MUSIC ---
if final_q != st.session_state.last_q:
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'default_search': 'ytsearch15', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            with st.spinner('Syncing Studio...'):
                data = ydl.extract_info(final_q, download=False)
                st.session_state.playlist = [e for e in data['entries'] if e is not None]
                st.session_state.last_q = final_q
        except:
            st.error("Connection Error! Refresh Karo.")

# --- 4. CONTROLS (Suffer & Fetch) ---
st.write("---")
c_suf, c_fch = st.columns([1, 1])
with c_suf:
    shuffle_on = st.toggle("🔀 SUFFER Mode")
with c_fch:
    if st.button("🚀 FETCH NOW"):
        st.session_state.last_q = "" # Reset to force fetch
        st.rerun()

# --- 5. INDIVIDUAL PLAYER ENGINE ---
st.markdown("<div class='neon-label'>Active Playlist 🎧</div>", unsafe_allow_html=True)

songs = list(st.session_state.playlist)
if shuffle_on:
    random.shuffle(songs)

for song in songs:
    with st.container():
        # Song Card ditto image jaisa
        st.markdown(f"""
            <div class="song-box">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; border:1px solid #00ff7f; object-fit:cover;">
                    <div style="flex-grow:1;">
                        <b style="font-size:16px; color:#fff;">{song.get('title')[:60]}</b><br>
                        <small style="color:#00ff7f;">{song.get('uploader')}</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 🔥 INDIVIDUAL LOOP SWITCH (Har song pe alag)
        loop_this = st.toggle(f"AUTO-LOOP Enabled", value=True, key=f"lp_{song.get('id')}")
        
        # Audio Player
        st.audio(song.get('url'), format='audio/mp3', loop=loop_this)

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v120.0 • No Overlap Fix</small></center>", unsafe_allow_html=True)
