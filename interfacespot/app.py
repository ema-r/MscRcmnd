import os
from flask import Flask, jsonify, request
import spotify_secrets as spot

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'hello': 'world'})

@app.route('/spotify_search', methods=["POST"])
def search():
    title = request.json.get("title")
    try:
        ret = spot.sp.search(title, type="track", limit=3)
    except:
        return jsonify({"error": "Error fetching the request"}), 500
    result = comp_search(ret)
    if(result):
        return jsonify(result), 200
    else: return jsonify({"error": "No songs found"}), 404

@app.route('/spotify_song_link/<song_id>')
def get_link(song_id):
    return jsonify({'song_link' : ('https://open.spotify.com/track/'+song_id)}), 200

###########################
# AUX FUNCTIONS
###########################

def comp_search(ret):
    artist_name = []
    track_name = []

    for i, t in enumerate(ret['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
    
    result_dict = {k: v for k, v in zip(artist_name, track_name)}
    print(result_dict, flush=True)
    
    return result_dict


if __name__ == '__main__':
    app.run()
