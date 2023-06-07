import os
import openai
from dotenv import load_dotenv
import base64
import requests
import json
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin

load_dotenv()

#------------- Spotify section -------------
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


# Generate a new token when connecting
def get_spotify_token(client_id, client_secret):
    # Set the Spotify API endpoint for retrieving an access token
    endpoint = "https://accounts.spotify.com/api/token"

    # Encode the client ID and client secret as base64
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode("ascii")

    # Set the headers and body for the HTTP request
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }

    # Send the HTTP request to the Spotify API
    response = requests.post(endpoint, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON and extract the access token
        token_data = response.json()
        access_token = token_data['access_token']

        # Return the access token
        return access_token
    else:
        # Print the error message
        print(f"Error: {response.content}")
        return None


# Set your API token
token = get_spotify_token(client_id, client_secret)

def get_playlist_tracks(playlist_id, token):
    # Set the Spotify API endpoint for retrieving a playlist by ID
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    # Set the headers for the HTTP request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Send the HTTP request to the Spotify API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        playlist_data = json.loads(response.content)

        playlist_cover = playlist_data['images'][0]['url']

        playlist_creator = playlist_data['owner']['display_name']

        # Extract track IDs from playlist data
        tracks = []
        playlist_title = playlist_data['name']
        for item in playlist_data['tracks']['items']:
            track = item['track']
            print(track)
            n_track = {}
            n_track['name'] = track['name']
            n_track['id'] = track['id']
            n_track['album'] = track['album']['name']
            n_track['artists'] = track['artists'][0]['name']
            tracks.append(n_track)
        # Return list of track IDs
        return tracks,playlist_title,playlist_creator,playlist_cover,playlist_id
    else:
        # Print the error message
        print(f"Error: {response.content}")
        return []
    
def get_album_tracks(album_id, token):
    # Set the Spotify API endpoint for retrieving an album by ID
    endpoint = f"https://api.spotify.com/v1/albums/{album_id}"

    # Set the headers for the HTTP request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Send the HTTP request to the Spotify API
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        album_data = json.loads(response.content)

        # Extract the album name
        album_name = album_data['name']

        album_cover = album_data['images'][0]['url']

        artist = album_data['artists'][0]['name']

        # Extract the list of track IDs
        tracks = []
        for track in album_data['tracks']['items']:
            n_track = {}
            n_track['name'] = track['name']
            n_track['id'] = track['id']
            n_track['artists'] = track['artists']
            tracks.append(n_track)

        # Return the album name and list of track IDs
        return tracks,album_name,artist,album_cover,album_id
    else:
        # Print the error message
        print(f"Error: {response.content}")
        return None, None

def search_spotify(query):
    """Searches for playlists or albums on Spotify based on a given query string.

    Args:
        query (str): The query string to search for.

    Returns:
        dict: A dictionary containing the search results.
    """
    url = 'https://api.spotify.com/v1/search'
    params = {'q': query, 'type': 'playlist,album'}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error searching Spotify:', response.text)
        return None
    
# For playlists
# track_ids,track_names,playlist_title = get_playlist_tracks(playlist_id,token)

# For Albums
# track_ids,track_names,playlist_title = get_album_tracks(album_id,token)

def get_track_valences(track_ids, token):
    # Set the Spotify API endpoint for retrieving multiple tracks by ID
    endpoint = "https://api.spotify.com/v1/audio-features"

    # Set the headers for the HTTP request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Create a comma-separated string of track IDs
    id_string = ",".join(track_ids)

    # Set the query parameters for the HTTP request
    params = {
        "ids": id_string
    }

    # Send the HTTP request to the Spotify API
    response = requests.get(endpoint, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        track_data = json.loads(response.content)

        # Extract valence values from track data
        valences = []
        for track in track_data['audio_features']:
            valence = track['valence']
            valences.append(valence)

        # Return list of valence values
        return valences
    else:
        # Print the error message
        print(f"Error: {response.content}")
        return []
    
# -------------- GPT Section ------------------

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------ API section -----------------

app = Flask(__name__)
CORS(app)

def generate_story(playlist_title, track_names, valences):
    num_tracks = len(track_names.split('|'))
    print(track_names)
    print(num_tracks)
    messages = [
        {"role": "system", "content": "I want you to write me a story broken into chapters, each chapter should be relevant to the chapters before it and only about 5 sentances long. I only want you to return one chapter at a time. When I say 'next' you will respond with the next chapter. I will provide the tile of the story and all of the chapters together should tell the story of that title. Each chapter should be related to the relevant chapter title from the list of chapters and also have the mood of the chapter driven by the corresponding mood number from the list of numbers. I am going to provide you with a list of chapter titles and a list of mood numbers. The first chapter title corresponds to the first chapter and the first mood number. The second chapter title to the second chapter and second mood number and so on. The mood numbers will range from 0 to 1 where 0 is a bad mood and 1 is a good mood. Do not include the input chapter title or mood number."},
        {"role": "user", "content": f"The title of the story is {playlist_title}. The chapter titles are {track_names} and the mood numbers are {valences}. Please start the story after I prompt with 'next'."},
        {"role": "user", "content": "next"}
    ]
    story = []
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    for track in range(num_tracks):
        output = completion.choices[0].message.content
        yield output
        story.append(output)
        print(output)
        tmp_message = {"role": "assistant", "content": output}
        messages.append(tmp_message)
        messages.append({"role": "user", "content": "next"})
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

@app.route('/search', methods=['GET'])
@cross_origin()
def search_spot():
    search_string = request.args.get('q')
    results = search_spotify(search_string)
    response = jsonify(results)
    return response

@app.route('/get_album', methods=['GET'])
@cross_origin()
def get_album():
    album = request.args.get('album')
    results = get_album_tracks(album, token)
    response = jsonify(results)
    return response

@app.route('/get_playlist', methods=['GET'])
@cross_origin()
def get_playlist():
    album = request.args.get('playlist')
    results = get_playlist_tracks(album, token)
    response = jsonify(results)
    return response

@app.route('/generate_album', methods=['GET'])
@cross_origin()
def generate_album():
    album_id = request.args.get('album_id')
    is_album = request.args.get('album')
    print(album_id)
    if is_album:
        tracks,playlist_title,artist,album_cover,id = get_album_tracks(album_id,token)
    else:
        tracks,playlist_title,artist,album_cover,id = get_playlist_tracks(album_id,token)
    track_ids = [track['id'] for track in tracks]
    track_names = [track['name'] for track in tracks]
    valences = get_track_valences(track_ids, token)
    valences = "|".join(str(v) for v in valences)
    for idx, track_name in enumerate(track_names):
            # Remove things like "Remastered" or "From X movie" from track titles
            track_name = track_name.split(' -')[0]
            # Remove featured artist blocks
            track_name = track_name.split(' (feat')[0]
            track_names[idx] = track_name
    track_names = "|".join(str(t) for t in track_names)
    return Response(generate_story(playlist_title,track_names,valences), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

