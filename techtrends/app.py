import sqlite3
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
import sys

# Function to get a database connection.
# This function connects to database with the name `database.db`

conn_count = 0
def get_db_connection():
    global conn_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_count += 1

    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    app.logger.info(post)
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info("Non-Existing Article")
        logger.info("404 - Article does not exists")
        logger.addHandler(h1)
        logger.addHandler(h2)
        return render_template('404.html'), 404
        
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("/About Request Succesfully")
    logger.info("About Us")
    logger.addHandler(h1)
    logger.addHandler(h2)
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info("Article Created")
            logger.info(f"Article {title} created")
            logger.addHandler(h1)
            logger.addHandler(h2)
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the /healthz endpoint
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
        response = json.dumps({ "result": "OK - healthy" }),
        status = 200,
        mimetype='application/json'
    )
    return response

# Define the /metrics endpoint
@app.route('/metrics')
def metrics():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    count_posts = c.execute('SELECT COUNT(id) as post_count FROM posts')
    for r in c.fetchall():
        response = app.response_class(
            response = json.dumps({
                "post_count": dict(r),
                "db_connections": conn_count
                }),
            status = 200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111

if __name__ == "__main__":
    logger = logging.getLogger("__name__")
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h2 = logging.StreamHandler(sys.stderr)
    h2.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port='3111', debug=True)
