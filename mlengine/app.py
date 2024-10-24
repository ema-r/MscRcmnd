from flask import Flask, jsonify, request

import numpy
import pandas

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import cdist

# start server
app = Flask(__name__)
app.config["DEBUG"] = True

# needs query on user id, and reccomendations from the user. We need to add a music id table
@app.route('/get_reccomandation/')
def get_rec():
    song_title = request.args.get('song_title', None)
    song_artist = request.args.get('song_artist', None)

    song_data = pandas.read_csv("./data.csv")
    song_data.head()
    song_data.info() # Prints pretty info table
    
    # song_data cleaning
    song_data.isnull().sum()
    song_data.dropna(inplace = True)
    #song_data = song_data.drop(['artists', 'id', 'popularity', 'name', 'release_date'], axis = 1)
    
    # drop duplicate songs
    song_data = song_data.sort_values(by=['popularity'], ascending=False)
    song_data.drop_duplicates(subset=['name'], keep='first', inplace=True)
    
    # Actual calculation
    song_vectorizer = CountVectorizer()
    song_vectorizer.fit(song_data['genres'])

    recommend_song(song_title, song_data, song_vectorizer)

    return 200

# Data to use
song_data_cols = ['valence', 'acousticness', 'danceability', 'energy',
                 'instrumentalness', 'speechiness', 'liveness','tempo', 'key']

metasong_data_cols = ['name', 'year', 'artists']

def get_similiarities(song_name, music_data, vectorizer):
    # Get input song vector
    text_data_array = vectorizer.transform(music_data[music_data['name'] == song_name]['genres']).toarray()
    num_data_array = music_data[music_data['name']==song_name].select_dtypes(include=numpy.number).to_numpy()

    # Cycle through songs to calc similiarities
    similiarities = []
    for idx, row in music_data.iterrows():
        song2_name = row['name']

        text_data_array2 = vectorizer.transform(music_data[music_data['name'] == song2_name]['genres']).toarray()
        num_data_array2  = music_data[music_data['name']==song2_name].select_dtypes(include=numpy.number).to_numpy()

        text_sim = cosine_similarity(text_data_array, text_data_array2)[0][0]
        num_sim  = cosine_similarity(num_data_array, num_data_array2)[0][0]
        similiarities.append(text_sim + num_sim)
    return similiarities

def recommend_song(song_name, music_data, vectorizer):
    music_data['similiarity_factor'] = get_similiarities(song_name, music_data, vectorizer)
    music_data.sort_values(by=['similiarity_factor', 'popularity'],
                           ascending = [False, False],
                           inplace = True)

    return music_data[['name', 'artists']][2:7]

if __name__ == '__main__':
    app.run()
