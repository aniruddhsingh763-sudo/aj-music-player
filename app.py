import streamlit as st
import yt_dlp
import random
import logging

# Faltu warnings block karne ke liye
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Pro Player", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS + JAVASCRIPT (Multi-play fix)
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .header-box { text-align: center; padding: 15px; }
    .profile-img { border-radius: 50%; width: 100px; height: 100px; border: 3px solid #1DB954; box-shadow: 0 0 15px #1DB954; }
    
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
    audio { width: 100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5); margin-top: 10px; }
    .section-title { color: #1DB954; font-size: 18px; margin-top: 20px; font-weight: bold; border-left: 5px solid #1DB954; padding-left: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>

    <script>
    // FIX: Ek gaana play hote hi baaki pause ho jayenge
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

# Session State
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_q' not in st.session_state: st.session_state['last_q'] = ""

# Header
st.markdown(f'<center><div class="header-box"><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"><h2 style="color:#1DB954; margin-top:10px;">Aj Pro Player</h2></div></center>', unsafe_allow_html=True)

# Search
search_input = st.text_input(label="Search", placeholder="🔍 Search Song, Singer or Playlist...", label_visibility="collapsed")

# Mood Buttons
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

# Logic for current search
active_query = mood if mood else (search_input if search_input else st.session_state['last_q'] if st.session_state['last_q'] else "Top Bollywood Hits 2025")

st.write("---")
h_col, s_col = st.columns([3, 1])
with h_col: st.markdown(f"#### 🎧 Playing: `{active_query}`")
with s_col: shuffle = st.toggle("🔀 Suffer Mode")

# Youtube Fetching
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if active_query != st.session_state['last_q']:
            with st.spinner('Updating Playlist...'):
                data = ydl.extract_info(active_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_q'] = active_query
                st.rerun()

        current_list = list(st.session_state['playlist'])
        if shuffle: random.shuffle(current_list)

        for song in current_list:
            with st.container():
                st.markdown(f"""
                    <div class="song-card">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="{song.get('thumbnail')}" style="width:55px; height:55px; border-radius:8px; object-fit:cover;">
                            <div>
                                <b style="font-size:15px; color:#fff;">{song.get('title')[:55]}</b><br>
                                <small style="color:#b3b3b3;">{song.get('uploader')}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                # Auto-Loop ON, but JS will stop other songs
                st.audio(song.get('url'), format='audio/mp3', loop=True)

    except Exception:
        st.error("Server slow hai, please refresh karein!")

st.markdown("""<div style="text-align: center; color: #777; margin-top: 40px;">Aj Pro Player v4.5 • Stable</div>""", unsafe_allow_html=True)
