import streamlit as st
import yt_dlp
import random
import logging

# 1. Sabhi backend warnings block
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO IMAGE UI: Neon Circuits, Glassmorphism & Exact Layout
st.markdown("""
    <style>
    /* Dark Deep Background with Circuit Vibes */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 255, 127, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(138, 43, 226, 0.08) 0%, transparent 40%),
            linear-gradient(rgba(0, 255, 127, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 127, 0.04) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 30px 30px, 30px 30px;
        color: white; 
    }
    
    /* Search Bar at the Very Top */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0, 255, 127, 0.5) !important;
        padding: 12px !important;
        font-size: 16px !important;
    }

    /* Mood Buttons (Grid Design like Image) */
    div.stButton > button {
        background: rgba(20, 20, 40, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.5) !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 65px !important;
        width: 100% !important;
        transition: 0.3s ease;
        text-transform: uppercase;
        border-bottom: 3px solid #00ff7f !important;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important;
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.6) !important;
        transform: scale(1.02);
    }

    /* Suffer & Fetch Buttons (Compact Style) */
    .stButton > button[kind="secondary"] {
        height: 40px !important;
        font-size: 12px !important;
    }

    /* Glass Song Cards */
    .song-card { 
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 15px; 
        border-radius: 18px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .neon-text { 
        color: #00ff7f; 
        font-weight: 800; 
        text-transform: uppercase; 
        border-left: 5px solid #00ff7f;
        padding-left: 10px;
        margin: 25px 0 10px 0;
    }

    /* Player Aesthetics */
    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 8px; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session State for fetching and memory
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_query' not in st.session_state: st.session_state['last_query'] = ""

# --- 1. TOP HEADER (Ditto Image Profile) ---
t1, t2 = st.columns([1, 4])
with t1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; height:75px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit:cover;">', unsafe_allow_html=True)
with t2:
    st.markdown("<h2 style='margin:0;'>AJ BEATS</h2><small style='color:#00ff7f; letter-spacing:2px;'>THE MUSIC STUDIO</small>", unsafe_allow_html=True)

# --- 2. SEARCH BAR (Top Layout) ---
st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search songs, artists or playlists...", label_visibility="collapsed")

# --- 3. DISCOVER SOUNDSPHERES (Grid Buttons) ---
st.markdown("<div class='neon-text'>Discover Soundspheres 🔥</div>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
mood = ""

with m1:
    if st.button("🚜 HARYANI TECHAN"): mood = "Latest Haryanvi Songs 2026"
with m2:
    if st.button("📻 OLD GOLD HIES"): mood = "90s Bollywood Evergreen"
with m3:
    if st.button("🕺 PUNJABI BEATS"): mood = "Top Punjabi Songs 2026"
with m4:
    if st.button("🌌 NEON PUNJABI"): mood = "Latest Punjabi Remix 2026"

final_query = user_search if user_search else (mood if mood else "Bollywood Hits 2026")

# --- 4. CONTROLS (Suffer & Fetch Button Together) ---
st.write("---")
c_1, c_2, c_3 = st.columns([2, 1, 1])
with c_2:
    shuffle = st.toggle("☁️ Suffer Mode")
with c_3:
    if st.button("🚀 Fetch Now"):
        st.session_state['last_query'] = "" # Reset to force refresh

# --- 5. DITTO PLAYER ENGINE ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_query']:
            with st.spinner('SYNCING STUDIO...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_query'] = final_query

        songs = list(st.session_state['playlist'])
        if shuffle: random.shuffle(songs)

        for song in songs:
            with st.container():
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
                
                # Auto-Loop toggle exactly above each player
                loop_val = st.toggle(f"Auto-Loop Enabled", value=True, key=f"loop_{song.get('id')}")
                st.audio(song.get('url'), format='audio/mp3', loop=loop_val)

    except:
        st.error("Studio Sync Error! Refresh please.")

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v30.0 • Developed by Aj</small></center>", unsafe_allow_html=True)
