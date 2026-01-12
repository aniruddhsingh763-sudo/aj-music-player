import streamlit as st
import yt_dlp
import random
import logging

# Warnings block karne ke liye
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Pro Player", layout="wide", initial_sidebar_state="collapsed")

# 🎨 ADVANCED UI DESIGN (Glassmorphism & Gradients)
st.markdown("""
    <style>
    /* Background with Subtle Gradient */
    .stApp { 
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        color: white; 
    }
    
    /* Profile Photo with Advanced Glow */
    .profile-container {
        text-align: center;
        padding: 20px;
    }
    .profile-img { 
        border-radius: 50%; 
        width: 120px; height: 120px; 
        border: 4px solid #1DB954;
        box-shadow: 0 0 25px rgba(29, 185, 84, 0.6);
        transition: 0.4s;
    }
    .profile-img:hover { transform: scale(1.05); }

    /* Premium Buttons with Icons */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #1DB954 !important;
        border: 1px solid #1DB954 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        height: 50px !important;
    }
    div.stButton > button:hover {
        background: #1DB954 !important;
        color: black !important;
        box-shadow: 0 0 15px #1DB954;
    }

    /* Modern Song Cards */
    .song-card { 
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 15px; 
        border-radius: 15px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        margin-top: 15px;
    }
    
    /* Neon Green Audio Player */
    audio { 
        width: 100%; 
        filter: invert(100%) hue-rotate(90deg) brightness(1.8); 
        margin-top: 10px; 
    }

    .section-title { 
        color: #ffffff; 
        font-size: 22px; 
        margin-top: 30px; 
        font-weight: 800; 
        letter-spacing: 1px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Memory ---
if 'playlist' not in st.session_state:
    st.session_state['playlist'] = []
    st.session_state['query_text'] = "Top Bollywood Hits 2026"

# --- Header ---
st.markdown(f"""
    <div class="profile-container">
        <img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img">
        <h1 style="color:#1DB954; font-family: 'Arial Black'; margin-top:15px;">AJ PRO PLAYER</h1>
        <p style="color:#888;">Your Private Ad-Free Music Studio</p>
    </div>
    """, unsafe_allow_html=True)

# --- Search ---
user_search = st.text_input(label="Search", placeholder="🚀 Type song name or singer...", label_visibility="collapsed")

# --- Premium Categories ---
st.markdown("<div class='section-title'>💎 DISCOVER MOODS</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)
mood = ""

with c1: if st.button("🚜 HARYANVI"): mood = "New Haryanvi Songs 2026"
with c2: if st.button("🕺 PUNJABI"): mood = "Top Punjabi Beats 2026"
with c3: if st.button("📻 OLD GOLD"): mood = "90s Bollywood Hits"
with c4: if st.button("💔 SAD VIBES"): mood = "Arijit Singh Sad Mix"
with c5: if st.button("🥳 PARTY HITS"): mood = "Latest Dance Songs 2026"
with c6: if st.button("🧘 CHILL LOFI"): mood = "Hindi Lofi Mix 2026"

active_query = user_search if user_search else (mood if mood else st.session_state['query_text'])

# --- Player Section ---
st.write("---")
h_col, s_col = st.columns([3, 1])
with h_col:
    st.markdown(f"#### 🎵 Active: <span style='color:#1DB954;'>{active_query}</span>", unsafe_allow_html=True)
with s_col:
    shuffle = st.toggle("Suffer Mode")

# --- Fetching Logic ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch20', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if active_query != st.session_state.get('last_q'):
            with st.spinner('✨ Creating your playlist...'):
                data = ydl.extract_info(active_query, download=False)
                st.session_state['playlist'] = [entry for entry in data['entries'] if entry is not None]
                st.session_state['last_q'] = active_query

        current_list = list(st.session_state['playlist'])
        if shuffle: random.shuffle(current_list)

        for song in current_list:
            with st.container():
                st.markdown(f"""
                    <div class="song-card">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <img src="{song.get('thumbnail')}" style="width:60px; height:60px; border-radius:12px; object-fit:cover; border: 1px solid #1DB954;">
                            <div style="flex-grow: 1;">
                                <b style="font-size:16px; color:#fff;">{song.get('title')[:60]}</b><br>
                                <small style="color:#1DB954;">{song.get('uploader')}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.audio(song.get('url'), format='audio/mp3', loop=True)

    except Exception:
        st.error("Network issue, please try again.")

# --- Modern Footer ---
st.markdown(f"""
    <div style="background: rgba(29, 185, 84, 0.1); padding: 30px; border-radius: 20px; margin-top: 50px; text-align: center; border: 1px solid #1DB954;">
        <h3 style="color:#1DB954; margin:0;">AJ PRO PLAYER v5.0</h3>
        <p style="color:#777; font-size:12px;">Premium Ad-Free Experience • Auto-Loop Enabled • Developed by Aj</p>
    </div><br>
    """, unsafe_allow_html=True)
