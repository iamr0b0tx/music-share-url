# music-share-url
![example workflow](https://github.com/iamr0b0tx/music-share-url/actions/workflows/main.yml/badge.svg) <br>
Generate urls for a track given url for a track from any platform. Currently, supports Spotify and YouTube Music.

Application currently hosted at [https://music-url-share.herokuapp.com/](https://music-url-share.herokuapp.com/)

## API specifications
- URLs API: The route `/urls` will return the specific all urls for all supported platforms. Example response
```json
[
    {
        "linkText": "Coming Soon",
        "link": "https://music.apple.com/us/browse",
        "service": "Apple Music"
    },
    {
        "linkText": "https://open.spotify.com/track/3bt6gBOA41MHQfXy0Jf855",
        "link": "https://open.spotify.com/track/3bt6gBOA41MHQfXy0Jf855",
        "service": "Spotify"
    }
]
```

## Project setup
Before going through the steps make sure you have the following pre-installed

### Tools and Resources
1. Python 3.6+
2. Virtualenv


__Note__: _Make sure to download/clone this repository and navigate to the folder in your terminal. Now follow the instructions below_

1. Create the virtual environment.
```
    virtualenv /path/to/venv --python=/path/to/python3
```
You can find out the path to your `python3` interpreter with the command `which python3`.

2. Set up `.env` file by duplicating the `.example.env` file(and editing if required).

3. Activate the environment and install dependencies.
    - #### Linux
    ```
        source /path/to/venv/bin/activate
        pip install -r requirements.txt
    ```

    - #### Windows
    ```
        ./path/to/venv/bin/activate
        pip install -r requirements.txt
    ```

4. Launch the service
```
    uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000
```

## Run locally
When the service is running, try this link in your browser/Postman. send a GET request
```
    127.0.0.1:8000
```

You can test the project with pytest by running the command. You can check Github Actions for the status of tests [here](https://github.com/iamr0b0tx/uuid-api/actions) 
```
    pytest
```

This project id based heavily on this setup [Audio Files API](https://github.com/iamr0b0tx/audio_files_api)

# References
1. FastAPI Documentation. [link](https://fastapi.tiangolo.com/)
2. Requests Documentation. [link](https://requests.readthedocs.io/en/master/)
3. Pytest Documentation. [link](https://docs.pytest.org/en/stable/contents.html)
