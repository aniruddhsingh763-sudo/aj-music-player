import streamlit as st
import yt_dlp
import random
import logging

# Faltu ki saari warnings ko block karne ke liye
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Pro Player", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS - Buttons, Cards aur Auto-Loop player styling
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .header-box { text-align: center; padding: 15px; }
    .profile-img { border-radius: 50%; width: 100px; height: 100px; border: 3px solid #1DB954; box-shadow: 0 0 15px #1DB954; }
    
    /* Buttons Fix: Text White, Bold aur saaf dikhega */
    div.stButton > button {
        color: white !important;
        background-color: #1DB954 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 12px !important;
        border: none !important;
        font-size: 16px !important;
    }
    
    .song-card { background: #181818; padding: 12px; border-radius: 10px; border: 1px solid #282828; margin-top: 10px; }
    
    /* Audio Player Styling */
    audio { 
        width: 100%; 
        filter: invert(100%) hue-rotate(180deg) brightness(1.5); 
        margin-top: 10px; 
    }

    .section-title { color: #1DB954; font-size: 18px; margin-top: 20px; font-weight: bold; border-left: 5px solid #1DB954; padding-left: 10px; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session State for Memory
if 'playlist' not in st.session_state:
    st.session_state['playlist'] = []
    st.session_state['query_text'] = "Top Bollywood Hits 2025"

# Header
st.markdown(f'<center><div class="header-box"><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"><h2 style="color:#1DB954; margin-top:10px;">Aj Pro Player</h2></div></center>', unsafe_allow_html=True)

# Search Bar (No Warnings)
search_input = st.text_input(label="Search", placeholder="🔍 Search Song, Singer or Playlist...", label_visibility="collapsed")

# Mood Buttons (Haryanvi, Punjabi, Old Gold)
st.markdown("<div class='section-title'>🔥 Music Categories</div>", unsafe_allow_html=True)
m_col1, m_col2, m_col3 = st.columns(3)
m_col4, m_col5, m_col6 = st.columns(3)
mood = ""

with m_col1:
    if st.button("🚜 Haryanvi"): mood = "Latest Haryanvi Songs 2026"
with m_col2:
    if st.button("🕺 Punjabi"): mood = "Top Punjabi Hits 2026"
with m_col3:
    if st.button("📻 Old Gold"): mood = "Bollywood Evergreen 90s"
with m_col4:
    if st.button("💔 Sad Vibes"): mood = "Arijit Singh Best Sad Songs"
with m_col5:
    if st.button("🥳 Party Mix"): mood = "New Bollywood Dance Hits"
with m_col6:
    if st.button("🧘 Chill Lofi"): mood = "Hindi Lofi Chill Mix"

# Active Query Selection
active_query = search_input if search_input else (mood if mood else st.session_state['query_text'])

st.write("---")
h_col, s_col = st.columns([3, 1])
with h_col:
    st.markdown(f"#### 🎧 Playing: `{active_query}`")
with s_col:
    shuffle = st.toggle("🔀 Suffer Mode")

# Youtube Fetching Logic
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch20', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if active_query != st.session_state.get('last_q'):
            with st.spinner('Updating Playlist...'):
                data = ydl.extract_info(active_query, download=False)
                st.session_state['playlist'] = [entry for entry in data['entries'] if entry is not None]
                st.session_state['last_q'] = active_query
                st.session_state['query_text'] = active_query

        current_list = list(st.session_state['playlist'])
        if shuffle:
            random.shuffle(current_list)

        for song in current_list:
            with st.container():
                st.markdown(f"""
                    <div class="song-card">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="{song.get('thumbnail')}" style="width:55px; height:55px; border-radius:8px; object-fit:cover;">
                            <div>
                                <b style="font-size:15px; color:#fff;">{song.get('title')[:55]}</b><br>
                                <small style="color:#b3b3b3;">{song.get('uploader')} • {song.get('duration_string')}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # AUTO-LOOP FEATURE: 'loop' parameter add kar diya hai
                st.audio(song.get('url'), format='audio/mp3', loop=True)

    except Exception:
        st.error("Server slow hai, please refresh karein!")

st.markdown("""
    <div style="background-color: #121212; padding: 20px; border-radius: 15px; margin-top: 40px; text-align: center; border-top: 2px solid #1DB954;">
        <p style="color:#1DB954; font-weight:bold;">Aj Pro Player v4.5</p>
        <p style="font-size: 12px; color: #777;">Auto-Loop is ON | No Warnings | High Quality Stream</p>
    </div><br>
    """, unsafe_allow_html=True)
