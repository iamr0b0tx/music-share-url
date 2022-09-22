from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from utils import get_youtube_music_track_details, get_apple_music_track_details, get_spotify_track_details, \
    get_spotify_track_url

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/urls")
async def get_urls(platform: Literal["apple-music", "spotify", "youtube-music"], url: str):
    try:
        title, artist = {
            "apple-music": get_apple_music_track_details,
            "youtube-music": get_youtube_music_track_details,
            "spotify": get_spotify_track_details,
        }[platform](url)

        urls = {}
        for service in ["apple-music", "spotify", "youtube-music"]:
            if platform == service:
                continue

            urls[service] = {
                "apple-music": get_spotify_track_url,
                "youtube-music": get_spotify_track_url,
                "spotify": get_spotify_track_url,
            }[service](title, artist)

    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")

    return urls


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
