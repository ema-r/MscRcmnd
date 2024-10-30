import os
from flask import Flask, jsonify, request

import requests
import secrets

# Businesslogic base url
bl_url="http://mscrcmnd-businesslogic-1:5000/"

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'hello': 'world'})

@app.route('/get_user_data', methods=['POST'])
def get_data():
   if request.method == 'POST':
        r_user_id = request.json.get("user_id", None)
        r_api_token = request.json.get("api_credential", None)

        if are_credentials_valid(r_user_id, r_api_token):
            data = {'id': r_user_id}
            ret = requests.post(bl_url+"user_id", json=data)
            if ret.status_code == 200:
                return ret.json, 200
            else:
                return jsonify({'error': 'Error recovering reccomandations'}), 405

   else:
       return jsonify({'error': 'Method not allowed'}), 405

@app.route('/get_past_reccomandations', methods=['POST'])
def get_recs():
   if request.method == 'POST':
        r_user_id = request.json.get("user_id", None)
        r_api_token = request.json.get("api_credential", None)

        if are_credentials_valid(r_user_id, r_api_token):
            ret = requests.get(bl_url+"reccomandations/"+r_user_id)
            if ret.status_code == 200:
                return ret.json, 200
            else:
                return jsonify({'error': 'Error recovering reccomandations'}), 405

   else:
       return jsonify({'error': 'Method not allowed'}), 405

@app.route('/get_user_tokens', methods=['POST'])
def get_tokens():
   if request.method == 'POST':
        r_user_id = request.json.get("user_id", None)
        r_api_token = request.json.get("api_credential", None)

        if are_credentials_valid(r_user_id, r_api_token):
            ret = requests.get(bl_url+"reccomandations/"+r_user_id)
            if ret.status_code == 200:
                return ret.json, 200
            else:
                return jsonify({'error': 'Error recovering reccomandations'}), 405

   else:
       return jsonify({'error': 'Method not allowed'}), 405

@app.route('/get_reccomandation', methods=['POST'])
def get_recco():
    if request.method == 'POST':
        r_user_id = request.json.get("user_id", None)
        r_api_token = request.json.get("api_credential", None)
        r_song_title = request.json.get("song_title", None)
        r_artist = request.json.get("artist", None)

        if are_credentials_valid(r_user_id, r_api_token):
            data = {'song_title':r_song_title, 'song_artist':r_artist}
            ret = requests.get(bl_url+"/get_new_recommendation/"+r_user_id, json=data)
            if ret.status_code == 200:
                return ret.json, 200
            else:
                return jsonify({'error': 'Error recovering reccomandations'}), 405

    else:
       return jsonify({'error': 'Method not allowed'}), 405

@app.route('/submit_review', methods=['POST'])
def submit_review():
   if request.method == 'POST':
        r_user_id = request.json.get("user_id", None)
        r_api_token = request.json.get("api_credential", None)
        r_reccomandation_id = request.json.get("reccomandation_id", None)

        if request.json.get("evaluation") == "positive":
            r_evaluation = 1.0
        else:
            r_evaluation = 0.0

        if are_credentials_valid(r_user_id, r_api_token):
            data = {'rating': r_evaluation}
            ret = requests.post(bl_url+"update_review/"+r_user_id+"/"+r_reccomandation_id, json = data)
            if ret.status_code == 200:
                return ret.json, 200
            else:
                return jsonify({'error': 'Error recovering reccomandations'}), 405

   else:
       return jsonify({'error': 'Method not allowed'}), 405

#@app.route('/getAPIcredentials', methods=['POST'])
#def getAPIcreds():
#    if request.method == 'POST':
#        r_username = request.json.get("username", None)
#        r_password_hash = request.json.get("password_hash", None)
#        
#        if (does_username_exists(r_username)):
#            password = session.execute(select(User.password).where(User.username == r_username)).first()
#            if r_password_hash == password:
#                apitoken = session.execute(select(User.apicred).where(User.username == r_username)).first()
#                return jsonify({'api_token':apitoken})
#            else:
#                return jsonify({'error': 'password incorrect'}), 403
#
#        else:
#            return jsonify({'error': 'Username does not exist'}), 404
#
#    else:
#        return jsonify({'error': 'Method not allowed'}), 405

# Helper functions
def are_credentials_valid(userid, api_credentials):
    data={"user_id": userid, "apicred": api_credentials}
    ret=requests.post(bl_url+"addmessages", json=data)

    if ret.status_code == 200:
        if ret.json()["result"] == "Success":
            return True
        else:
            return False
    else:
        return False


# standard request format
#   if request.method == 'POST':
#   else:
#       return jsonify({'errro': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run()
