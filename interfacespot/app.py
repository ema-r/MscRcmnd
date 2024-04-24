import os
from flask import Flask, jsonify, request

import spotify_secrets

token = spotify_secrets.token

app = Flask(__name__)

# Import spotify

@app.route('/')
def hello():
    return jsonify({'hello': 'world'})

@app.route('/spotify_search/<song_title>')
def srch(song_title):
    url_endpoint = 'https://api.spotify.com/v1/search?q=track'+song_title+"&type=track&market=IT&limit=1"

    ret = request.get(url_endpoint).headers({'Authorization: Bearer ': token})

    if ret.status_code == 200:        
        song_id = ret.get_json().items[0].id
        return jsonify({'song_id': song_id}), 200

    elif ret.status_code == 401:
        return jsonify({'error' : 'Bad or expired spotify auth token. Contact an Admin;'}), 401

    elif ret.status_code == 403:
        return jsonify({'error' : 'Bad oauth request. Contact an Admin;'}), 403

    elif ret.status_code == 429:
        return jsonify({'error' : 'App has exceeded rate limits. Contact an Admin;'}), 429

@app.route('/spotify_song_link/<song_id>')
def get_link(song_id):
    return jsonify({'song_link' : ('https://open.spotify.com/track/'+song_id)}), 200

if __name__ == '__main__':
    app.run()
