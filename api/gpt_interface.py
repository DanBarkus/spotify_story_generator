import os
import csv
import random
import openai
from google.cloud import texttospeech
from dotenv import load_dotenv
import base64
import requests
import json
from flask import Flask, jsonify, request
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

# Set the playlist ID
playlist_id = "4Zs4LuGmHghwIDtbBNOGap"
album_id = "4SZko61aMnmgvNhfhgTuD3"

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

        # Extract track IDs from playlist data
        track_ids = []
        track_names = []
        playlist_title = playlist_data['name']
        for item in playlist_data['tracks']['items']:
            track = item['track']
            track_id = track['id']
            track_name = track['name']
            # Remove things like "Remastered" or "From X movie" from track titles
            track_name = track_name.split(' -')[0]
            # Remove featured artist blocks
            track_name = track_name.split(' (feat')[0]
            track_ids.append(track_id)
            track_names.append(track_name)
        # Return list of track IDs
        return track_ids,track_names,playlist_title
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
        track_ids = []
        track_names = []
        for track in album_data['tracks']['items']:
            track_id = track['id']
            track_name = track['name']
            track_ids.append(track_id)
            track_names.append(track_name)

        # Return the album name and list of track IDs
        return track_ids,track_names,album_name,artist,album_cover
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
    
# valences = get_track_valences(track_ids, token)
# valences = "|".join(str(v) for v in valences)
# track_names = "|".join(str(t) for t in track_names)

# print(track_names)
# print(valences)

# -------------- GPT Section ------------------

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_random_row(filename):
    # Open the CSV file
    with open(filename, 'r') as file:

        # Create a CSV reader object
        reader = csv.reader(file)

        # Read all the rows into a list
        rows = list(reader)

        # Pick a random row
        random_row = random.choice(rows)

        # Get the text value of the selected row
        random_text = random_row[0]

        # Return the text value
        return random_text

speak = False

# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
#     {"role": "system", "content": "I am going to give you a list of numbers between 0 and 1 where each of these numbers corresponds to a main character's fortune in a story at a given point in time. 0 is total misfortune and 1 is total fortune, the numbers are separated by the | character. Do not include the numbers in the output. I am also going to give you a list of titles that corresponds to the numbers, the titles are also separated by |. Do not mention the titles in the output"},
#     {"role": "user", "content": f"write me a detailed, fiction inspired by the phrase '{playlist_title}' where each chapter is loosely based on a title from the list of titles. Use each title and in order, don't mention the title in the body of the fiction. Make sure that the chapters flow into each other. The sequence of numbers is {valences}. Use every value in order, do not mention the values in the output. The sequence of titles is {track_names}, use these as chapter titles"}])
# output = completion.choices[0].message.content

# print(output)

if speak:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=output)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE, name="en-US-Neural2-I"
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, effects_profile_id=["small-bluetooth-speaker-class-device"]
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(f"{mood}_story_about_a_{subject}_that_{action}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

# ------------ API section -----------------

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(debug=True, port=5001)

