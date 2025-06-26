import requests
from bs4 import BeautifulSoup
import re

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

    # Filter out junk lines before actual lyrics
    lyrics_lines = []
    start_found = False
    for line in raw_lines:
        if not start_found:
            if re.search(r"(Contributors|Translations|Read More|Lyrics|Album|Released|Featuring|Produced)", line, re.IGNORECASE):
                continue
            if len(line.strip().split()) >= 4:
                start_found = True
                lyrics_lines.append(line.strip())
        else:
            lyrics_lines.append(line.strip())

    # Clean [Verse], etc.
    cleaned = [re.sub(r"\[.*?\]", "", l).strip() for l in lyrics_lines if l.strip()]

    # Group multi-line parentheses content into a single line
    formatted_lines = []
    buffer = []
    in_parens = False

    for line in cleaned:
        if in_parens:
            buffer.append(line)
            if ")" in line:
                combined = " ".join(buffer)
                formatted_lines.append(combined)
                buffer = []
                in_parens = False
        else:
            if line.startswith("(") and not line.endswith(")"):
                buffer = [line]
                in_parens = True
            else:
                formatted_lines.append(line)

    # In case we never closed the parenthesis
    if buffer:
        formatted_lines.append(" ".join(buffer))

    return "\n".join(formatted_lines) if formatted_lines else None

# Example usage
if __name__ == "__main__":
    url = "https://genius.com/Taylor-swift-love-story-lyrics"
    lyrics = get_lyrics(url)
    print(lyrics)
