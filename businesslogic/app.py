import json

from flask import Flask, jsonify, request
from flask_cors import CORS

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

secrets = {}
with open("./business_secrets.json", "r") as rf:
    secrets = json.load(rf)

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

#class Session(Base):
#    __tablename__ = 'Sessions'
#    sid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#    uid = sqlalchemy.Column(sqlalchemy.Integer)
#    ttl = sqlalchemy.Column(sqlalchemy.Integer)     # In hours

# Create a SQLAlchemy session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# Server creation and config
server = Flask(__name__)
server.config["DEBUG"] = True
server.config["JWT_SECRET_KEY"] = secrets['jwt_secret']

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
    Base.metadata.create_all(engine)
    return jsonify({'result': "DB succesfully initialized"})


# SIGN UP route
@server.route('/users', methods=['GET','POST'])
def user():
    # Assume the data is sent as JSON in the request body
    if request.method == 'POST':
    # Get JSON data
        user_data = request.json
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
        
        return jsonify(result)

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

# Allows login exclusively via post, returns json containing the needed JWT
@server.route('/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        uname = request.json.get("username", None)
        pword = func.md5(request.json.get("password", None))

        uid = get_user_id(uname)

        userdata = session.execute(
                select(User.password).where(User.username == uname)
                ).first()

        if userdata is None:
            return jsonify({'result': 'wrong username or password'})
        
        if userdata[0] != pword:
            return jsonify({'result': 'wrong username or password'})
        
        access_token = create_access_token(identity=uid)
        return jsonify({'result': 'successfully logged in', 'access_token': access_token})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

# Serves user info for GET, deletes user with DELETE
@server.route('/user/<uid>', methods=['POST', 'DELETE'])
@jwt_required()
def userdata(uid):
    # New check that utilizes the JWT to check if user is authorized to access; any JWT will clear
    # the preliminary check, this one will make sure requested user id is the same as the one of
    # user making the request
    if request.method == 'POST':

        if not is_user(get_jwt_identity(), uid):
            return jsonify({'error': 'Not authorized'}), 403

        user = session.execute(
                select(User.username, User.email, User.availabletokens).where(User.id == uid)
                ).first()

        if user is None:
            return jsonify({'error': 'no such user'})
        return jsonify({'username':user[0], 'email':user[1], 'availabletokens':user[2]})

    else:
        return jsonify({'error': 'Method not allowed'}), 405

@server.route('/user/<userid>/reccomandations', methods=['GET', 'POST'])
@jwt_required()
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
@jwt_required()
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

