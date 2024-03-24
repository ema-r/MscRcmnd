from flask import Flask, render_template, request, redirect, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'


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
    
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        return jsonify({"Username": username, "Email": email})

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
        if username == 'admin' and password == 'password':
            return "Login successful! Welcome, {}".format(username)
        else:
            return "Login failed. Please check your username and password."

    # GET request
    return render_template('login.html', active_page='login')

if __name__ == "__main__":
    app.run(debug=True)
