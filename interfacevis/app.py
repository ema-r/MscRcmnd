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

        # Process the form data (you can add your own logic here)

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
        # Ottenere i dati inviati dalla form di registrazione
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Esegui il codice per salvare i dati dell'utente nel database o fare altre operazioni necessarie per la registrazione

        # Di solito, reindirizziamo l'utente a una pagina di conferma dopo la registrazione
        #return render_template('signup_confirmation.html', username=username)
    else:
        # Se la richiesta non è di tipo POST, restituisci semplicemente la pagina di registrazione
        return render_template('signup.html', active_page='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottieni i dati inviati dalla form di login
        username = request.form['username']
        password = request.form['password']

        # Esegui il codice per verificare le credenziali dell'utente nel database o in altro modo
        # In questo esempio, controlliamo solo se le credenziali sono corrette
        if username == 'admin' and password == 'password':
            return "Login successful! Welcome, {}".format(username)
        else:
            return "Login failed. Please check your username and password."

    # Se la richiesta non è di tipo POST, restituisci semplicemente la pagina di login
    return render_template('login.html', active_page='login')

if __name__ == "__main__":
    app.run(debug=True)
