import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "<p>hello</p>"


if __name__ == '__main__':
    app.run()
    print("test")
