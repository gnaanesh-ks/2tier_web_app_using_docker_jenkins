from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "password"),
        database=os.environ.get("DB_NAME", "posts_db")
    )

@app.route("/")
def home():
    return '''
        <h2>Post Message</h2>
        <form method="POST" action="/post">
            <input type="text" name="message" placeholder="Enter message" />
            <button type="submit">Submit</button>
        </form>
    '''

@app.route("/post", methods=["POST"])
def create_post():
    message = request.form.get("message")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))")
    cursor.execute("INSERT INTO posts (message) VALUES (%s)", (message,))
    db.commit()
    return f"<h3>Saved: {message}</h3><a href='/posts'>View All</a>"

@app.route("/posts")
def get_posts():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    result = "<h2>All Posts</h2><ul>"
    for row in rows:
        result += f"<li>{row[0]}: {row[1]}</li>"
    result += "</ul><a href='/'>Back</a>"
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
