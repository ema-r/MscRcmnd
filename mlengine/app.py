from flask import Flask, jsonify, request

import numpy
import pandas

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist

# start server
app = Flask(__name__)

# Columns to use
columnIndexes = ['valence', 'acousticness', 'danceability', 'energy',
                 'instrumentalness', 'speechiness', 'liveness','tempo', 'key']

# needs query on user id, and reccomendations from the user. We need to add a music id table
@app.route('/get_reccomandation/<str:song_title>&<str:song_artist>')
def get_rec(song_title, song_artist):
    
    data = pandas.read_csv("./data.csv")
    
    metadataCols = ['name', 'year', 'artists']
    
    song_data = get_song_data_from_csv(song_title, song_artist, data)

    songVector   = get_song_vector(song_data) 

    scaler = song_clustering_pipeline.steps[0][1]
    scaled_data = scaler.transform(data[columnIndexes])
    scaled_song_center = scaler.transform(songVector.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])

    rec_song = data.iloc[index]

    return jsonify({'message': rec_song[columnIndexes].to_dict(orient='records')}), 200

def get_song_data_from_csv(song_name, song_artist, csv_data):
    try:
        song_data = csv_data[(csv_data['name'] == song_name)] & csv_data[(csv_data['artists'] == song_artist)]
        return song_data

    except IndexError:
        return jsonify("error")

def get_song_vector(song_data):
    return song_vector = song_data[columnIndexes].values

if __name__ == '__main__':
    app.run()
