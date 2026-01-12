import streamlit as st
import yt_dlp
import random

# 1. Page Config - Device responsive
st.set_page_config(page_title="Aj Pro Player", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced CSS - Spotify Dark Look
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .header-box { text-align: center; padding: 15px; }
    .profile-img { border-radius: 50%; width: 100px; height: 100px; border: 2px solid #1DB954; box-shadow: 0 0 15px #1DB954; }
    .song-card { background: #181818; padding: 12px; border-radius: 10px; border: 1px solid #282828; margin-top: 10px; }
    audio { width: 100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5); margin-top: 8px; }
    .section-title { color: #1DB954; font-size: 20px; margin-top: 20px; border-left: 4px solid #1DB954; padding-left: 10px; font-weight: bold; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Session State: Recent Search & Memory ---
if 'last_results' not in st.session_state:
    st.session_state['last_results'] = []
    st.session_state['current_query'] = "Top Bollywood Hits 2025" 

# --- Header ---
st.markdown(f'<center><div class="header-box"><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"><h2 style="color:#1DB954; margin-top:10px;">Aj Pro Player</h2></div></center>', unsafe_allow_html=True)

# --- Search Section (No Warning) ---
search_input = st.text_input(label="Search Music", placeholder="🔍 Search Singer, Gaana ya Playlist...", label_visibility="collapsed")

# --- Explore Moods (Haryanvi, Punjabi, Old Hits Added) ---
st.markdown("<div class='section-title'>🔥 Explore Moods</div>", unsafe_allow_html=True)
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)
mood_query = ""

with row1_col1:
    if st.button("🚜 Haryanvi Hits"): mood_query = "Latest Haryanvi Songs 2026"
with row1_col2:
    if st.button("🕺 Punjabi Beats"): mood_query = "Top Punjabi Party Songs 2026"
with row1_col3:
    if st.button("📻 Old Gold Hits"): mood_query = "90s Bollywood Evergreen Hits"

with row2_col1:
    if st.button("💔 Sad Vibes"): mood_query = "Best of Arijit Singh Sad Songs"
with row2_col2:
    if st.button("🥳 Party Mix"): mood_query = "Latest Bollywood Dance Hits"
with row2_col3:
    if st.button("🧘 Chill Lofi"): mood_query = "Hindi Lofi Chill Mix"

# Logic for current query
if search_input:
    target_query = search_input
elif mood_query:
    target_query = mood_query
else:
    target_query = st.session_state['current_query']

# --- Playlist Controls ---
st.write("---")
c_title, c_shuff = st.columns([3, 1])
with c_title:
    st.markdown(f"#### 🎧 Now Playing: `{target_query}`")
with c_shuff:
    shuffle_on = st.toggle("🔀 Suffer Mode")

# --- Music Fetching ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'default_search': 'ytsearch20', 'noplaylist': True, 'nocheckcertificate': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if target_query != st.session_state.get('last_fetched_query'):
            with st.spinner('🎵 Playlist taiyar ho rahi hai...'):
                info = ydl.extract_info(target_query, download=False)
                st.session_state['last_results'] = info['entries']
                st.session_state['last_fetched_query'] = target_query
                st.session_state['current_query'] = target_query

        songs_to_display = list(st.session_state['last_results'])
        if shuffle_on:
            random.shuffle(songs_to_display)

        for i in range(0, len(songs_to_display), 2):
            cols = st.columns(2)
            for k in range(2):
                if i + k < len(songs_to_display):
                    song = songs_to_display[i + k]
                    with cols[k]:
                        st.markdown(f"""
                            <div class="song-card">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <img src="{song.get('thumbnail')}" style="width:50px; height:50px; border-radius:5px; object-fit:cover;">
                                    <div style="line-height: 1.2;">
                                        <b style="font-size:14px; color:#fff;">{song.get('title')[:50]}...</b><br>
                                        <small style="color:#b3b3b3;">{song.get('uploader')}</small>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.audio(song.get('url'), format='audio/mp3')

    except Exception as e:
        st.error("Server slow hai, please refresh karein!")

# --- Footer ---
st.markdown(f"""
    <div style="background-color: #121212; padding: 20px; border-radius: 15px; margin-top: 50px; text-align: center; border-top: 2px solid #1DB954;">
        <p style="color:#1DB954; font-weight:bold;">Aj Pro Player v3.7</p>
        <p style="font-size: 12px; color: #b3b3b3;">
            <b>Recent Memory:</b> App pichli playlist yaad rakhti hai.<br>
            <b>Loop:</b> Audio ke ⋮ menu se 'Loop' on karein.
        </p>
    </div>
    <br>
    """, unsafe_allow_html=True)
