import requests
import json

# Set your API token
token = "BQA7rGi5xpZF8E2Xo-hFXVRC3A-Q5JJ4D_Z2C6oovdsK7-WibVu8ux-EiGEarnQ6_HzAsx88auScQsCBeAgteHXRtVzjHLMqrQCcTyigJl_UGcq0bhgm"

# Set the playlist ID
playlist_id = "2vWk4sRkPU4adhmGirW5OW"

# Set the Spotify API endpoint for retrieving a playlist by ID
endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"

def get_playlist_tracks(playlist_id, token):
    # Set the Spotify API endpoint for retrieving a playlist by ID
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

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
        for item in playlist_data['items']:
            track = item['track']
            track_id = track['id']
            track_ids.append(track_id)

        # Return list of track IDs
        return track_ids
    else:
        # Print the error message
        print(f"Error: {response.content}")
        return []
    
track_ids = get_playlist_tracks(playlist_id,token)

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
    
valences = get_track_valences(track_ids, token)

print(valences)