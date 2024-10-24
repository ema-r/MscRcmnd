import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, update

ml_url="http://mscrcmnd-mlengine-1:5000/"

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test_user:test@db:3306/test_database")
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String(length=30), unique=True)
    email    = sqlalchemy.Column(sqlalchemy.String(length=30))
    password = sqlalchemy.Column(sqlalchemy.Text()) # password hash is bigger than a string
    availabletokens = sqlalchemy.Column(sqlalchemy.Integer)

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)
    
    def check_password(self, psw):
        return check_password_hash(self.password, psw)
    
    def to_dict(self):
        return {'id': self.id,
            'username': self.username,
            'email': self.email,
            'tokens': self.availabletokens}

class Song(Base):
    __tablename__ = 'Songs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    artist   = sqlalchemy.Column(sqlalchemy.String(length=32))
    songname = sqlalchemy.Column(sqlalchemy.String(length=32))
    spotlink = sqlalchemy.Column(sqlalchemy.String(length=32))

class Reccomandation(Base):
    __tablename__ = 'Reccomandations'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer)
    songid = sqlalchemy.Column(sqlalchemy.Integer)

class Review(Base):
    __tablename__ = 'Review'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer)
    songid = sqlalchemy.Column(sqlalchemy.Integer)      # Actually recommandation id
    rating = sqlalchemy.Column(sqlalchemy.Float)

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


# SIGN UP route
@server.route('/users', methods=['GET','POST'])
def user():
    user_data = request.json
    # Assume the data is sent as JSON in the request body
    if request.method == 'POST':
        # Insert user data
        new_username = user_data.get('username').lower()
        new_email = user_data.get('email').lower()

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
        new_user = User(username=new_username, email=new_email,
                        availabletokens=new_availabletokens)
        # Set hashed password
        new_user.set_password(new_password)

        # Saving it in the db
        try:
            session.add(new_user)
            session.commit()
        except(SQLAlchemyError) as e:
            error = str(e.__dict__['orig'])
            print(error)
            session.rollback()
            return jsonify({'error': "Cannot connect to database, try again later"}), 503

        return jsonify({'message': 'User added successfully'}), 200

    else:
        # Se la richiesta non è una richiesta POST, restituisci un errore 405 (Method Not Allowed)
        return jsonify({'error': 'Method not allowed'}), 405

# LOGIN ROUTE
@server.route('/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        uname = request.json.get("username", None).lower()
        pword = (request.json.get("password", None))

        uid = get_user_id(uname)

        userdata = session.query(User).filter(User.username == uname).first()

        if(userdata is None):
            return jsonify({'error': 'User does not exist'}), 404
        
        if (userdata.check_password(pword)):
            return jsonify({'result': 'successfully logged in', 'user_id': uid}), 200
        
        else: return jsonify({'error': 'wrong username or password'}), 409

    else:
        return jsonify({'error': 'Method not allowed'}), 405


# path to get the whole user from its id
@server.route('/user_id', methods=['POST'])
def get():
    user_data = request.json.get('id', None)
    user = session.query(User).get(user_data)
    
    if user is None:
        return jsonify({'error': "User doesn't exist"}), 404
    else:
        print(user.to_dict())
        return jsonify(user.to_dict())
    

@server.route('/delete/<int:user_id>')
def delete(user_id):
    print(user_id)
    if delete_user(user_id):
        return jsonify({'result': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'Cannot delete user'}), 409

@server.route('/add_token/<int:user_id>/<int:val>')
def add_token(user_id, val):
    if(add_token_to_user(user_id, val)):
        return jsonify({'success': f'added {val} tokens'}), 200
    else: return jsonify({'error': 'Cannot add tokens'}), 409

@server.route('/get_recommandation/<int:user_id>')
def get_rec(user_id):
    print('lol')

@server.route('/update_review/<int:user_id>/<int:reccomandation_id',
              methods = ['POST'])
def update_rev(user_id, reccomandation_id):
    if request.method == 'POST':
        rating = request.json.get("rating")

        # Check if a review with this combination of ids exists
        if (does_review_exist):
            return jsonify
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

def does_review_exist(user_id, reccomandation_id):
    review = session.execute(
            select(Review.id).where(Review.userid == user_id and Review.songid == reccomandation_id)).first()
    if review is None:
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

def delete_user(user_id):
    try:
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
    except SQLAlchemyError as e:
        error=str(e.__dict__['orig'])
        print(error)
        session.rollback()
        return False
    return True

def add_token_to_user(user_id, val):
    try:
        user=session.query(User).filter_by(id=user_id).update({User.availabletokens: User.availabletokens + val})
        session.commit()
        return True
    except:
        session.rollback()
        return False

        


# Server initialization
@server.route('/reset')
def reset():
    Base.metadata.drop_all(engine)
    return jsonify({'result': "DB succesfully reset"})

@server.route('/database_initial_setup')
def dbsetup():
    Base.metadata.create_all(engine)
    return jsonify({'result': "DB succesfully initialized"})

if __name__ == '__main__':
    server.run()

