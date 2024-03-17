import os
import flask

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return "<p>hello</p>"


if __name__ == '__main__':
    app.run()
    print("test")
