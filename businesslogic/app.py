from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import sys

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test_user:test@db:3306/test_database")

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(length=30))
    email    = sqlalchemy.Column(sqlalchemy.String(length=30))
    password = sqlalchemy.Column(sqlalchemy.String(length=32))
    availabletokens = sqlalchemy.Column(sqlalchemy.Integer)

class Reccomandation(Base):
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

# Create a SQLAlchemy session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

server = Flask(__name__)
server.config["DEBUG"] = True
CORS(server)

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
@server.route('/user', methods=['GET','POST'])
def user():
    # Assume the data is sent as JSON in the request body
    if request.method == 'POST':
    # Get JSON data
        user_data = request.json
        
        # Insert user data
        new_username = user_data.get('username')
        new_email = user_data.get('email')
        new_password = user_data.get('password')
        new_availabletokens = 10

        if not (new_username and new_email and new_password):
            return jsonify({'error': 'Missing required fields'}), 400

        new_user = User(username=new_username, email=new_email, password=new_password,
                        availabletokens=new_availabletokens)

        session.add(new_user)
        session.commit()

        return jsonify({'message': 'User added successfully'}), 200

    elif request.method == 'GET':
        users = session.execute(
                select(User.username, User.id, User.email, User.availabletokens)
                ).all()
        ind = 1
        result = {}
        for user in users:
            name = 'user' + chr(ind)
            user_result = []
            for element in user:
                user_result.append(element)
            result[name] = user_result

            ind += 1
        print(result)
        return jsonify(result)

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

@server.route('/user/<uid>', methods=['GET, DELETE'])
def userdata(uid):
    if request.method == 'GET':
        user = session.execute(
                select(User.username, User.email, User.availabletokens).where(User.id==uid)
                ).first()

        return jsonify({'username':user[0], 'email':user[1], 'availabletokens':user[2]})

    elif request.method == 'DELETE':
        return jsonify({'result':'user not deleted (to be implemented)'})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

# Utility functions
#def does_user_exists(id):
    
#@server.route('/check_user_existence_id/<userid>')
#def user_exists(userid):
#    return check_user_existence_id(userid)
#
#@server.route('/check_user_existence_username/<username>')
#def user_exists_uname(username):
#   return check_user_existence_username(username)
#
#@server.route('/check_user_existence_email/<email>')
#def user_exists_email(email):
#    return check_user_existence_email(email)

if __name__ == '__main__':
    server.run()

