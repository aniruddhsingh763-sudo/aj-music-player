import streamlit as st
import yt_dlp
import random
import logging

# 1. Background Warnings block
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").setLevel(logging.ERROR)

st.set_page_config(page_title="Aj Beats", layout="wide", initial_sidebar_state="collapsed")

# 🎨 DITTO IMAGE STYLE: Circuit Lines & Neon Glow CSS
st.markdown("""
    <style>
    /* Dark Theme with Neon Circuit Background (Exactly like your image) */
    .stApp { 
        background-color: #0b0b15;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(138, 43, 226, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(0, 255, 127, 0.1) 0%, transparent 50%),
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: #ffffff;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Search Bar - Top Premium Look */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        padding: 12px !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
    }
    .stTextInput > div > div > input:focus {
        border-color: #1DB954 !important;
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.3);
    }

    /* Mood Buttons - Neon Border Style (Ditto Image) */
    div.stButton > button {
        background: rgba(20, 20, 35, 0.7) !important;
        color: #ffffff !important;
        border: 1px solid rgba(138, 43, 226, 0.5) !important; /* Purple Glow */
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 65px !important;
        width: 100% !important;
        transition: 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        border-color: #00ff7f !important; /* Green Neon Glow on Hover */
        box-shadow: 0 0 20px rgba(0, 255, 127, 0.4) !important;
        background: rgba(0, 255, 127, 0.1) !important;
        transform: translateY(-2px);
    }

    /* Glass Cards for Song List */
    .song-card { 
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        padding: 18px; 
        border-radius: 15px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Neon Header Labels */
    .neon-label { 
        color: #00ff7f; 
        font-weight: 800; 
        font-size: 18px;
        text-transform: uppercase; 
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .neon-label::before {
        content: "";
        width: 4px;
        height: 20px;
        background: #00ff7f;
        display: inline-block;
        box-shadow: 0 0 10px #00ff7f;
    }

    audio { width: 100%; filter: invert(100%) hue-rotate(90deg) brightness(1.8); margin-top: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Session Memory
if 'playlist' not in st.session_state: st.session_state['playlist'] = []
if 'last_fetched' not in st.session_state: st.session_state['last_fetched'] = ""

# --- 1. HEADER (Ditto Image Profile) ---
t_col1, t_col2 = st.columns([1, 4])
with t_col1:
    st.markdown('<img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" style="width:70px; height:70px; border-radius:50%; border:3px solid #00ff7f; box-shadow: 0 0 15px rgba(0, 255, 127, 0.5); object-fit: cover;">', unsafe_allow_html=True)
with t_col2:
    st.markdown("<h1 style='margin:0; color:#ffffff; font-weight:900; letter-spacing:1px;'>AJ BEATS</h1><small style='color:#00ff7f;'>DISCOVER SOUNDSPHERES</small>", unsafe_allow_html=True)

# --- 2. SEARCH BAR (Top Position) ---
st.write("")
user_search = st.text_input(label="Search", placeholder="🔍 Search songs or artists...", label_visibility="collapsed")

# --- 3. DISCOVER MOODS (Ditto Image Buttons) ---
st.markdown("<div class='neon-label'>DISCOVER SOUNDSPHERES 🔥</div>", unsafe_allow_html=True)
m1, m2 = st.columns(2)
m3, m4 = st.columns(2)
m5, m6 = st.columns(2)
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
with m5:
    if st.button("💔 SAD SHADOWS"):
        mood = "Arijit Singh Sad Collection"
with m6:
    if st.button("🧘 CHILL VIBES"):
        mood = "Hindi Lofi Chill Mix"

# Final Query Logic
final_query = user_search if user_search else (mood if mood else "Top Bollywood Hits 2026")

# --- 4. PLAYER CONTROLS (Auto-Loop ditto like image) ---
st.write("---")
ctrl1, ctrl2, ctrl3 = st.columns([2, 1, 1])
with ctrl1:
    st.markdown(f"<small style='color:gray;'>ACTIVE STUDIO:</small><br><b>{final_query}</b>", unsafe_allow_html=True)
with ctrl2:
    shuffle = st.toggle("🔀 SUFFER")
with ctrl3:
    auto_loop = st.toggle("🔁 AUTO-LOOP", value=True)

# --- 5. MUSIC ENGINE ---
ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'ignoreerrors': True, 'default_search': 'ytsearch15', 'noplaylist': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        if final_query != st.session_state['last_fetched']:
            with st.spinner('SYNCING STUDIO...'):
                data = ydl.extract_info(final_query, download=False)
                st.session_state['playlist'] = [e for e in data['entries'] if e is not None]
                st.session_state['last_fetched'] = final_query

        for song in st.session_state['playlist']:
            if shuffle: random.shuffle(st.session_state['playlist'])
            
            st.markdown(f"""
                <div class="song-card">
                    <img src="{song.get('thumbnail')}" style="width:65px; height:65px; border-radius:12px; border:1px solid #00ff7f;">
                    <div style="flex-grow:1;">
                        <b style="font-size:15px; color:#fff;">{song.get('title')[:55]}</b><br>
                        <small style="color:#00ff7f;">{song.get('uploader')}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.audio(song.get('url'), format='audio/mp3', loop=auto_loop)

    except Exception:
        st.error("SYNC FAILED! REFRESH.")

st.markdown("<br><center><small style='color:#333;'>AJ BEATS STUDIO v10.0 • NO ADS</small></center>", unsafe_allow_html=True)
