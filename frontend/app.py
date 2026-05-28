from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "appuser"),
        password=os.environ.get("DB_PASSWORD", "apppassword123"),
        database=os.environ.get("DB_NAME", "posts_db"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(100),
            mobile      VARCHAR(15),
            address     VARCHAR(255),
            message     VARCHAR(255),
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    cursor.close()
    db.close()

@app.route("/")
def home():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Post Message</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 500px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }
                h2 {
                    color: #333;
                }
                form {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                label {
                    display: block;
                    margin-top: 10px;
                    font-weight: bold;
                    color: #555;
                }
                input, textarea {
                    width: 100%;
                    padding: 8px;
                    margin-top: 5px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                button {
                    margin-top: 15px;
                    padding: 10px 20px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #218838;
                }
                a {
                    display: block;
                    margin-top: 15px;
                    text-align: center;
                    color: #007bff;
                }
            </style>
        </head>
        <body>
            <h2>Submit a Post</h2>
            <form method="POST" action="/post">

                <label>Name</label>
                <input
                    type="text"
                    name="name"
                    placeholder="Enter your name"
                    required
                />

                <label>Mobile Number</label>
                <input
                    type="tel"
                    name="mobile"
                    placeholder="Enter your mobile number"
                    required
                />

                <label>Address</label>
                <textarea
                    name="address"
                    placeholder="Enter your address"
                    rows="3"
                    required
                ></textarea>

                <label>Message</label>
                <input
                    type="text"
                    name="message"
                    placeholder="Enter your message"
                    required
                />

                <button type="submit">Submit</button>
            </form>
            <a href="/posts">View All Posts</a>
        </body>
        </html>
    '''

@app.route("/post", methods=["POST"])
def create_post():
    name    = request.form.get("name")
    mobile  = request.form.get("mobile")
    address = request.form.get("address")
    message = request.form.get("message")

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO posts (name, mobile, address, message)
        VALUES (%s, %s, %s, %s)
    """, (name, mobile, address, message))
    db.commit()
    cursor.close()
    db.close()

    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 500px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                h3 {{
                    color: #28a745;
                }}
                p {{
                    color: #555;
                }}
                a {{
                    display: inline-block;
                    margin-top: 10px;
                    margin-right: 10px;
                    color: #007bff;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h3>✅ Post Saved Successfully!</h3>
                <p><b>Name:</b>    {name}</p>
                <p><b>Mobile:</b>  {mobile}</p>
                <p><b>Address:</b> {address}</p>
                <p><b>Message:</b> {message}</p>
                <a href="/">Submit Another</a>
                <a href="/posts">View All Posts</a>
            </div>
        </body>
        </html>
    '''

@app.route("/posts")
def get_posts():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, mobile, address, message, created_at FROM posts")
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    rows_html = ""
    for row in rows:
        rows_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
            </tr>
        """

    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>All Posts</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 30px;
                    background-color: #f4f4f4;
                }}
                h2 {{
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                th {{
                    background-color: #28a745;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 10px 12px;
                    border-bottom: 1px solid #ddd;
                    color: #555;
                }}
                tr:hover {{
                    background-color: #f9f9f9;
                }}
                a {{
                    display: inline-block;
                    margin-top: 15px;
                    color: #007bff;
                }}
            </style>
        </head>
        <body>
            <h2>All Posts</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Mobile</th>
                        <th>Address</th>
                        <th>Message</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            <a href="/">Submit New Post</a>
        </body>
        </html>
    '''

if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000)
