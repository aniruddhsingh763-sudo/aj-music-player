import streamlit as st
import yt_dlp
import random

# Page config
st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO UI: Exact Grid Pattern & Neon Glass Layout
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
        height: 65px !important;
        width: 100% !important;
        border-bottom: 4px solid #00ff7f !important;
        font-weight: 800 !important;
    }
    .song-card { 
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        padding: 15px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
    }
    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'playlist' not in st.session_state: st.session_state.playlist = []
if 'search_query' not in st.session_state: st.session_state.search_query = "New Bollywood 2026"

# 1. Header (Profile Picture)
t1, t2 = st.columns([1, 4])
with t1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; height:75px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit: cover;">', unsafe_allow_html=True)
with t2:
    st.markdown("<h2 style='margin:0;'>Aj BEATs Studio</h2><small style='color:#00ff7f;'>THE MUSIC STUDIO</small>", unsafe_allow_html=True)

# 2. Search Bar (TOP - Working Fix)
search_input = st.text_input("", placeholder="🔍 Search songs, artists or playlists...", key="main_search")
if search_input and search_input != st.session_state.search_query:
    st.session_state.search_query = search_input
    st.session_state.playlist = [] # Clear old results

# 3. Discover Moods (Grid Layout)
st.markdown("<h4 style='color: #00ff7f; border-left: 5px solid #00ff7f; padding-left: 10px;'>DISCOVER SOUNDSPHERES 🔥</h4>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)

mood_q = ""
with m1: 
    if st.button("🚜 HARYANI TECHAN"): mood_q = "Latest Haryanvi 2026"
with m2: 
    if st.button("📻 OLD GOLD HITS"): mood_q = "90s Bollywood Hits"
with m3: 
    if st.button("🕺 PUNJABI BEATS"): mood_q = "Top Punjabi 2026"
with m4: 
    if st.button("🌌 NEON PUNJABI"): mood_q = "New Punjabi Remix"

if mood_q:
    st.session_state.search_query = mood_q
    st.session_state.playlist = []
    st.rerun()

# 4. Fetch Music Engine
if not st.session_state.playlist:
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'default_search': 'ytsearch15', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            with st.spinner('Syncing...'):
                info = ydl.extract_info(st.session_state.search_query, download=False)
                st.session_state.playlist = [e for e in info['entries'] if e is not None]
        except: st.error("Sync Error! Refresh please.")

# 5. Global Controls (Suffer & Fetch)
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])
with c1: st.markdown(f"<b>ACTIVE: {st.session_state.search_query}</b>", unsafe_allow_html=True)
with c2: shuffle_on = st.toggle("🔀 SUFFER Mode")
with c3: 
    if st.button("🚀 FETCH NOW"):
        st.session_state.playlist = []
        st.rerun()

# 6. Song Display (Individual Loop Fix)
display_songs = list(st.session_state.playlist)
if shuffle_on: random.shuffle(display_songs)

for song in display_songs:
    with st.container():
        st.markdown(f"""
            <div class="song-card">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; border:1px solid #00ff7f; object-fit:cover;">
                    <div style="flex-grow:1;">
                        <b style="font-size:16px;">{song.get('title')[:60]}</b><br>
                        <small style="color:#00ff7f;">{song.get('uploader')}</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 🔥 Individual Loop Switch (As per Image)
        loop_this = st.toggle(f"AUTO-LOOP Enabled", value=True, key=f"lp_{song.get('id')}")
        st.audio(song.get('url'), format='audio/mp3', loop=loop_this)

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v150.0 • No More Multi-Play</small></center>", unsafe_allow_html=True)
