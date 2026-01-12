import streamlit as st
import yt_dlp
import random
import logging

# 1. Technical Fix: Saari faltu warnings aur logs ko backend se block kiya hai
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

# 2. Page Configuration
st.set_page_config(page_title="Aj Pro Player", layout="wide", initial_sidebar_state="collapsed")

# 3. Custom CSS: Buttons, Colors, aur No-Error Layout
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .header-box { text-align: center; padding: 15px; }
    .profile-img { border-radius: 50%; width: 100px; height: 100px; border: 3px solid #1DB954; box-shadow: 0 0 15px #1DB954; }
    
    /* Mood Buttons: Text white aur bold taaki saaf dikhe */
    div.stButton > button {
        color: white !important;
        background-color: #1DB954 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 12px !important;
        border: none !important;
        font-size: 15px !important;
    }
    
    .song-card { background: #181818; padding: 12px; border-radius: 10px; border: 1px solid #282828; margin-top: 10px; }
    audio { width: 100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5); margin-top: 8px; }
    .section-title { color: #1DB954; font-size: 18px; margin-top: 20px; font-weight: bold; border-left: 4px solid #1DB954; padding-left: 10px; }
    
    /* Streamlit ki faltu cheezein hide karne ke liye */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Memory Management: No Blank Page Logic ---
if 'playlist' not in st.session_state:
    st.session_state['playlist'] = []
    st.session_state['query_text'] = "Top Bollywood Hits 2025"

# --- Header Section ---
st.markdown(f'<center><div class="header-box"><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"><h2 style="color:#1DB954; margin-top:10px;">Aj Pro Player</h2></div></center>', unsafe_allow_html=True)

# --- Search Box: No Warning Label ---
user_search = st.text_input(label="Search", placeholder="🔍 Search Song, Singer or Playlist...", label_visibility="collapsed")

# --- Explore Moods: Haryanvi, Punjabi, Old Hits Added ---
st.markdown("<div class='section-title'>🔥 Explore Moods</div>", unsafe_allow_html=True)
m_col1, m_col2, m_col3 = st.columns(3)
m_col4, m_col5, m_col6 = st.columns(3)
mood = ""

with m_col1:
    if st.button("🚜 Haryanvi Hits"): mood = "Latest Haryanvi Songs 2026"
with m_col2:
    if st.button("🕺 Punjabi Beats"): mood = "Top Punjabi Songs 2026"
with m_col3:
    if st.button("📻 Old Gold Hits"): mood = "90s Bollywood Evergreen Hits"
with m_col4:
    if st.button("💔 Sad Vibes"): mood = "Arijit Singh Sad Collection"
with m_col5:
    if st.button("🥳 Party Mix"): mood = "New Bollywood Dance Songs"
with m_col6:
    if st.button("🧘 Chill Lofi"): mood = "Hindi Lofi Chill Mix"

# Logic for active query
active_query = user_search if user_search else (mood if mood else st.session_state['query_text'])

# --- Player Controls: Suffer Mode ---
st.write("---")
h_col, s_col = st.columns([3, 1])
with h_col:
    st.markdown(f"#### 🎧 Playing: `{active_query}`")
with s_col:
    shuffle = st.toggle("🔀 Suffer Mode")

# --- Music Fetching & Auto-Loop Logic ---
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'ignoreerrors': True,
    'default_search': 'ytsearch20',
    'noplaylist': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        # Check if query changed or first time
        if active_query != st.session_state.get('last_q'):
            with st.spinner('🎵 Playlist taiyar ho rahi hai...'):
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
                
                # AUTO-LOOP: loop=True adds repeat automatically
                st.audio(song.get('url'), format='audio/mp3', loop=True)

    except Exception:
        st.error("Server slow hai, please refresh karein!")

# --- Footer ---
st.markdown(f"""
    <div style="background-color: #121212; padding: 20px; border-radius: 15px; margin-top: 40px; text-align: center; border-top: 2px solid #1DB954;">
        <p style="color:#1DB954; font-weight:bold;">Aj Pro Player v4.5 Final</p>
        <p style="font-size: 11px; color: #555;">Recent Memory Active | Auto-Loop ON | No Ad Experience</p>
    </div><br>
    """, unsafe_allow_html=True)

