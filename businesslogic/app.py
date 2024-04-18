import json

from flask import Flask, jsonify, request

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func


engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test_user:test@db:3306/test_database")
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(length=30))
    email    = sqlalchemy.Column(sqlalchemy.String(length=30))
    password = sqlalchemy.Column(sqlalchemy.String(length=32))
    availabletokens = sqlalchemy.Column(sqlalchemy.Integer)

class Reccomandation(Base):
    __tablename__ = 'Reccomandations'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    artist   = sqlalchemy.Column(sqlalchemy.String(length=32))
    songname = sqlalchemy.Column(sqlalchemy.String(length=32))
    spotlink = sqlalchemy.Column(sqlalchemy.String(length=32))
    userid   = sqlalchemy.Column(sqlalchemy.Integer)

# Create a SQLAlchemy session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# Server creation and config
server = Flask(__name__)
server.config["DEBUG"] = True


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
    Base.metadata.create_all(engine)
    return jsonify({'result': "DB succesfully initialized"})


# SIGN UP route
@server.route('/users', methods=['GET','POST'])
def user():
    user_data = request.json
    # Assume the data is sent as JSON in the request body
    if request.method == 'POST':
        # Insert user data
        new_username = user_data.get('username')
        new_email = user_data.get('email')

        # Check if user already exists
        try:
            if does_username_exists(new_username):
                return jsonify({'error': "Username already exists"}), 409 # Username already taken

            if does_email_exists(new_email):
                return jsonify({'error': "Email already registered"}), 409 # Email already registered

        except:
            return jsonify({'error': 'Cannot communicate with the db'}), 503


        # User exists, we can now register him
        new_password = user_data.get('password')
        new_availabletokens = 10

        # New user instance from its model
        new_user = User(username=new_username, email=new_email, password=func.md5(new_password),
                        availabletokens=new_availabletokens)

        # Saving it in the db
        try:
            session.add(new_user)
            session.commit()
        except:
            session.rollback()
            return jsonify({'error': 'Error communicating with the db'}), 503

        return jsonify({'message': 'User added successfully'}), 200


    # Method to retrieve users' data
    elif request.method == 'GET':
        return jsonify({})

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

# LOGIN ROUTE
@server.route('/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        uname = request.json.get("username", None)
        pword = func.md5(request.json.get("password", None))

        uid = get_user_id(uname)
        print(uid)

        userdata = session.execute(
                select(User.password).where(User.username == uname)
                ).first()

        if userdata is None:
            return jsonify({'result': 'wrong username or password'}), 409
        
        return jsonify({'result': 'successfully logged in', 'user_id': uid}), 200

    else:
        return jsonify({'error': 'Method not allowed'}), 405

# Serves user info for GET, deletes user with DELETE
@server.route('/user/<uid>', methods=['POST', 'DELETE'])
def userdata(uid):
    # New check that utilizes the JWT to check if user is authorized to access; any JWT will clear
    # the preliminary check, this one will make sure requested user id is the same as the one of
    # user making the request
    if request.method == 'POST':
        user = session.execute(
                select(User.username, User.email, User.availabletokens).where(User.id == uid)
                ).first()

        if user is None:
            return jsonify({'error': 'no such user'})
        return jsonify({'username':user[0], 'email':user[1], 'availabletokens':user[2]})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

@server.route('/user/<userid>/reccomandations', methods=['GET', 'POST'])
def raccs(userid):

    if not is_user(get_jwt_identity(), userid):
        return jsonify({'error': 'Not authorized'}), 403

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

    if not is_user(get_jwt_identity(), userid):
        return jsonify({'error': 'Not authorized'}), 403

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


@server.route('/user_id', methods=['POST'])
def get():
    print("getting user from id")
    user_data = request.json.get('id', None)
    user = session.execute(
                select(User.username, User.email).where(User.id == user_data)).first()
    
    print(user)
    if user is None:
        return jsonify({'error': "User doesn't exist"}), 404
    else:
        return jsonify({'username': user[0], 'email': user[1]})


# Utility functions

# Check if user exist before signup

# Check if username already taken
def does_username_exists(username):
    user = session.execute(
            select(User.username).where(User.username==username)).first()
    if user is None:
        return False
    else:
        return True

# Check if email already exists (so user already registered)    
def does_email_exists(email):
    user = session.execute(
            select(User.email).where(User.email==email)).first()
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

def is_user(token_uid, tried_uid):
    if tried_uid != token_uid:
        return False
    return True

if __name__ == '__main__':
    server.run()

