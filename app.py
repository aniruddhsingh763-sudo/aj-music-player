import streamlit as st
import yt_dlp
import random
import logging

# Sabhi technical warnings block kar di hain
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 UNIVERSAL UI: Neon Circuit & Responsive Design
st.markdown("""
    <style>
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 255, 127, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(138, 43, 226, 0.05) 0%, transparent 40%),
            linear-gradient(rgba(0, 255, 127, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 127, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 35px 35px, 35px 35px;
        color: white; 
    }
    
    /* Search Bar - Top Position */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 255, 127, 0.4) !important;
        padding: 12px !important;
    }

    /* Mood Buttons - Large & Neon Glow */
    div.stButton > button {
        background: rgba(15, 15, 25, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.4) !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        height: 75px !important;
        width: 100% !important;
        transition: 0.3s;
        border-bottom: 4px solid #00ff7f !important;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important;
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.5) !important;
        transform: translateY(-3px);
    }

    /* Glass Song Cards */
    .song-card { 
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        padding: 15px; 
        border-radius: 18px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .neon-label { 
        color: #00ff7f; 
        font-weight: 900; 
        font-size: 20px; 
        text-transform: uppercase;
        border-left: 6px solid #00ff7f;
        padding-left: 12px;
        margin: 25px 0 15px 0;
    }

    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session State for History & Playlist
if 'u_playlist' not in st.session_state: st.session_state['u_playlist'] = []
if 'u_last_q' not in st.session_state: st.session_state['u_last_q'] = ""

# --- 1. HEADER & TOP SEARCH ---
h_col1, h_col2 = st.columns([1, 4])
with h_col1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:80px; height:80px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit: cover;">', unsafe_allow_html=True)
with h_col2:
    st.markdown("<h1 style='margin:0;'>AJ BEATS</h1><small style='color:#00ff7f; letter-spacing:2px;'>UNIVERSAL STUDIO</small>", unsafe_allow_html=True)

st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search songs, artists or playlists...", label_visibility="collapsed")

# --- 2. DISCOVER MOODS (Responsive Grid) ---
st.markdown("<div class='neon-label'>DISCOVER SOUNDSPHERES 🔥</div>", unsafe_allow_html=True)
mood = ""

# PC par 3 columns, Phone par automatically adjust hoga
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    if st.button("🚜 HARYANI TECHAN"): mood = "Latest Haryanvi Songs 2026"
    if st.button("💔 SAD SHADOWS"): mood = "Arijit Singh Sad 2026"
with m_col2:
    if st.button("🕺 PUNJABI BEATS"): mood = "Top Punjabi Songs 2026"
    if st.button("🥳 PARTY HITS"): mood = "New Bollywood Dance 2026"
with m_col3:
    if st.button("📻 OLD GOLD HITS"): mood = "90s Bollywood Evergreen"
    if st.button("🧘 CHILL VIBES"): mood = "Hindi Lofi Mashup"

# Final query logic
final_query = user_search if user_search else (mood if mood else "Trending Bollywood 2026")

# --- 3. PLAYER CONTROLS ---
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    st.markdown(f"#### 🎧 ACTIVE: `{final_query}`")
with c2:
    shuffle = st.toggle("🔀 SHUFFLE")
with c3:
    auto_loop = st.toggle("🔁 AUTO-LOOP", value=True)

# --- 4. ENGINE (PC + PHONE OPTIMIZED) ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['u_last_q']:
            with st.spinner('SYNCING STUDIO...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['u_playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['u_last_q'] = final_query

        current_songs = list(st.session_state['u_playlist'])
        if shuffle: random.shuffle(current_songs)

        for song in current_songs:
            st.markdown(f"""
                <div class="song-card">
                    <img src="{song.get('thumbnail')}" style="width:70px; height:70px; border-radius:12px; border:1px solid #00ff7f; object-fit:cover;">
                    <div style="flex-grow:1;">
                        <b style="font-size:16px; color:#fff;">{song.get('title')[:60]}</b><br>
                        <small style="color:#00ff7f;">{song.get('uploader')}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.audio(song.get('url'), format='audio/mp3', loop=auto_loop)

    except Exception:
        st.error("Studio Sync Error! Refresh please.")

st.markdown("<br><center><p style='color:#333; font-size:12px;'>AJ BEATS v15.0 • NO ADS • High Quality</p></center>", unsafe_allow_html=True)
