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

songs_data['artists'] = songs_data['artists'].apply(lambda x: x[1:-1].split(',')[0])
song_data = songs_data.merge(song_genres, on="artists", how = 'inner')

song_data.isnull().sum()
song_data.dropna(inplace = True)
song_data.drop_duplicates(subset=['name'], keep='first', inplace=True)
song_data = song_data.sort_values(by=['popularity'], ascending=False).head(25000)
song_data = song_data.drop(columns=['release_date', 'mode', 'id', 'year'])

# start server
app = Flask(__name__)
app.config["DEBUG"] = True

# needs query on user id, and reccomendations from the user. We need to add a music id table
@app.route('/get_reccomandation', methods = ['POST'])
def get_rec():
    song_title = request.json.get('song_title', None)
    song_artist = request.json.get('song_artist', None)

    # Actual calculation
    song_vectorizer = CountVectorizer()
    song_vectorizer.fit(song_data['genres'])

    if song_data[song_data['name'] == song_title].empty:
        return jsonify({"error": "song not found"}, 404)
    
    song_data.head()

    working_dataframe = song_data.copy()

    return_data = recommend_song(song_title, song_artist, working_dataframe, song_vectorizer)

    print("return data names: ", return_data['name'])
    print("return data artists: ", return_data['artists'])


    return jsonify({"name":return_data['name'].values[0], "artist":return_data['artists'].values[0]}), 200

def get_similiarities(song_name, song_artist, music_data, vectorizer):
    # Get input song vector
    print("calculating similiarities...")
    reduced_dataframe = music_data.copy()
    reduced_dataframe.drop(columns=['popularity'])

    text_data_array = vectorizer.transform(reduced_dataframe[reduced_dataframe['name'] == song_name]['genres']).toarray()
    num_data_array = reduced_dataframe[reduced_dataframe['name']== song_name].select_dtypes(include=numpy.number).to_numpy()

    # Cycle through songs to calc similiarities
    similiarities = []
    for idx, row in reduced_dataframe.iterrows():
        song2_name = row['name']

        text_data_array2 = vectorizer.transform(reduced_dataframe[reduced_dataframe['name'] == song2_name]['genres']).toarray()
        num_data_array2  = reduced_dataframe[reduced_dataframe['name']==song2_name].select_dtypes(include=numpy.number).to_numpy()

        text_sim = cosine_similarity(text_data_array, text_data_array2)[0][0]
        num_sim  = cosine_similarity(num_data_array, num_data_array2)[0][0]
        similiarities.append(text_sim + num_sim)
    return similiarities

def recommend_song(song_name, artist_name, music_data, vectorizer):
    music_data['similiarity_factor'] = get_similiarities(song_name, artist_name, music_data, vectorizer)
    print("song name: ", song_name)
    print("artist name: ", artist_name)
    music_data_result = music_data[music_data['artists'] != ("'"+artist_name+"'")]
    music_data_result.sort_values(by=['similiarity_factor'],
                           ascending = False,
                           inplace = True)

    print("artist: \n", music_data_result['artists'][2:7])
    print("song_title: \n", music_data_result['name'][2:7])
    return music_data_result[2:5]

if __name__ == '__main__':
    app.run()
