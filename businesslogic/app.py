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
    return jsonify({'result': "Hi, this appears to work"})

@server.route('/reset')
def reset():
    Base.metadata.drop_all(engine)
    return jsonify({'result': "DB succesfully reset"})

@server.route('/database_initial_setup')
def dbsetup():
    Base.metadata.create_all(engine);
    return jsonify({'result': "DB succesfully initialized"})

@server.route('/users', methods=['GET','POST'])
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

        new_user = User(username=new_username, email=new_email, password=func.md5(new_password),
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
            name = 'user_' + str(ind)
            result[name] = {'username':user[0], 'user_id':user[1],
                            'email':user[2], 'availabletokens':user[3]}
            ind += 1
        #print(result)
        return jsonify(result)

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

@server.route('/user/<uid>', methods=['GET', 'DELETE'])
def userdata(uid):
    if request.method == 'GET':
        user = session.execute(
                select(User.username, User.email, User.availabletokens).where(User.id == uid)
                ).first()
        if user is None:
            return jsonify({'error': 'no such user'})
        return jsonify({'username':user[0], 'email':user[1], 'availabletokens':user[2]})

    elif request.method == 'DELETE':
        return jsonify({'result':'user not deleted (to be implemented)'})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

@server.route('/user/<userid>/reccomandations', methods=['GET', 'POST'])
def raccs(userid):
    if request.method == 'GET' :
        reccomandations = session.execute(
                select(Reccomandation.songname, Reccomandation.artist).where(Reccomandation.userid == userid)
                ).all()

        ind = 1
        result = {}
        for recc in reccomandations:
            name = 'reccomandation_' + str(ind)
            result[name] = {'song_name': recc[0], 'artist': recc[1]}
            ind += 1

        return jsonify(result)

    elif request.method == 'POST':
        return jsonify({'error': 'to be implemented'})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

@server.route('/user/<userid>/reccomandation/<reccid>', methods=['GET'])
def racc(userid, reccid):
    if request.method == 'GET':
        recc = session.execute(
                select(Reccomandation.songname, Reccomandation.artist, Reccomandation.spotlink).where(
                    Reccomandation.userid == userid, Reccomandation.id == reccid
                    )
                )
        if recc is None:
            return jsonify({'error': 'no such reccomandation_'})
        return jsonify({'song_name': recc[0], 'artist': recc[1], 'spotify_link': recc[2]})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

# Utility functions
def does_user_exists(uid):
    user = session.execute(
            select(User).where(User.id==uid)
            ).first()
    if user is None:
        return False
    else:
        return True

def get_user_id(uname):
    user = session.execute(
            select(User.id).where(User.username==uname)
            ).first()

    if user is None:
        return ''
    else:
        return user[0]

if __name__ == '__main__':
    server.run()

