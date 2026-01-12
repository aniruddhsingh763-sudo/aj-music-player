import streamlit as st
import yt_dlp
import random

# 1. Page Configuration - PC aur Mobile dono ke liye layout set kiya hai
st.set_page_config(page_title="Aj Music Pro", layout="wide", initial_sidebar_state="collapsed")

# 2. Custom CSS - Spotify Style Dark Theme aur Responsive Design
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    
    /* Sticky Header: Search aur Profile upar fixed rahenge */
    .header-box {
        position: sticky;
        top: 0;
        background-color: #0c0c0c;
        z-index: 99;
        padding-bottom: 15px;
        border-bottom: 1px solid #1f1f1f;
    }

    .profile-img { 
        border-radius: 50%; 
        width: 110px; height: 110px; 
        border: 3px solid #1DB954;
        object-fit: cover;
        box-shadow: 0 0 15px rgba(29, 185, 84, 0.4);
    }

    /* Song Cards: PC par Grid (2 columns), Mobile par List */
    .song-card {
        background: #181818;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #282828;
        margin-top: 15px;
        transition: 0.3s;
    }
    .song-card:hover { border-color: #1DB954; }

    /* Audio Player Styling */
    audio { 
        width: 100%; 
        height: 40px;
        filter: invert(100%) hue-rotate(180deg) brightness(1.5);
        margin-top: 10px;
    }

    /* Mobile Text Adjustment */
    @media (max-width: 600px) {
        .song-title { font-size: 14px !important; }
        .profile-img { width: 90px; height: 90px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sticky Header Section ---
st.markdown('<div class="header-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # Aapki Profile Photo aur Naam
    st.markdown(f'<center><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"><h1 style="color:#1DB954; margin-top:10px; font-family:sans-serif;">Aj Pro Player</h1></center>', unsafe_allow_html=True)

# Search aur Shuffle Controls
col_search, col_shuffle = st.columns([4, 1])
with col_search:
    query = st.text_input("", placeholder="🔍 Singer, Gaana ya Playlist search karein...")
with col_shuffle:
    st.write("<div style='height:15px;'></div>", unsafe_allow_html=True) # Mobile spacing
    shuffle_on = st.toggle("🔀 Shuffle")
st.markdown('</div>', unsafe_allow_html=True)

# --- Music Logic Section ---
if query:
    # 20 gaane fetch karne ke liye settings
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch20', 
        'noplaylist': True,
        'nocheckcertificate': True,
        'proxy': '' # Glitch avoid karne ke liye
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            with st.spinner('🎵 Aapki Super Playlist ready ho rahi hai...'):
                info = ydl.extract_info(query, download=False)
                results = info['entries']
            
            if shuffle_on:
                random.shuffle(results)

            # PC par 2 columns, Mobile par auto 1 column (Responsive Grid)
            for i in range(0, len(results), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(results):
                        song = results[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="song-card">
                                    <div style="display: flex; align-items: center; gap: 12px;">
                                        <img src="{song.get('thumbnail')}" style="width:55px; height:55px; border-radius:8px; object-fit:cover;">
                                        <div style="line-height: 1.3;">
                                            <b class="song-title" style="color:#fff; font-size:15px;">{song.get('title')[:55]}...</b><br>
                                            <small style="color:#b3b3b3;">{song.get('uploader')} • {song.get('duration_string')}</small>
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            # Direct Audio Player (No YouTube Redirect)
                            st.audio(song.get('url'), format='audio/mp3')

        except Exception as e:
            st.error("Glich Alert! Shayad YouTube server ne block kiya ya internet slow hai. 1-2 minute baad try karein.")
else:
    # Jab search khali ho tab ye dikhega
    st.markdown("""
        <div style="text-align: center; margin-top: 80px; color: #444;">
            <h3>🎧 Welcome to your Personal Ad-Free Player</h3>
            <p>Upar search box mein kisi bhi Singer ka naam likhein (e.g. Arijit Singh)</p>
        </div>
    """, unsafe_allow_html=True)

# --- Professional Footer (Spotify Style) ---
st.markdown("""
    <div style="background-color: #121212; padding: 25px; border-radius: 20px; margin-top: 60px; border-top: 2px solid #1DB954; text-align: center;">
        <h4 style="color: #1DB954; margin-bottom: 5px; font-family: sans-serif;">Aj Pro Player v3.5</h4>
        <p style="color: #b3b3b3; font-size: 14px;">
            Designed & Developed by <b>Aniruddh Singh (Aj)</b><br>
            Enjoy 20+ hits with <b>Suffer Mode</b> (Shuffle) & Zero Ads.
        </p>
        <div style="font-size: 11px; color: #555; letter-spacing: 1px;">
            TIP: USE CHROME BROWSER FOR BEST EXPERIENCE
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)
