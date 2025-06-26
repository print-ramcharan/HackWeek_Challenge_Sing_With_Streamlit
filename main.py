import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from bs4 import BeautifulSoup
import time

# ---------------- Configuration ----------------
GENIUS_API_TOKEN = ""

# Demo fallback lyrics
demo_lyrics = {
    "Love Story": """We were both young when I first saw you
I close my eyes and the flashback starts
I'm standing there on a balcony in summer air
See the lights, see the party, the ball gowns
See you make your way through the crowd and say \"Hello\"
Little did I know..."""
}

# ---------------- Genius API Helpers ----------------
def get_song_path(title):
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    response = requests.get(f"https://api.genius.com/search?q={title}", headers=headers).json()
    try:
        path = response['response']['hits'][0]['result']['path']
        return f"https://genius.com{path}"
    except:
        return None

def get_lyrics(url):
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.text, "html.parser")
    lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})

    if not lyrics_divs:
        return None

    raw_lines = []
    for div in lyrics_divs:
        lines = div.get_text(separator="\n", strip=True).split("\n")
        raw_lines.extend(lines)

    lyrics_lines = []
    start_found = False
    for line in raw_lines:
        if not start_found:
            if re.search(r"(Contributors|Translations|Read More|Lyrics|Album|Released|Produced|Featuring)", line, re.IGNORECASE):
                continue
            if len(line.strip().split()) >= 4:
                start_found = True
                lyrics_lines.append(line.strip())
        else:
            lyrics_lines.append(line.strip())

    cleaned = [re.sub(r"\[.*?\]", "", l) for l in lyrics_lines if l]
    return "\n".join(cleaned).strip() if cleaned else None

# ---------------- Word Cloud Generator ----------------
def generate_wordcloud(text):
    if not text or not isinstance(text, str):
        st.warning("Lyrics are empty or invalid. Cannot generate word cloud.")
        return

    clean_text = re.sub(r"[^\w\s]", "", text).strip()
    if not clean_text:
        st.warning("Lyrics only contain special characters. Cannot generate word cloud.")
        return

    words = clean_text.split()
    if len(words) == 0:
        st.warning("No valid words found in lyrics to generate a word cloud.")
        return

    try:
        wc = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(" ".join(words))
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except ValueError:
        st.warning("Word cloud generation failed. No usable content in lyrics.")

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Taylor Swift Lyrics Visualizer", layout="wide")

st.markdown("""
    <style>
    .kanye-tooltip {
        position: fixed;
        bottom: 10px;
        right: 10px;
        z-index: 9999;
        opacity: 0.8;
    }

    .kanye-tooltip img {
        width: 80px;
        border-radius: 8px;
    }

    .kanye-tooltip:hover::after {
        content: "Beyoncé had the best music video of all time.";
        position: absolute;
        bottom: 90px;
        right: 0;
        background: #000;
        color: #fff;
        padding: 5px 8px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
    }
    </style>

    <div class="kanye-tooltip">
        <img src="https://media1.giphy.com/media/v1.Y2lkPTZjMDliOTUyMmJvbDhmb3k2emFvazR6NG5tM2g2MjNpN2w0eDV5cWYzaGlpOGNnMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/14tvbepZ8vhU40/source.gif">
    </div>
""", unsafe_allow_html=True)



song_title = st.text_input("Enter a Taylor Swift song title (e.g., Love Story)", help="Case-insensitive, try popular titles")

if song_title:
    lyrics = demo_lyrics.get(song_title.strip())
    if not lyrics:
        url = get_song_path(song_title)
        if url:
            with st.spinner("Fetching lyrics..."):
                lyrics = get_lyrics(url)

    if lyrics and isinstance(lyrics, str) and lyrics.strip():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎶 Animated Lyrics")
            delay = st.slider("Speed (seconds per line)", 0.2, 1.5, 0.5)
            if st.button("▶️ Start Lyric Animation"):
                placeholder = st.empty()
                for line in lyrics.strip().split("\n"):
                    if line.strip():
                        placeholder.markdown(f"<h4 style='text-align:center'>{line}</h4>", unsafe_allow_html=True)
                        time.sleep(delay)
                placeholder.success("🎉 Done!")

        with col2:
            st.markdown("#### ☁️ Word Cloud")
            generate_wordcloud(lyrics)

    else:
        st.error("Couldn't fetch usable lyrics. Try a different song.")
