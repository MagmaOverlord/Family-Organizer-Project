from flask import Flask, request, redirect, session, render_template
app = Flask(__name__)

import mysql.connector

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

app.secret_key = "Key Time!"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="greatkid5000",
    database="sys"
)

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(50))")
cursor.execute("CREATE TABLE IF NOT EXISTS events (id INT AUTO_INCREMENT PRIMARY KEY, host VARCHAR(100), description VARCHAR (255), day VARCHAR (50), time VARCHAR(20), status VARCHAR(20))")
db.commit()

@app.route('/')
def index():
    if "username" in session:
        return render_template("welcome.html", username = session["username"], list="")
    else:
        return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = "SELECT username FROM users"
        cursor.execute(sql)
        usernames = cursor.fetchall()
        sql = "SELECT password FROM users"
        cursor.execute(sql)
        passwords = cursor.fetchall()
        i = 0
        for user in usernames:
            if username == user and password == password[i]:
                    session["username"] = username
                    return redirect("/home")
            i+=1
            return render_template("index.html", message = "Wrong username or password.")
    else:
        return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")
        if password == confirmPassword:
            sql = f'INSERT INTO users ("{username}", "{password}")'
            cursor.execute(sql)
            db.commit()
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
