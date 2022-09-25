from urllib.parse import quote, urlparse

import requests
from bs4 import BeautifulSoup
from decouple import config
from requests import utils
from requests.auth import HTTPBasicAuth

YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')
SPOTIFY_CLIENT_ID = config("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET")
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/105.0.0.0 Safari/537.36', **utils.default_headers()}


def get_spotify_track_details(spotify_url):
    """ takes url and return song title and artist name """
    response = requests.get(spotify_url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("meta", property="og:title")
    description = soup.find("meta", property="og:description")
    title = title and title["content"]
    artist = description and description["content"].split(" · Song · ")[0].strip()
    return title, artist


def get_apple_music_track_details(apple_music_url):
    """ takes url and return song title and artist name """
    response = requests.get(apple_music_url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("meta", attrs={"name": "apple:title"})
    title = title and title["content"]
    description = soup.find("meta", property="og:title")
    artist = title and description["content"].replace(f"{title} by", "", 1).strip()
    return title, artist


def get_youtube_music_track_details(yt_music_url):
    """ takes url and return song title and artist name """
    parsed_url = urlparse(yt_music_url)
    video_id = parsed_url and parsed_url.query and parsed_url.query.replace("v=", "", 1)
    if not video_id:
        return None, None

    response = requests.get(f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&maxResults=1&"
                            f"id={video_id}&key={YOUTUBE_API_KEY}", headers=DEFAULT_HEADERS).json()
    title = response["items"][0]["snippet"]["title"]
    artist = response["items"][0]["snippet"]["channelTitle"].replace("- Topic", "", 1)
    return title, artist


def get_auth_credentials():
    response = requests.post(
        f"https://accounts.spotify.com/api/token", auth=HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
        data={"grant_type": "client_credentials"}, headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()


def get_auth_token():
    return get_auth_credentials()["access_token"]


def search_spotify(track_name, artist_name):
    q = quote(f"{track_name} track:{track_name} artist:{artist_name}")
    return requests.get(
        f"https://api.spotify.com/v1/search?type=track&include_external=audio&limit=1&q={q}",
        headers={
            "Authorization": f"Bearer {get_auth_token()}",
            "Content-Type": "application/json"
        }
    ).json()


def search_youtube(track_name, artist_name):
    q = quote(f"{track_name} {artist_name}")
    return requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&"
                        f"type=video&q={q}&key={YOUTUBE_API_KEY}", headers=DEFAULT_HEADERS).json()


def get_spotify_track_url_info(track_name, artist_name):
    track_info = search_spotify(track_name, artist_name)
    url = track_info["tracks"]["items"][0]["external_urls"]["spotify"]
    return {
        "linkText": url,
        "link": url,
        "service": "Spotify"
    }


def get_apple_music_track_url_info(track_name, artist_name):
    return {
        "linkText": "Coming Soon",
        "link": "https://music.apple.com/us/browse",
        "service": "Apple Music"
    }


def get_youtube_music_track_url_info(track_name, artist_name):
    track_info = search_youtube(track_name, artist_name)
    video_id = track_info["items"][0]["id"]["videoId"]
    link = video_id and f"https://music.youtube.com/watch?v={video_id}"
    return {
        "linkText": link,
        "link": link,
        "service": "YouTube Music"
    }


if __name__ == '__main__':
    # url = "https://open.spotify.com/track/2Ka2eZtnllhJ8hukVLkXmt?si=RjLJTg0pTXOtZ1hWN-YGng&context=spotify
    # %3Astation%3Atrack%3A60OEb5MtEmmepJPUJtYvFW" url =
    # "https://open.spotify.com/track/7o2CTH4ctstm8TNelqjb51?si=e03a989b1c034a26" print(get_spotify_track_details(url))
    #
    # url = "https://music.apple.com/ng/album/sweet-child-o-mine/1377826053?i=1377826892"
    # print(get_apple_music_track_details(url))
    #
    # url =
    # print(get_youtube_music_track_details(url))

    get_auth_token()
    print(get_spotify_track_url_info(
        *get_youtube_music_track_details("https://music.youtube.com/watch?v=oMfMUfgjiLg&feature=share")))
