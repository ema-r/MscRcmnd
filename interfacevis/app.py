from flask import Flask, render_template, request, flash, jsonify, session, redirect
import requests
from datetime import timedelta
from hashlib import md5
import json

app = Flask(__name__)
app.secret_key = 'secret-key'


# Session cookies security
app.permanent_session_lifetime = timedelta(days=60)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


# Businesslogic base url
bl_url="http://mscrcmnd-businesslogic-1:5000/"
# Spotify container base url
sp_url="http://mscrcmnd-interfacespot-1:5000/"

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

        # Sending data to businesslogic
        data={"name": name, "email": email, "message": message}
        ret=requests.post(bl_url+"addmessages", json=data)


        if ret.status_code == 200:
            flash("Thank you for contacting us!", "success")
            return render_template('index.html', active_page='index')
        else:
            flash("Failure to contact us", 'danger')
            return render_template('index.html', active_page='index')

    # If it's a GET request, render the contact form
    else:
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
        if('username' in session):
            return redirect("/")
        # If it's GET, return normal page
        return render_template('signup.html', active_page='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        remember = request.form.get('remember')

        # Check input data 
        data = {"username": username, "password": password}
        ret = requests.post(bl_url + f"users/login", json = data)

        if ret.status_code == 200:
            flash("Login successful!", "success")
            session['logged_in'] = True
            session['user_id'] = ret.json()['user_id']
            session['username'] = username

            if remember:
                session.permanent = True
            else:
                session.permanent = False
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
            return render_template('profile.html', active_page='profile', user = user, pic = get_pic(user["email"]))
        else:
            flash("Error, you're not logged in", "danger")
            return render_template('index.html', active_page='index')
    else:
        return jsonify("{'error': 'Method not allowed'}"), 405

        
@app.route('/get_rec', methods=['GET', 'POST'])
def get_rec():
    if "username" in session:
        if request.method == 'POST':
            # Process the form data
            song_title = request.form.get('song_title')

            results = retr_link(song_title)
            print(results, flush=True)

            # if the song exists
            if results:
                return render_template('get_rec.html', results = results, found = False)

            else: 
                flash("Song not found!", "danger")
                return render_template('get_rec.html', results = None)
        
        elif request.method == "GET":
            return render_template('get_rec.html', results=None)
    
    else: 
        flash("You must be logged in", "danger")
        return render_template("index.html", active_page="index")

@app.route('/recommendations', methods=['POST'])
def recommendations():
        if request.method == 'POST':
            if 'username' in session:
                # token substraction 
                print("\nTOKEN REMOVED!!!!\n")
                ret = requests.get(bl_url+'remove_token/'+str(session['user_id']))

                flash('Calculating a reccomandation. This may take a while...')
                if(ret.status_code == 200):
                    song_title = request.form.get('track_title', None)
                    song_artist = request.form.get('artist_name', None)
                    data = {"song_title":song_title, "song_artist":song_artist}
                    ret = requests.post(bl_url+"get_new_recommendation/"+str(session['user_id']),json=data)

                    if ret.status_code == 200:
                        print('\n\nRETURNNNN\n')
                        print(ret.json())
                        song_title = ret.json().get('songname')
                        song_artist = ret.json().get('artistname')
                        print("Song artist found: ", song_artist)
                        flash('Recommendation found!', 'success')
                        search_res = retr_link(song_title)
                        final_res = {}
                        final_res[song_artist] = search_res[song_artist]
                        return render_template('get_rec.html', results = final_res, found = True)
                    else:
                        flash(error_handler(ret.status_code, ret.json()), "danger")
                        return render_template('get_rec.html', results = None, found = False)
                    
                else:
                    flash(error_handler(ret.status_code, ret.json()), 'danger')
                    return render_template('index.html', active_page='index')




@app.route('/delete', methods=['GET'])
def delete():
    if request.method == 'GET':
        if 'username' in session:
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
    print("Error: "+str(code))
    return txt["error"]

def get_user(user_id):
    data = {'id': str(user_id)}
    ret = requests.post(bl_url +"user_id", json = data)
    return ret.json()

def get_pic(email, size=200, default='identicon', rating='g'):
    hash = md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash}?s={size}&d={default}&r={rating}"


def retr_link(song):
    data = {'title': song}
    data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    ret=requests.post(sp_url+"spotify_search", data=data, headers=headers)
    if(ret.status_code==200):
        print("found links: ", ret.json())
        return ret.json()
    else:
        error_handler(ret.status_code)
        return jsonify({'error': 'error'})


if __name__ == "__main__":
    app.run(debug=True)
