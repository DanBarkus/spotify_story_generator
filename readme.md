# Spotbot

## What is it?
Spotbot uses ChatGPT to generate stories based on your Spotify playlists or albums in general.

## How do I set it up?
You'll need:
- OpenAI API key: [how to get](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)
- Spotify API key: [how to get](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- Node
- Python

### The backend
- Navigate to the `api` folder
- From there, run `pip install -r requirements.txt` to install requirements
- Use `python gpt_interface.py` to start the backend

### The frontend
- Navigate to the `spotbot` folder
- Run `npm install` to install requirements
- `npm run serve` will start the frontend