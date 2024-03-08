import os
from flask import Flask
import mysql.connector

server = Flask(__name__)
conn = None

@server.route('/')
def hello():
    return "hello"


if __name__ == '__main__':
    server.run()
