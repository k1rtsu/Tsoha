from app import app
import secrets
from flask import render_template, request, redirect, session, abort
import users
from regions import get_regions, regions_posts_count, regions_topics_count, get_region
from topics import get_topics, topic_posts_count, get_topic
from posts import get_posts


#MAINPAGE
@app.route("/")
def index():
    username = session.get('username')
    regions = get_regions()
    
    post_count = regions_posts_count()
    topic_count = regions_topics_count()

    return render_template("index.html", username=username, regions=regions, 
                           regions_topic_count=topic_count, regions_post_count=post_count)


#CREATEACCOUNT
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        session['csrf_token'] = secrets.token_hex(16)
        return render_template("create_account.html", csrf_token=session['csrf_token'])
    
    if request.method == 'POST':
        if session.get('csrf_token') != request.form.get('csrf_token'):
            abort(403)  
        
        username = request.form['username']
        password = request.form['password']


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

#REGION
@app.route("/region/<int:region_id>")
def region(region_id):
    region = get_region(region_id)
    topics = get_topics(region_id)
    topics_with_post_counts = [
        {
            "id": topic[0],
            "title": topic[2],
            "description": topic[3],
            "post_count": topic_posts_count(topic[0]),
        }
        for topic in topics
    ]
    return render_template("region.html", region=region, topics=topics_with_post_counts)

#TOPIC
@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    topic = get_topic(topic_id)
    posts = get_posts(topic_id)
    return render_template("topic.html", topic=topic, posts=posts)
