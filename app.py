import streamlit as st
import yt_dlp
import random
import logging

# 1. Technical Fix: Saari backend warnings aur kachra block kiya
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

# 2. Page Configuration
st.set_page_config(page_title="Aj Beats Studio", layout="wide", initial_sidebar_state="collapsed")

# 3. DITTO IMAGE UI: Exact Circuit Pattern & Neon Glow
st.markdown("""
    <style>
    /* Exact Background: Deep Blue with Neon Purple/Green Grid Lines */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(138, 43, 226, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(0, 255, 127, 0.1) 0%, transparent 45%),
            linear-gradient(rgba(138, 43, 226, 0.05) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(138, 43, 226, 0.05) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 35px 35px, 35px 35px;
        color: white; 
    }
    
    /* Search Bar - White Glass at Top */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #111 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 15px !important;
        font-weight: 600 !important;
    }

    /* Category Buttons - Neon Borders (DITTO) */
    div.stButton > button {
        background: rgba(15, 15, 30, 0.85) !important;
        color: white !important;
        border: 1px solid rgba(138, 43, 226, 0.6) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 65px !important;
        width: 100% !important;
        border-bottom: 4px solid #00ff7f !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important;
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.5) !important;
    }

    /* Glass Panels for Songs */
    .song-box { 
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        padding: 18px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
    }
    
    .neon-text-label { 
        color: #00ff7f; 
        font-weight: 900; 
        border-left: 5px solid #00ff7f;
        padding-left: 10px;
        margin: 25px 0 15px 0;
        text-transform: uppercase;
    }

    audio { width: 100%; filter: invert(100%) hue-rotate(85deg) brightness(1.7); margin-top: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Memory for State Management
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_query' not in st.session_state: st.session_state['last_query'] = ""

# --- 1. HEADER (Profile Picture Mirror) ---
h1, h2 = st.columns([1, 4])
with h1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:75px; height:75px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px #00ff7f; object-fit: cover;">', unsafe_allow_html=True)
with h2:
    st.markdown("<h2 style='margin:0;'>Aj BEATs Studio</h2><small style='color:#00ff7f; letter-spacing:1px;'>DISCOVER SOUNDSPHERES</small>", unsafe_allow_html=True)

# --- 2. SEARCH BAR (Top Position Locked) ---
st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search Singer, Song or Playlist...", label_visibility="collapsed")

# --- 3. DISCOVER MOODS (Correct Indentation) ---
st.markdown("<div class='neon-text-label'>DISCOVER SOUNDSPHERES 🔥</div>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
mood = ""

with m1:
    if st.button("🚜 HARYANI TECHAN"):
        mood = "Latest Haryanvi Songs 2026"
with m2:
    if st.button("📻 OLD GOLD HITS"):
        mood = "90s Bollywood Evergreen"
with m3:
    if st.button("🕺 PUNJABI BEATS"):
        mood = "Top Punjabi Songs 2026"
with m4:
    if st.button("🌌 NEON PUNJABI"):
        mood = "New Punjabi Remix 2026"

# Final logic
final_query = user_search if user_search else (mood if mood else "Trending Bollywood 2026")

# --- 4. CONTROLS (Suffer & Fetch) ---
st.write("---")
ctrl_1, ctrl_2, ctrl_3 = st.columns([2, 1, 1])
with ctrl_1:
    st.markdown(f"<b>ACTIVE: {final_query}</b>", unsafe_allow_html=True)
with ctrl_2:
    shuffle = st.toggle("🔀 SUFFER Mode")
with ctrl_3:
    if st.button("🚀 FETCH NOW"):
        st.session_state['last_query'] = "" # Refresh force

# --- 5. ENGINE (DITTO PLAYER DESIGN) ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_query']:
            with st.spinner('Syncing Studio...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_query'] = final_query

        for song in st.session_state['playlist']:
            if shuffle: random.shuffle(st.session_state['playlist'])
            with st.container():
                st.markdown(f"""
                    <div class="song-box">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; border:1px solid #00ff7f; object-fit:cover;">
                            <div style="flex-grow:1;">
                                <b style="font-size:15px; color:#fff;">{song.get('title')[:55]}</b><br>
                                <small style="color:#00ff7f;">{song.get('uploader')}</small>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Image wala Loop switch har gaane ke upar
                auto_lp = st.toggle(f"AUTO-LOOP Enabled", value=True, key=f"lp_{song.get('id')}")
                st.audio(song.get('url'), format='audio/mp3', loop=auto_lp)
    except:
        st.error("Studio Offline! Refresh Karo.")

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v80.0 • No Ads</small></center>", unsafe_allow_html=True)
