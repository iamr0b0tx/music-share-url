try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from utils import get_youtube_music_track_details, get_apple_music_track_details, get_spotify_track_details, \
    get_spotify_track_url_info, get_apple_music_track_url_info, get_youtube_music_track_url_info

app = FastAPI()


@app.get("/urls")
async def get_urls(platform: Literal["apple-music", "spotify", "youtube-music"], url: str):
    try:
        title, artist = {
            "apple-music": get_apple_music_track_details,
            "youtube-music": get_youtube_music_track_details,
            "spotify": get_spotify_track_details,
        }[platform](url)

        urls = []
        for service in ["apple-music", "spotify", "youtube-music"]:
            if platform == service:
                continue

            urls.append({
                "apple-music": get_apple_music_track_url_info,
                "youtube-music": get_youtube_music_track_url_info,
                "spotify": get_spotify_track_url_info,
            }[service](title, artist))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Item not found")

    return urls


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
