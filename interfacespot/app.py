import os
from flask import Flask, jsonify, request
import spotify_secrets as spot
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'hello': 'world'})

@app.route('/spotify_search', methods=["POST"])
def search():
    title = request.json.get("title")
    artist = request.json.get("artist")
    limit = request.json.get('limit')
    query = get_URL_query(title, artist)

    print(query, flush=True)

    try:
        ret = spot.sp.search(q=query, type='track', limit=limit)
    except:
        return jsonify({"error": "Error fetching the request"}), 500
    
    result = comp_search(ret)

    if(result):
        return result, 200
    else: return jsonify({"error": "No songs found"}), 404


def get_URL_query(title, artist):
    query = ''
    if(artist is ''):
        query = f'track:"{title}"'
    elif(title is ''):
        query = f'artist:"{artist}"'
    else:
        query = f'track:"{title}" artist:"{artist}"'

    return query

@app.route('/spotify_song_link/<song_id>')
def get_link(song_id):
    return jsonify({'song_link' : ('https://open.spotify.com/track/'+song_id)}), 200

###########################
# AUX FUNCTIONS
###########################

def comp_search(ret):
    artist_tracks = {}

    for i, t in enumerate(ret['tracks']['items']):
        artist_name = t['artists'][0]['name']
        track_data = {
            'track': t['name'],
            'preview': t['preview_url'],
            'url': t['external_urls']['spotify'],
        }

        artist = spot.sp.artist(t['artists'][0]['uri'])
        if artist['images']:
            track_data['img'] = artist['images'][0]['url']
        else:
            track_data['img'] = None

        # Aggiungi il track_data al dizionario di liste
        if artist_name in artist_tracks:
            artist_tracks[artist_name].append(track_data)
        else:
            artist_tracks[artist_name] = [track_data]

    return dict_to_ordered_json_array(artist_tracks)


# to mantain order during json transfer
def dict_to_ordered_json_array(sorted_dict):
    ordered_list = [
        {
            "artist": artist,
            "tracks": tracks  # Each entry remains a list of track dictionaries
        }
        for artist, tracks in sorted_dict.items()
    ]

    # Convert the ordered list to JSON
    ordered_json = json.dumps(ordered_list, ensure_ascii=False, indent=4)
    return ordered_json


if __name__ == '__main__':
    app.run()
