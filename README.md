# Lyrics Visualizer

This Streamlit web app allows users to enter the title of a Taylor Swift song, fetches the lyrics using the Genius API, and displays them line-by-line with animation. It also generates a word cloud from the lyrics for visual analysis.

## Features

- Fetches real-time lyrics using the Genius API
- Displays animated lyrics line by line
- Generates a word cloud of frequently used words
- Simple and responsive UI

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/print-ramcharan/HackWeek_Challenge_Sing_With_Streamlit.git  
   cd lyrics-visualizer
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your Genius API token in the `GENIUS_API_TOKEN` variable inside `app.py`.

5. Run the app:

   ```bash
   streamlit run app.py
   ```

6. Open your browser and go to `http://localhost:8501` to use the app.

## Deployment

The app is deployed using [Streamlit Community Cloud](https://streamlit.io/cloud).  
Deployed Link: **[]**

