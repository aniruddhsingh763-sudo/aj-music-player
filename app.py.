import streamlit as st
import yt_dlp
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="Aj Music Pro", layout="wide")

# Force JavaScript to handle audio pause (This will run in the browser background)
components.html(
    """
    <script>
    const interval = setInterval(() => {
        const audios = window.parent.document.querySelectorAll('audio');
        audios.forEach(audio => {
            if (!audio.dataset.listener) {
                audio.dataset.listener = "true";
                audio.addEventListener('play', (event) => {
                    audios.forEach(a => {
                        if (a !== event.target) {
                            a.pause();
                        }
                    });
                });
            }
        });
    }, 1000);
    </script>
    """,
    height=0,
)

# Advanced CSS for Spotify Feel
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .profile-img { border-radius: 50%; width: 120px; height: 120px; border: 3px solid #1DB954; box-shadow: 0 4px 20px rgba(29, 185, 84, 0.5); }
    .stButton>button { border-radius: 20px; background-color: #282828; color: white; border: 1px solid #1DB954; transition: 0.3s; width: 100%; }
    .stButton>button:hover { background-color: #1DB954; color: black; }
    .download-btn { background-color: #1DB954; color: white !important; padding: 8px 15px; text-decoration: none; border-radius: 20px; font-size: 14px; font-weight: bold; display: inline-block; margin-top: 10px; }
    audio { filter: invert(100%) hue-rotate(180deg) brightness(1.5); width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
c1, c2, c3 = st.columns([1,1,1])
with c2:
    st.markdown(f'<center><img src="https://i.postimg.cc/rpd79wYM/IMG-20220517-WA0009.jpg" class="profile-img"></center>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Aj Pro Player</h2>", unsafe_allow_html=True)

st.write("---")

# --- Mood Shortcuts ---
st.subheader("Explore Moods")
m1, m2, m3, m4 = st.columns(4)
mood_search = ""
if m1.button("🔥 Party Hits"): mood_search = "Latest Punjabi Party Songs"
if m2.button("🎸 Sad Vibes"): mood_search = "Hindi Sad Songs"
if m3.button("💪 Gym Beast"): mood_search = "Punjabi Gym Workout Songs"
if m4.button("🌙 Relaxing"): mood_search = "Lo-fi Hindi Chill"

# --- Search Bar ---
user_query = st.text_input("", placeholder="Gaana ya Singer ka naam likhein...", value=mood_search)

# Function to fetch and display songs
def display_songs(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch8',
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(query, download=False)['entries']
            for song in results:
                with st.container():
                    col_thumb, col_play = st.columns([1, 4])
                    with col_thumb:
                        st.image(song.get('thumbnail'), use_container_width=True)
                    with col_play:
                        title = song.get('title')
                        audio_url = song.get('url')
                        st.markdown(f"**{title}**")
                        st.markdown(f"<small style='color:gray'>{song.get('uploader')}</small>", unsafe_allow_html=True)
                        st.audio(audio_url)
                        st.markdown(f'<a href="{audio_url}" download="{title}.mp3" class="download-btn">📥 Download MP3</a>', unsafe_allow_html=True)
                    st.markdown("<hr style='border: 0.1px solid #333'>", unsafe_allow_html=True)
        except:
            st.error("Kuch problem aa rahi hai. Page refresh karke dekhein.")

if user_query:
    display_songs(user_query)
else:
    st.info("Gaana search karein aur enjoy karein!")
