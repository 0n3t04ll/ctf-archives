# imports
from flask import Flask, render_template, session, request, redirect, make_response
import secrets
import sqlite3
import re

# filter out XSS!
# blocks the most common event handlers and exfiltration primitives
_BLOCKED = [
    "script", "fetch", "xmlhttprequest",
    "onload", "onerror", "ontoggle", "onmouseover", "onmouseenter",
    "onmouseleave", "onmouseout", "onmousedown", "onmouseup", "ondblclick",
    "onclick", "onscroll", "onwheel", "onresize", "onkeydown", "onkeyup",
    "onkeypress", "onsubmit", "onchange", "oninput", "onblur",
    "oncontextmenu", "onpointerover", "onpointerdown", "onpointerup",
    "onpageshow", "onpagehide", "onhashchange", "onanimation", "ontransition",
]

def filter_str(s):
    for keyword in _BLOCKED:
        if re.search(keyword, s, re.IGNORECASE):
            return True
    return False


# initialize database
conn = sqlite3.connect('local.db')
print("Opened database successfully")

conn.execute('CREATE TABLE if not exists posts (postID TEXT, session TEXT, content TEXT, comments TEXT)')
print("Posts table created successfully")

conn.close()


# initialize flask
app = Flask(__name__)
app.secret_key = open("secret_key.txt", "r").read()
app.config["SESSION_COOKIE_HTTPONLY"] = False


# home page
@app.route('/', methods=['GET'])
def home():

    # if you're a new tester, we'll make you a brand new id!
    if 'id' not in session:
        session['id'] = secrets.token_hex(32)

    # get all posts
    posts = []
    con = sqlite3.connect("local.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute(f"SELECT * FROM posts WHERE session = '{session['id']}'")
    rows = cur.fetchall()

    for row in rows:
        posts.append({
            'id': row['postID'],
            'content': row['content'],
            'comments': row['comments'].split("|")
        })

    # actual HTML for index.html
    index = """
<!DOCTYPE html>

<head>
    <title>FaceTagramTokBook but the second one where it's way harder</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <div class="container">
        <div id="header">
            <h1>🔒 FaceTagramTokBook but the second one where it's way harder</h1>
            <p class="tagline">The most secure social network ever built</p>
        </div>

        <div id="links">
            <a href="/new" class="btn">✍️ Write a new post</a>
            <a href="https://www.youtube.com/watch?v=HUnqE_Tnkhg" class="btn btn-secondary">View your friends!</a>
        </div>

        <div id="title"><h2>View all your posts</h2></div>"""

    for post in posts:
        index += """
        <div class="post-container">
            <div class="post">"""+post["content"]+"""</div>
            <div class="small">Post ID: <a href="/getpost?id="""+post["id"]+"""" class="post-link">"""+post["id"]+"""</a></div>
            <div id="comments">
                <div class="comments-header">💬 Comments</div>"""

        for comment in post["comments"]:
            index += """<div class="comment">"""+comment+"""</div>"""

        index += """
                <div class="comment add-comment-box">
                    <form action="/addComment" method="post">
                        <h3>Add a comment for the world:</h3>
                        <input name="comment" type="text" placeholder="Share your thoughts..." class="comment-input">
                        <input name="postID" type="hidden" value=\""""+post['id']+"""\">
                        <input type="submit" value="Post Comment" class="btn btn-comment">
                    </form>
                </div>
            </div>
        </div>"""
    index += """
    </div>
</body>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

#header {
    background: white;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

#header h1 {
    color: #667eea;
    font-size: 2.5em;
    margin-bottom: 10px;
}

.tagline {
    color: #666;
    font-style: italic;
}

#title, #links {
    text-align: center;
    width: 100%;
    margin: 20px 0;
}

#title h2 {
    color: white;
    font-size: 1.8em;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.btn {
    display: inline-block;
    padding: 12px 24px;
    margin: 0 10px;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 25px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.btn-secondary {
    background: #764ba2;
    color: white;
}

.btn-comment {
    padding: 8px 16px;
    margin-top: 10px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
}

.btn-comment:hover {
    background: #5568d3;
    transform: translateY(-1px);
}

.post-container {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.post {
    width: 100%;
    border-left: 4px solid #667eea;
    padding: 15px;
    background: #f8f9ff;
    border-radius: 8px;
    font-size: 1.1em;
    line-height: 1.6;
}

.small {
    font-size: 0.85em;
    color: #888;
    margin: 15px 0;
    padding-left: 15px;
}

.post-link {
    color: #667eea;
    text-decoration: none;
    font-family: monospace;
    font-weight: bold;
}

.post-link:hover {
    text-decoration: underline;
}

.comments-header {
    font-weight: bold;
    color: #667eea;
    margin: 20px 0 10px 0;
    font-size: 1.1em;
}

#comments {
    margin-left: 20px;
    margin-top: 15px;
}

.comment {
    width: calc(100% - 20px);
    border-left: 3px solid #ddd;
    background: #fafafa;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.comment:hover {
    border-left-color: #667eea;
    background: #f0f0ff;
}

.add-comment-box {
    background: white;
    border: 2px dashed #667eea;
    border-left: 2px dashed #667eea;
    margin-top: 15px;
}

.add-comment-box:hover {
    background: white;
    border-color: #5568d3;
}

h3 {
    margin: 0 0 10px 0;
    color: #667eea;
    font-size: 1em;
}

.comment-input {
    width: 100%;
    padding: 10px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1em;
    transition: border-color 0.3s ease;
    font-family: inherit;
}

.comment-input:focus {
    outline: none;
    border-color: #667eea;
}
</style>"""
    resp = make_response(index)
    resp.headers['Content-Security-Policy'] = "script-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; object-src 'none'"
    return resp


# form to add a new post
@app.route('/new', methods=['GET'])
def new():
    return render_template("new.html")


@app.route('/getpost', methods=['GET'])
def getpost():
    # get variables
    postid = request.args["id"]

    # make sure it's hex
    VALID_CHARS = "0123456789abcdef"
    for letter in postid:
        if letter not in VALID_CHARS:
            return redirect('error')

    # try to get post
    con = sqlite3.connect("local.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute(f"SELECT * FROM posts WHERE postID = '{postid}' LIMIT 1")
    rows = cur.fetchall()

    # make sure post exists
    if len(rows) == 0:
        return redirect('/error')

    for row in rows:
        content = row['content']
        comments = row['comments'].split("|")

    content = """
<!DOCTYPE html>

<head>
    <title>FaceTagramTokBook but the second one where it's way harder</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <div class="container">
        <div id="header">
            <h1>🔒 FaceTagramTokBook but the second one where it's way harder/h1>
            <p class="tagline">The most secure social network ever built</p>
        </div>

        <div id="links">
            <a href="/" class="btn">🏠 Back to home</a>
        </div>

        <div id="title"><h2>Post Details</h2></div>
        <div class="post-container">
            <div class="post">"""+content+"""</div>
            <div class="small">Post ID: """+str(postid)+"""</div>
            <div id="comments">
                <div class="comments-header">💬 Comments</div>"""

    for comment in comments:
        content += """<div class="comment">"""+comment+"""</div>"""

    content += """
            </div>
        </div>
    </div>
</body>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

#header {
    background: white;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

#header h1 {
    color: #667eea;
    font-size: 2.5em;
    margin-bottom: 10px;
}

.tagline {
    color: #666;
    font-style: italic;
}

#title, #links {
    text-align: center;
    width: 100%;
    margin: 20px 0;
}

#title h2 {
    color: white;
    font-size: 1.8em;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.btn {
    display: inline-block;
    padding: 12px 24px;
    margin: 0 10px;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 25px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.post-container {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.post {
    width: 100%;
    border-left: 4px solid #667eea;
    padding: 15px;
    background: #f8f9ff;
    border-radius: 8px;
    font-size: 1.1em;
    line-height: 1.6;
}

.small {
    font-size: 0.85em;
    color: #888;
    margin: 15px 0;
    padding-left: 15px;
    font-family: monospace;
}

.comments-header {
    font-weight: bold;
    color: #667eea;
    margin: 20px 0 10px 0;
    font-size: 1.1em;
}

#comments {
    margin-left: 20px;
    margin-top: 15px;
}

.comment {
    width: calc(100% - 20px);
    border-left: 3px solid #ddd;
    background: #fafafa;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.comment:hover {
    border-left-color: #667eea;
    background: #f0f0ff;
}

h3 {
    margin: 0;
}
</style>"""

    resp = make_response(content)
    resp.headers['Content-Security-Policy'] = "script-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; object-src 'none'"
    return resp


# actually adds a new post
@app.route('/add', methods=['POST'])
def add():
    # get variables
    content = request.form['content']

    if filter_str(content):
        return redirect('error')

    if ("'" in content):
        return redirect('error')

    # add new post
    with sqlite3.connect("local.db") as con:
        cur = con.cursor()
        id = secrets.token_hex(24)
        cur.execute(f"INSERT INTO posts (postID, session, content, comments) VALUES ('{id}', '{session['id']}', '{content}', 'Test comment!')")
        con.commit()

    return redirect('/')


# adds a comment to a post
@app.route('/addComment', methods=['POST'])
def addComment():
    # get variables
    comment = request.form['comment']
    id = request.form['postID']

    if filter_str(comment):
        return redirect('error')

    if ("'" in comment) or ('|' in comment):
        return redirect('error')

    # add comment
    con = sqlite3.connect("local.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute(f"SELECT comments FROM posts WHERE postID = '{id}'")
    rows = cur.fetchall()

    # make sure post exists!
    if len(rows) == 0:
        return redirect('/error')

    finalComment = ""
    for row in rows:
        finalComment = row['comments']+"|"+comment

    cur.execute(f"UPDATE posts SET comments = '{finalComment}' WHERE postID = '{id}'")
    con.commit()

    return redirect('/')


# generic error form
@app.route('/error', methods=['GET'])
def error():
    return render_template("error.html")


# start application
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, threaded=True)