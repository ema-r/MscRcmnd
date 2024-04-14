from flask import Flask, jsonify, request
import sys
from flask_cors import CORS
import json

# Defined by us
import businessqueries as bqueries
import businesshelpers as bhelpers

server = Flask(__name__)
server.config["DEBUG"] = True
CORS(server)

def check_user_existence_id(userid):
    user = bhelpers.run_sql_query(bqueries.get_user_by_id(userid), True)
    try:
        if(userid in user[0]):
            return True
        else: return False
    
    except:
        return False

def check_user_existence_username(username):
    user = bhelpers.run_sql_query(bqueries.get_user_by_username(username), True)
    try:
        if(username in user[0]):
            return True
        else: return False
    
    except:
        return False

def check_user_existence_email(email):
    user = bhelpers.run_sql_query(bqueries.get_user_by_email(email), True)
    try:
        if(email in user[0]):
            return True
        else: return False
    
    except:
        return False


@server.route('/reset')
def reset():
    bhelpers.run_sql_query("DROP TABLE Users;")
    dbsetup()
    return bhelpers.json_return("Success")

@server.route('/database_initial_setup')
def dbsetup():
    bhelpers.run_sql_query(bqueries.get_conditional_user_table_creation_query())
    bhelpers.run_sql_query(bqueries.get_conditional_reccomandation_table_creation_query())

    return bhelpers.json_return("The DB was succesfully initialized")

@server.route('/')
def hello():
    return bhelpers.json_return("Hi, this appears to work")

# Route to receive info on available number of tokens to request services
@server.route('/availabletokens/<userid>')
def availabletokens(userid):
    return jsonify({'available_tokens': bhelpers.run_sql_query(bqueries.get_available_token_query(userid))})  # :)


@server.route('/prevracc/<userid>')
# Instantiate Connection
def racc(userid):
    return jsonify({'reccomandations_for_user': bhelpers.run_sql_query(bqueries.get_reccomandation_for_user_query(userid))})


@server.route('/add_user', methods=['POST'])
def add_user():
    # Assume the data is sent as JSON in the request body
    if request.method == 'POST':
    # Get JSON data
        user_data = request.json
        
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')

        # Check if user is already registered
        if(check_user_existence_email(email) or check_user_existence_username(username)):
            return jsonify({'error': 'User already exists'}), 409 # Error 409, conflict

        #name = user_data.get('name')
        availabletokenquantity = user_data.get('availabletokenquantity')
        availabletokenquantity = 10
        query = bqueries.insert_user_query(username, email, password)

        # Executing signup query (TO-BE completed)
        bhelpers.run_sql_query(query)

        if not (username and email and password):
            return jsonify({'error': 'Missing required fields'}), 400

        return jsonify({'message': 'User added successfully'}), 200

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

#@server.route('/delete_user/<userid>')
#def delete_user(userid):
#

@server.route('/user_data/<userid>')
def userdata(userid):
    return jsonify({'user_data': bhelpers.run_sql_query((bqueries.get_user_data_query(userid), True))})

@server.route('/check_user_existence_id/<userid>')
def user_exists(userid):
    return check_user_existence_id(userid)

if __name__ == '__main__':
    server.run()

