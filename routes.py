from app import app
import secrets
from flask import render_template, request, redirect, session, abort
import users

#MAINPAGE
@app.route("/")
def index():
    username = session.get('username')
    return render_template("index.html", username=username)

#CREATEACCOUNT
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        session['csrf_token'] = secrets.token_hex(16)
        return render_template("create_account.html", csrf_token=session['csrf_token'])
    
    if request.method == 'POST':
        if session.get('csrf_token') != request.form.get('csrf_token'):
            abort(403)  # Lopeta pyyntö, jos CSRF-token ei täsmää
        
        username = request.form['username']
        password = request.form['password']

        # Käyttäjänimen ja salasanan pituuden tarkistus
        if len(username) < 3 or len(username) > 50:
            return render_template("create_account.html", error="Username must be 3-50 characters long.", csrf_token=session['csrf_token'])
        if len(password) < 8:
            return render_template("create_account.html", error="Password must be at least 8 characters long.", csrf_token=session['csrf_token'])

        if users.create_account(username, password):
            return redirect('/')
        
        return render_template("create_account.html", error="Username already taken or registration failed.", csrf_token=session['csrf_token'])


#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session['csrf_token'] = secrets.token_hex(16)
        return render_template("login.html", csrf_token=session['csrf_token'])
    
    if request.method == 'POST':
        if session['csrf_token'] != request.form['csrf_token']:
            return redirect('/login')
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
        return render_template("login.html", error="Wrong username or password", csrf_token=session['csrf_token'])

#LOGOUT
@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')


