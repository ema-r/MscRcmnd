from flask import Flask, render_template, make_response, request, flash, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
            session['logged_in'] = True
            session['user_id'] = ret.json()['user_id']
            return render_template('index.html', active_page='index')
        else:
            flash(error_handler(ret.status_code, ret.json()), 'danger')
            return render_template('login.html', active_page='login')


    # GET request
    return render_template('login.html', active_page='login')


@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out')
    return render_template('index.html', active_page='index')

# Return JSON of user
@app.route('/user', methods=['GET'])
def userdata():
    if request.method == 'GET':
        if(session['user_id']== None):
            flash("Error, you're not logged in", "danger")
            return render_template('index.html', active_page='index')
        else:
            user = get_user(session['user_id'])
            return user, 200

    else:
        return jsonify("{'error': 'Method not allowed'}"), 405

        
def error_handler(code, txt={"error": "Unknown error!"} ):
    if(code==409): return txt["error"]
    else: return txt["error"]

def get_user(user_id):
    data = {'id': user_id}
    ret = requests.post(bl_url +"user_id", json = data)
    return ret.json()




if __name__ == "__main__":
    app.run(debug=True)
