from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import sys

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test_user:test@db:3306/test_database")

Base = declarative_base()

server = Flask(__name__)
server.config["DEBUG"] = True
CORS(server)

# Create a SQLAlchemy session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# Actual routes
@server.route('/')
def hello():
    return bhelpers.json_return("Hi, this appears to work")

@server.route('/reset')
def reset():
    Base.metadata.drop_all(engine)
    return "Success, db reset done."

@server.route('/database_initial_setup')
def dbsetup():
    class Users(Base):
        __tablename__ = 'users'
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        username = sqlalchemy.Column(sqlalchemy.String(length=30))
        email    = sqlalchemy.Column(sqlalchemy.String(length=30))
        password = sqlalchemy.Column(sqlalchemy.String(length=32))
    
    class Reccomandations(Base):
        __tablename__ = 'reccomandations'
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        artist   = sqlalchemy.Column(sqlalchemy.String(length=32))
        songname = sqlalchemy.Column(sqlalchemy.String(length=32))
        spotlink = sqlalchemy.Column(sqlalchemy.String(length=32))
        userid   = sqlalchemy.Column(sqlalchemy.Integer)
    
    class Session(Base):
        __tablename__ = 'sessions'
        sid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        uid = sqlalchemy.Column(sqlalchemy.Integer)
        ttl = sqlalchemy.Column(sqlalchemy.Integer)     # In hours
    
    Base.metadata.create_all(engine);
    return "The DB was succesfully initialized"
#
## Route to receive info on available number of tokens to request services
#@server.route('/availabletokens/<userid>')
#def availabletokens(userid):
#    return jsonify({'available_tokens': bhelpers.run_sql_query(bqueries.get_available_token_query(userid))})  # :)
#
#
#@server.route('/prevracc/<userid>')
## Instantiate Connection
#def racc(userid):
#    return jsonify({'reccomandations_for_user': bhelpers.run_sql_query(bqueries.get_reccomandation_for_user_query(userid))})
#
#
#@server.route('/add_user', methods=['POST'])
#def add_user():
#    # Assume the data is sent as JSON in the request body
#    if request.method == 'POST':
#    # Get JSON data
#        user_data = request.json
#        
#        username = user_data.get('username')
#        email = user_data.get('email')
#        password = user_data.get('password')
#
#        #name = user_data.get('name')
#        availabletokenquantity = user_data.get('availabletokenquantity')
#        availabletokenquantity = 10
#        query = bqueries.insert_user_query(username, email, password)
#
#        # Executing signup query (TO-BE completed)
#        bhelpers.run_sql_query(query)
#        bhelpers.run_sql_query(bqueries.show_all_users(), True)
#
#        if not (username and email and password):
#            return jsonify({'error': 'Missing required fields'}), 400
#
#        return jsonify({'message': 'User added successfully'}), 200
#
#    else:
#        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
#        return jsonify({'error': 'Method not allowed'}), 405
#
##@server.route('/delete_user/<userid>')
##def delete_user(userid):
##
#
#@server.route('/user_data/<userid>')
#def userdata(userid):
#    return jsonify({'user_data': bhelpers.run_sql_query((bqueries.get_user_data_query(userid), True))})
#
#@server.route('/check_user_existence_id/<userid>')
#def user_exists(userid):
#    return check_user_existence_id(userid)
#
#@server.route('/check_user_existence_username/<username>')
#def user_exists_uname(username):
#    return check_user_existence_username(username)
#
#@server.route('/check_user_existence_email/<email>')
#def user_exists_email(email):
#    return check_user_existence_email(email)

if __name__ == '__main__':
    server.run()

