from flask import Flask, jsonify, request
import sys
from flask_cors import CORS

# Defined by us
import businessqueries as bqueries
import businesshelpers as bhelpers

server = Flask(__name__)
server.config["DEBUG"] = True
CORS(server)

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
    # Ottenere i dati JSON inviati nella richiesta
        user_data = request.json
    #user_data = request.json
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')
        #name = user_data.get('name')
        #availabletokenquantity = user_data.get('availabletokenquantity')
        #availabletokenquantity = 10
        query = bqueries.insert_user_query(username, email, password)
        bhelpers.run_sql_query(query)
        if not (username and email and password):
            return jsonify({'error': 'Missing required fields'}), 400

        return jsonify({'message': 'User added successfully'}), 200

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

    


   

if __name__ == '__main__':
    server.run()

