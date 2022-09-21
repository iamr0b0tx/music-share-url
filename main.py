import requests
from bs4 import BeautifulSoup


def get_spotify_track_details(spotify_url):
    """ takes url and return song title and artist name """
    response = requests.get(spotify_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("meta", property="og:title")
    description = soup.find("meta", property="og:description")

    title = title and title["content"]
    artist = description and description["content"].split(" · Song · ")[0].strip()
    return title, artist


def get_apple_music_track_details(apple_music_url):
    """ takes url and return song title and artist name """
    response = requests.get(apple_music_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("meta", attrs={"name": "apple:title"})
    title = title and title["content"]
    description = soup.find("meta", property="og:title")
    artist = title and description["content"].replace(f"{title} by", "", 1).strip()
    return title, artist


def get_youtube_music_track_details(yt_music_url):
    """ takes url and return song title and artist name """
    response = requests.get(yt_music_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("meta", property="og:title")
    video_tags = soup.findAll("meta", property="og:video:tag")
    title_tag = title and next(filter(lambda x: x["content"] in title["content"], video_tags), None)
    title = title_tag and title_tag["content"]
    artist = video_tags and video_tags[0]["content"]
    return title, artist


if __name__ == '__main__':
    # url = "https://open.spotify.com/track/2Ka2eZtnllhJ8hukVLkXmt?si=RjLJTg0pTXOtZ1hWN-YGng&context=spotify%3Astation%3Atrack%3A60OEb5MtEmmepJPUJtYvFW"
    url = "https://open.spotify.com/track/7o2CTH4ctstm8TNelqjb51?si=e03a989b1c034a26"
    print(get_spotify_track_details(url))

    url = "https://music.apple.com/ng/album/sweet-child-o-mine/1377826053?i=1377826892"
    print(get_apple_music_track_details(url))

    url = "https://music.youtube.com/watch?v=oMfMUfgjiLg&feature=share"
    print(get_youtube_music_track_details(url))