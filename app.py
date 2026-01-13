import streamlit as st
import yt_dlp
import random
import logging

# Warnings block
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Pro Player", layout="wide", initial_sidebar_state="collapsed")

# --- JAVASCRIPT FIX (Ye hai wo chota change jo jaruri hai) ---
# Ye script browser par nazar rakhegi. Jaise hi koi 'play' karega, baaki sab 'pause' honge.
st.markdown("""
    <script>
    document.addEventListener('play', function(e){
        var audios = document.getElementsByTagName('audio');
        for(var i = 0, len = audios.length; i < len; i++){
            if(audios[i] != e.target){
                audios[i].pause();
            }
        }
    }, true);
    </script>
    
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .header-box { text-align: center; padding: 15px; }
    .profile-img { border-radius: 50%; width: 100px; height: 100px; border: 3px solid #1DB954; box-shadow: 0 0 15px #1DB954; }
    
    /* Buttons Styling */
    div.stButton > button {
        color: white !important;
        background-color: #1DB954 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
        border: none !important;
        padding: 10px !important;
    }
    
    .song-card { background: #181818; padding: 10px; border-radius: 10px; border: 1px solid #282828; margin-top: 10px; }
    audio { width: 100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5); margin-top: 5px; }
    .section-title { color: #1DB954; font-size: 18px; margin-top: 20px; font-weight: bold; border-left: 5px solid #1DB954; padding-left: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session Setup
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_q' not in st.session_state: st.session_state['last_q'] = ""

# Header
st.markdown(f'<center><div class="header-box"><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"><h2 style="color:#1DB954; margin-top:10px;">Aj Pro Player</h2></div></center>', unsafe_allow_html=True)

# Search Bar
search_input = st.text_input(label="Search", placeholder="🔍 Search Song, Singer...", label_visibility="collapsed")

# Mood Buttons
st.markdown("<div class='section-title'>🔥 Music Categories</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)
mood = ""

with c1: 
    if st.button("🚜 Haryanvi"): mood = "Latest Haryanvi Songs 2026"
with c2: 
    if st.button("🕺 Punjabi"): mood = "Top Punjabi Hits 2026"
with c3: 
    if st.button("📻 Old Gold"): mood = "Bollywood Evergreen 90s"
with c4: 
    if st.button("💔 Sad Vibes"): mood = "Arijit Singh Best Sad Songs"
with c5: 
    if st.button("🥳 Party Mix"): mood = "New Bollywood Dance Hits"
with c6: 
    if st.button("🧘 Chill Lofi"): mood = "Hindi Lofi Chill Mix"

# Query Logic
active_query = mood if mood else (search_input if search_input else st.session_state.get('last_q', "Top Bollywood Hits 2025"))

st.write("---")
col_info, col_shuff = st.columns([3, 1])
with col_info: st.markdown(f"#### 🎧 Playing: `{active_query}`")
with col_shuff: shuffle = st.toggle("🔀 Shuffle")

# Fetching Logic
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        # Agar query change hui hai toh nayi list fetch karo
        if active_query != st.session_state['last_q']:
            with st.spinner('Loading Playlist...'):
                data = ydl.extract_info(active_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_q'] = active_query
                st.rerun() # Page refresh taaki naye gaane dikhen

        # Display Songs
        current_list = list(st.session_state['playlist'])
        if shuffle: random.shuffle(current_list)

        for song in current_list:
            with st.container():
                st.markdown(f"""
                    <div class="song-card">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="{song.get('thumbnail')}" style="width:55px; height:55px; border-radius:8px; object-fit:cover;">
                            <div>
                                <b style="font-size:15px; color:#fff;">{song.get('title')[:50]}</b><br>
                                <small style="color:#b3b3b3;">{song.get('uploader')}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                # Player
                st.audio(song.get('url'), format='audio/mp3')

    except Exception:
        st.error("Network Issue or Retry.")

st.markdown("""<br><center><small style='color: #555;'>Aj Pro Player v5.0 • Single Play Fix</small></center>""", unsafe_allow_html=True)
