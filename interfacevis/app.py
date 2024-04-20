from flask import Flask, render_template, request, flash, jsonify, session, redirect
import requests

app = Flask(__name__)
app.secret_key = 'secret-key'

# Businesslogic base url
bl_url="http://mscrcmnd-businesslogic-1:5000/"


@app.route('/')
def homepage():
    if 'username' in session:
        return render_template('index.html', active_page='index', username=session['username'])
    return render_template('index.html', active_page='index')

@app.route('/about')
def about():
    if('username' in session):
        return render_template('about.html', active_page='about', username=session['username'])
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
    else:
        if 'username' in session:
            return render_template('contact.html', active_page='contact', username=session['username'])
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

        if ret.status_code == 200:
            flash("Login successful!", "success")
            session['logged_in'] = True
            session['user_id'] = ret.json()['user_id']
            session['username'] = username
            return redirect('/')
        else:
            flash(error_handler(ret.status_code, ret.json()), 'danger')
            return render_template('login.html', active_page='login')


    # GET request
    if "username" in session:
        return redirect("/")
    return render_template('login.html', active_page='login')


@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out', 'success')
    return render_template('index.html', active_page='index')

# Return profile page of user
@app.route('/profile', methods=['GET'])
def profile():
    if request.method == 'GET':
        if 'username' in session:
            user = get_user(session['user_id'])
            return render_template('profile.html', active_page='profile', user = user)
        else:
            flash("Error, you're not logged in", "danger")
            return render_template('index.html', active_page='index')
    else:
        return jsonify("{'error': 'Method not allowed'}"), 405

        
@app.route('/delete', methods=['GET'])
def delete():
    if request.method == 'GET':
        if 'username' in session:
            print(session['username'])
            ret = requests.get(bl_url+"delete/"+str(session['user_id']))
            if ret.status_code == 200:
                session.clear()
                flash("Account deleted successfully", 'success')
                return redirect('/')

            else: 
                return error_handler(ret.status_code, ret.json())
        
        else:
            flash("You must be logged in", 'danger')
            return redirect('/')
    
    else:
        flash(error_handler(405, 'Method not allowed'), 'danger')
        return redirect("/")
    

@app.route('/profile/add_tokens/<int:val>', methods=['GET'])
def add_tokens(val):
    if 'username' in session:
        print(session['username'])
        ret = requests.get(bl_url+'add_token/'+str(session['user_id'])+"/"+str(val))
        
        if ret.status_code == 200:
            flash(f"Successfully added {val} tokens", 'success')
            return profile()
        else:
            print('ERROR')
            flash(error_handler(ret.status_code, ret.json()), 'danger')
            return profile()



# AUX FUNCTIONS
def error_handler(code, txt={"error": "Unknown error!"} ):
    return txt["error"]

def get_user(user_id):
    data = {'id': str(user_id)}
    ret = requests.post(bl_url +"user_id", json = data)
    return ret.json()




if __name__ == "__main__":
    app.run(debug=True)
