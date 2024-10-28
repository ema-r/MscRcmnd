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

# set up pandas dataset
songs_data   = pandas.read_csv("./data.csv")
song_genres = pandas.read_csv("./data_w_genres.csv")

song_genres = song_genres[['genres', 'artists']]
song_genres['genres'] = song_genres['genres'].astype(str)
#song_genres['artists'] = numpy.array_str(song_genres['artists'])

songs_data.info()
song_genres.info()

#songs_data = songs_data.loc[:, 'genres'] = songs_data.artists.map(lambda x: x[0])
songs_data['artists'] = songs_data['artists'].apply(lambda x: x[1:-1].split(',')[0])
print("song data1: ", songs_data['artists'])
print("genres: ", song_genres['artists'])
song_data = songs_data.merge(song_genres, on="artists", how = 'inner')
print("song data3: ", song_data['artists'])

# start server
app = Flask(__name__)
app.config["DEBUG"] = True

# needs query on user id, and reccomendations from the user. We need to add a music id table
@app.route('/get_reccomandation', methods = ['POST'])
def get_rec():
    song_title = request.json.get('song_title', None)
    song_artist = request.json.get('song_artist', None)

    print("requested song:", song_title)
    print("by artist:", song_artist)

    song_data.head()
    song_data.info() # Prints pretty info table
    print("GENRES: ",song_data['genres'])
    
    # song_data cleaning
    song_data.isnull().sum()
    song_data.dropna(inplace = True)
    #song_data = song_data.drop(['artist_name', 'id', 'popularity', 'track_name', 'release_date'], axis = 1)
    
    # drop duplicate songs
    # song_data = song_data.sort_values(by=['popularity'], ascending=False)
    song_data.drop_duplicates(subset=['name'], keep='first', inplace=True)
    
    # Actual calculation
    song_vectorizer = CountVectorizer()
    song_vectorizer.fit(song_data['genres'])

    return_data = recommend_song(song_title, song_data, song_vectorizer)

    print("returned data: ", return_data)

    return jsonify({"songs":{"name":return_data[0]}}), 200

# Data to use
song_data_cols = ['valence', 'acousticness', 'danceability', 'energy',
                 'instrumentalness', 'speechiness', 'liveness','tempo', 'key']

metasong_data_cols = ['track_name', 'year', 'artist_name']

def get_similiarities(song_name, music_data, vectorizer):
    # Get input song vector
    print("GENRES FOR CHOSEN SONG: ", music_data[music_data['name'] == song_name]['genres'])
    print(vectorizer.transform(music_data[music_data['name'] == song_name]['genres']).toarray())
    text_data_array = vectorizer.transform(music_data[music_data['name'] == song_name]['genres']).toarray()
    num_data_array = music_data[music_data['name']== song_name].select_dtypes(include=numpy.number).to_numpy()

    print(text_data_array)
    print(num_data_array)

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
    music_data.sort_values(by=['similiarity_factor'],
                           ascending = False,
                           inplace = True)

    #return music_data[['track_name', 'artist_name']][2:7]
    print("songs: ", music_data['name'])
    print("artist: ", music_data['artists'][2:7])
    print("song_title: ", music_data['name'][2:7])
    return (music_data['name'][2], music_data['artists'][2])

if __name__ == '__main__':
    app.run()
