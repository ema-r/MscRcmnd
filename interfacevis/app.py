from flask import Flask, render_template, request, flash, jsonify
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies)
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'


jwt = JWTManager(app)

# Businesslogic base url
bl_url="http://mscrcmnd-businesslogic-1:5000/"


@app.route('/')
def homepage():
    return render_template('index.html', active_page='index')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

        
@app.route("/contact", methods=['GET', 'POST']) 
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        #(add own logic here)

        # For demonstration purposes, let's print the form data
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")

        # Flash a thank you message
        flash('Thank you for contacting us!', 'success')

        # Redirect to the homepage
        return jsonify({"Name": name})

    # If it's a GET request, render the contact form
    return render_template('contact.html', active_page='contact')
    

# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Sending data to businesslogic
        data={"username": username, "email": email, "password": password}
        ret=requests.post(bl_url+"users", json=data)

        if ret.status_code == 200:
            flash("Successfully registered!", "success")
            return render_template('index.html', active_page='index')
        else:
            flash(error_handler(ret.status_code, ret.json()), 'danger')
            return render_template('signup.html', active_page='signup')

    else:
        # If it's GET, return normal page
        return render_template('signup.html', active_page='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Check input data 
        data = {"username": username, "password": password}
        ret = requests.post(bl_url + f"users/login", json = data)
        print(ret)

        if ret.status_code == 200:
            flash("Login successful!", "success")
            access_token = create_access_token(identity=username)

            resp = jsonify({"login": 'True'})

            set_access_cookies(resp, access_token)
            return resp, 200
            #return render_template('index.html', active_page='index')
        else:
            flash("Login failed, wrong username or password", "Failure")
            return render_template('login.html', active_page='login')

        # if username == 'admin' and password == 'password':
        #     return "Login successful! Welcome, {}".format(username)
        # else:
        #     return "Login failed. Please check your username and password."

    # GET request
    return render_template('login.html', active_page='login')


@app.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({"logout": 'True'})
    unset_jwt_cookies(resp)
    return resp, 200

# Route meant to test JWT cookies working as intended.
@app.route('/user', methods=['GET'])
@jwt_required()
def userdata():
    if request.method == 'GET':
        username = get_jwt_identity()
        return jsonify({'hello': 'from {}'.format(username)}), 200

    else:
        return jsonify("{}")

        
def error_handler(code, txt={"error": "Unknown error!"} ):
    if(code==409): return txt["error"]
    else: return txt["error"]



if __name__ == "__main__":
    app.run(debug=True)
