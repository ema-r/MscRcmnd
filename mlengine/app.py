from pyspark import SparkConf, SparkContext
from flask import Flask, jsonify, request

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select

# conf spark session
conf = SparkConf()
conf.setMaster("local")
conf.setAppName("SparkContext1")
conf.set("spark.executor.memory", "1g")

# conf sql session
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test_user:test@db:3306/test_database")
Base = declarative_base()

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# start server
app = Flask(__name__)

# needs query on user id, and reccomendations from the user. We need to add a music id table
@app.route('/get_reccomandation/<int:user_id>')
def get_rec(user_id):
    return jsonify({'message': 'Reccomendation successfully added'}), 200

if __name__ == '__main__':
    app.run()
