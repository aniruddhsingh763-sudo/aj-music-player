import streamlit as st
import yt_dlp
import random
import logging

# Technical Fix: Saari warnings block kar di hain
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats", layout="wide", initial_sidebar_state="collapsed")

# 🎨 PREMIUM UI DESIGN (Based on your final request)
st.markdown("""
    <style>
    .stApp { background: #0c0c0c; color: white; }
    
    /* 1. TOP SEARCH BAR */
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 20px !important;
        border: 1px solid #1DB954 !important;
        padding: 12px 20px !important;
    }

    /* 2. LARGE MOOD BUTTONS (EXPLORE) */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #1DB954 !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        height: 90px !important;
        width: 100% !important;
        transition: 0.3s;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5) !important;
    }
    div.stButton > button:hover {
        background: #1DB954 !important;
        color: black !important;
        box-shadow: 0 0 20px #1DB954;
        transform: translateY(-3px);
    }

    /* 3. PREMIUM SONG CARDS */
    .song-card { 
        background: #181818; 
        padding: 15px; 
        border-radius: 15px; 
        border-bottom: 2px solid #1DB954;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .section-header { 
        font-size: 22px; 
        font-weight: bold; 
        margin: 25px 0 10px 0; 
        color: #fff; 
        border-left: 5px solid #1DB954;
        padding-left: 12px;
    }

    /* Audio Player Styling */
    audio { width: 100%; filter: invert(100%) hue-rotate(90deg) brightness(1.6); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Memory for History & Playlist
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'history' not in st.session_state: st.session_state['history'] = []

# --- TOP SECTION: NAME & SEARCH ---
col_logo, col_name = st.columns([1, 4])
with col_logo:
    st.markdown(f'<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; border-radius:50%; border:2px solid #1DB954; box-shadow: 0 0 15px #1DB954;">', unsafe_allow_html=True)
with col_name:
    st.markdown("<h2 style='margin:0; color:#1DB954;'>AJ BEATS</h2><p style='color:#777; margin:0;'>The Music Studio</p>", unsafe_allow_html=True)

st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search Singer, Song or Playlist...", label_visibility="collapsed")

# --- MIDDLE SECTION: BADE CATEGORY BUTTONS ---
st.markdown("<div class='section-header'>🔥 Explore Categories</div>", unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m4, m5, m6 = st.columns(3)
mood = ""

with m1: if st.button("🚜 Haryanvi Hits"): mood = "Latest Haryanvi 2026"
with m2: if st.button("🕺 Punjabi Beats"): mood = "Top Punjabi 2026"
with m3: if st.button("📻 Old Gold Hits"): mood = "90s Bollywood Evergreen"
with m4: if st.button("💔 Sad Vibes"): mood = "Arijit Singh Best Sad"
with m5: if st.button("🥳 Party Mix"): mood = "Latest Bollywood Dance Hits"
with m6: if st.button("🧘 Chill Lofi"): mood = "Hindi Lofi Chill Mix"

# Final query logic
final_query = user_search if user_search else (mood if mood else "Top Bollywood Hits 2026")

# --- CONTROLS SECTION: AUTO LOOP & SUFFER ---
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    st.markdown(f"#### 🎧 Now Playing: `{final_query}`")
with c2:
    shuffle = st.toggle("🔀 Suffer Mode")
with c3:
    # IMAGE WALA FEATURE: Loop Toggle Clickable
    auto_loop = st.toggle("🔁 Auto Loop", value=True)

# --- MUSIC FETCH & DISPLAY ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state.get('last_q'):
            with st.spinner('Preparing Studio...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_q'] = final_query

        current_list = list(st.session_state['playlist'])
        if shuffle: random.shuffle(current_list)

        for song in current_list:
            st.markdown(f"""
                <div class="song-card">
                    <img src="{song.get('thumbnail')}" style="width:60px; height:60px; border-radius:10px; object-fit:cover;">
                    <div>
                        <b style="font-size:16px;">{song.get('title')[:60]}</b><br>
                        <small style="color:#1DB954;">{song.get('uploader')}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.audio(song.get('url'), format='audio/mp3', loop=auto_loop)

    except:
        st.error("Server slow hai! Refresh karke dekhein.")

st.markdown("<br><center><p style='color:#333; font-size:11px;'>AJ BEATS v8.0 • High Quality Ad-Free Music • Developed by Aj</p></center>", unsafe_allow_html=True)

