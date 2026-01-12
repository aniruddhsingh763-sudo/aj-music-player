import streamlit as st
import yt_dlp
import random

# 1. Page Config
st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 2. DITTO UI & JAVASCRIPT (Multi-Play Prevention)
st.markdown("""
    <style>
    .stApp { 
        background-color: #0b0b15;
        background-image: linear-gradient(rgba(0, 255, 127, 0.05) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 127, 0.05) 1px, transparent 1px);
        background-size: 35px 35px, 35px 35px;
    }
    .song-card { 
        background: rgba(255, 255, 255, 0.06);
        padding: 15px; border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 10px;
    }
    div.stButton > button {
        background: rgba(20, 20, 40, 0.9) !important;
        border-bottom: 4px solid #00ff7f !important;
        color: white !important; font-weight: bold; height: 60px; width: 100%;
    }
    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.5); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    
    <script>
    // System/Mobile Multi-play prevention
    document.addEventListener('play', function(e){
        var audios = document.getElementsByTagName('audio');
        for(var i = 0, len = audios.length; i < len; i++){
            if(audios[i] != e.target){
                audios[i].pause();
            }
        }
    }, true);
    </script>
    """, unsafe_allow_html=True)

# 3. Session State
if 'playlist' not in st.session_state: st.session_state.playlist = []
if 'search_q' not in st.session_state: st.session_state.search_q = "New Haryanvi Techan 2026"

# --- SEARCH & MOODS ---
st.markdown("<h2 style='text-align: center; color: white;'>Aj BEATs Studio 🎧</h2>", unsafe_allow_html=True)
search_val = st.text_input("", placeholder="🔍 Search songs or artists...", key="search_bar")

if search_val and search_val != st.session_state.search_q:
    st.session_state.search_q = search_val
    st.session_state.playlist = []

m1, m2, m3, m4 = st.columns(4)
mood = ""
with m1: 
    if st.button("🚜 HARYANI"): mood = "Haryanvi Techan 2026"
with m2: 
    if st.button("🕺 PUNJABI"): mood = "Top Punjabi 2026"
with m3: 
    if st.button("📻 OLD GOLD"): mood = "90s Bollywood Hits"
with m4: 
    if st.button("🌌 NEON"): mood = "New Punjabi Remix"

if mood:
    st.session_state.search_q = mood
    st.session_state.playlist = []
    st.rerun()

# --- FETCH & DISPLAY ---
if not st.session_state.playlist:
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'default_search': 'ytsearch15', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            with st.spinner('Syncing...'):
                info = ydl.extract_info(st.session_state.search_q, download=False)
                st.session_state.playlist = [e for e in info['entries'] if e is not None]
        except: st.error("Slow Internet!")

# Controls
st.write("---")
c1, c2 = st.columns(2)
with c1: shuffle = st.toggle("🔀 SUFFER Mode")
with c2: 
    if st.button("🚀 FETCH NEW"): st.session_state.playlist = []; st.rerun()

# Playlist
songs = list(st.session_state.playlist)
if shuffle: random.shuffle(songs)

for song in songs:
    with st.container():
        st.markdown(f"""
            <div class="song-card">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="{song.get('thumbnail')}" style="width:60px; height:60px; border-radius:10px; border:1px solid #00ff7f; object-fit:cover;">
                    <div>
                        <b style="color:white; font-size:15px;">{song.get('title')[:55]}</b><br>
                        <small style="color:#00ff7f;">{song.get('uploader')}</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        loop_this = st.toggle("AUTO-LOOP Enabled", value=True, key=f"loop_{song.get('id')}")
        st.audio(song.get('url'), format='audio/mp3', loop=loop_this)

st.markdown("<br><center><small style='color:gray;'>AJ BEATS • v180.0 • Verified</small></center>", unsafe_allow_html=True)
