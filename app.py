import streamlit as st
import yt_dlp
import random
import logging

# 1. Backend Clean-up: Saari warnings mute kar di hain
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

# 2. Page Setup
st.set_page_config(page_title="Aj Beats", layout="wide", initial_sidebar_state="collapsed")

# 3. Premium CSS (Image Style)
st.markdown("""
    <style>
    .stApp { background: #0c0c0c; color: white; }
    
    /* Search Bar at Top */
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 20px !important;
        border: 1px solid #1DB954 !important;
        padding: 12px 20px !important;
    }

    /* Mood Buttons - Large & 3D */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #1DB954 !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        height: 90px !important;
        width: 100% !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.6) !important;
    }
    div.stButton > button:hover {
        background: #1DB954 !important;
        color: black !important;
        box-shadow: 0 0 25px #1DB954;
    }

    /* Glass Cards */
    .song-card { 
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 15px; 
        border-radius: 18px; 
        border-left: 5px solid #1DB954;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .section-header { 
        font-size: 24px; 
        font-weight: bold; 
        margin: 25px 0 10px 0; 
        border-left: 6px solid #1DB954;
        padding-left: 12px;
    }

    audio { width: 100%; filter: invert(100%) hue-rotate(90deg) brightness(1.7); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session Memory
if 'playlist' not in st.session_state:
    st.session_state['playlist'] = []
if 'last_fetched' not in st.session_state:
    st.session_state['last_fetched'] = ""

# --- 1. SEARCH BAR (TOP) ---
col_logo, col_name = st.columns([1, 4])
with col_logo:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; border-radius:50%; border:2px solid #1DB954; box-shadow: 0 0 15px #1DB954;">', unsafe_allow_html=True)
with col_name:
    st.markdown("<h2 style='margin:0; color:#1DB954;'>AJ BEATS</h2><p style='color:#777; margin:0;'>The Music Studio</p>", unsafe_allow_html=True)

st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search Singer, Song or Playlist...", label_visibility="collapsed")

# --- 2. CATEGORIES (BADE BUTTONS) ---
st.markdown("<div class='section-header'>🔥 Explore Moods</div>", unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
m4, m5, m6 = st.columns(3)
mood = ""

# Fixed Python Syntax Indentation
with m1:
    if st.button("🚜 Haryanvi Hits"):
        mood = "Latest Haryanvi Songs 2026"
with m2:
    if st.button("🕺 Punjabi Beats"):
        mood = "Top Punjabi Songs 2026"
with m3:
    if st.button("📻 Old Gold Hits"):
        mood = "90s Bollywood Evergreen"
with m4:
    if st.button("💔 Sad Vibes"):
        mood = "Arijit Singh Sad Collection"
with m5:
    if st.button("🥳 Party Mix"):
        mood = "Latest Bollywood Dance Hits"
with m6:
    if st.button("🧘 Chill Lofi"):
        mood = "Hindi Lofi Chill Mix"

# Query Logic
final_query = user_search if user_search else (mood if mood else "Top Bollywood Hits 2026")

# --- 3. CONTROLS ---
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    st.markdown(f"#### 🎧 Now Playing: `{final_query}`")
with c2:
    shuffle = st.toggle("🔀 Suffer Mode")
with c3:
    auto_loop = st.toggle("🔁 Auto Loop", value=True)

# --- 4. ENGINE ---
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'ignoreerrors': True,
    'default_search': 'ytsearch15',
    'noplaylist': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_fetched']:
            with st.spinner('Preparing Studio...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_fetched'] = final_query

        display_list = list(st.session_state['playlist'])
        if shuffle:
            random.shuffle(display_list)

        for song in display_list:
            st.markdown(f"""
                <div class="song-card">
                    <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; object-fit:cover; border: 1px solid #1DB954;">
                    <div>
                        <b style="font-size:16px;">{song.get('title')[:60]}</b><br>
                        <small style="color:#1DB954;">{song.get('uploader')}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.audio(song.get('url'), format='audio/mp3', loop=auto_loop)

    except Exception:
        st.error("Studio Sync Error! Refresh please.")

st.markdown("<br><center><p style='color:#444; font-size:12px;'>AJ BEATS v8.0 • Developed by Aj</p></center>", unsafe_allow_html=True)

    
