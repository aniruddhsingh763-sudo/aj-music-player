import streamlit as st
import yt_dlp
import random
import logging

# 1. Backend Clean-up: Sabhi errors block
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO UI: Neon Grid Pattern & Glass Layout
st.markdown("""
    <style>
    /* Exact Background: Deep Blue with Neon Grid Lines */
    .stApp { 
        background-color: #0a0a1a;
        background-image: 
            linear-gradient(rgba(0, 255, 127, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 127, 0.05) 1px, transparent 1px),
            radial-gradient(circle at 20% 20%, rgba(138, 43, 226, 0.1) 0%, transparent 40%);
        background-size: 30px 30px, 30px 30px, 100% 100%;
        color: white; 
    }
    
    /* White Search Bar at Top */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 15px !important;
        font-weight: bold !important;
    }

    /* Category Buttons - Neon Borders & Glow */
    div.stButton > button {
        background: rgba(20, 20, 40, 0.9) !important;
        color: white !important;
        border: 2px solid rgba(138, 43, 226, 0.6) !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        height: 70px !important;
        width: 100% !important;
        text-transform: uppercase;
        border-bottom: 4px solid #00ff7f !important;
        transition: 0.3s ease;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important;
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.5) !important;
        transform: translateY(-3px);
    }

    /* Glass Song Panels */
    .song-card { 
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
    }
    
    .neon-label { 
        color: #00ff7f; 
        font-weight: 900; 
        text-transform: uppercase; 
        border-left: 6px solid #00ff7f;
        padding-left: 12px;
        margin: 30px 0 15px 0;
    }

    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Memory Management
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_query' not in st.session_state: st.session_state['last_query'] = ""

# --- 1. Header (Profile) ---
h1, h2 = st.columns([1, 4])
with h1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:80px; height:80px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 20px #00ff7f; object-fit: cover;">', unsafe_allow_html=True)
with h2:
    st.markdown("<h1 style='margin:0;'>AJ BEATS</h1><small style='color:#00ff7f; letter-spacing:2px;'>DISCOVER SOUNDSPHERES</small>", unsafe_allow_html=True)

# --- 2. Search Top ---
st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search Singer, Song or Playlist...", label_visibility="collapsed")

# --- 3. Moods Grid ---
st.markdown("<div class='neon-label'>Discover Soundspheres 🔥</div>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
mood = ""

with m1:
    if st.button("🚜 HARYANI TECHAN"): mood = "Latest Haryanvi Songs 2026"
with m2:
    if st.button("📻 OLD GOLD HITS"): mood = "90s Bollywood Evergreen"
with m3:
    if st.button("🕺 PUNJABI BEATS"): mood = "Top Punjabi Songs 2026"
with m4:
    if st.button("🌌 NEON PUNJABI"): mood = "New Punjabi Remix 2026"

final_query = user_search if user_search else (mood if mood else "Bollywood Hits 2026")

# --- 4. Controls ---
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    st.markdown(f"<b>ACTIVE: {final_query}</b>", unsafe_allow_html=True)
with c2:
    shuffle = st.toggle("🔀 SUFFER")
with c3:
    auto_loop = st.toggle("🔁 LOOP", value=True)

# --- 5. Studio Engine ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_query']:
            with st.spinner('SYNCING STUDIO...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_query'] = final_query

        current_songs = list(st.session_state['playlist'])
        if shuffle: random.shuffle(current_songs)

        for song in current_songs:
            st.markdown(f"""
                <div class="song-card">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <img src="{song.get('thumbnail')}" style="width:70px; height:70px; border-radius:15px; border:2px solid #00ff7f; object-fit:cover;">
                        <div>
                            <b style="font-size:16px;">{song.get('title')[:60]}</b><br>
                            <small style="color:#00ff7f;">{song.get('uploader')}</small>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.audio(song.get('url'), format='audio/mp3', loop=auto_loop)

    except:
        st.error("Studio Offline! Refresh.")

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v35.0 • FINAL MIRROR</small></center>", unsafe_allow_html=True)
