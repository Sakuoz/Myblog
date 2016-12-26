from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Sakura'} # fake user
    posts = [ # fake array of posts
        {
            'author': {'nickname': 'Sakura'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Mikasa'},
            'body': 'The Avengers movie was so cool!!'
        },
        {
            'author': {'nickname': 'Asuna'},
            'body': 'I love animation!!!'
        }
    ]
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)
