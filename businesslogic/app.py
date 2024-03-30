from flask import Flask, jsonify
import sys

# Defined by us
import businessqueries as bqueries
import businesshelpers as bhelpers

server = Flask(__name__)
server.config["DEBUG"] = True

@server.route('/database_initial_setup')
def dbsetup():
    bhelpers.run_sql_queries([bqueries.get_conditional_user_table_creation_query(),
                     bqueries.get_conditional_reccomandation_table_creation_query()])

    return bhelpers.json_return("The DB was succesfully initialized")

@server.route('/')
def hello():
    return bhelpers.json_return("Hi, this appears to work");

# Route to receive info on available number of tokens to request services
@server.route('/availabletokens/<userid>')
def availabletokens(userid):
    return jsonify({'available_tokens': bhelpers.run_sql_queries([bqueries.get_available_token_query(userid)])})  # :)


@server.route('/prevracc/<userid>')
# Instantiate Connection
def racc(userid):
    return jsonify({'reccomandations_for_user': bhelpers.run_sql_queries([bqueries.get_reccomandation_for_user_query(userid)])})

if __name__ == '__main__':
    server.run()

