from flask import Flask, request, redirect, session, render_template
app = Flask(__name__)
import gunicorn

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
        sql = "SELECT host, description, day, time, status FROM events"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return render_template("/home.html", user = session["username"])
        else:
            return render_template("/home.html", user = session["username"], list=results)
    else:
        return render_template("index.html")

#
# ACCOUNT METHODS/ROUTES
#

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = "SELECT username FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)
        result = cursor.fetchall()
        if len(result) == 1:
            session["username"] = username
            return render_template("home.html", user = session["username"])
        else:
            return render_template("index.html", message = "Wrong username or password.")
    else:
        return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm-password")
        sql = "SELECT username FROM users WHERE username = %s"
        value = (username,)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        if len(result) > 0:
            return render_template("signup.html", message = "Username is already in use")
        elif password == confirmPassword:
            sql = "INSERT INTO users(username, password) VALUES(%s, %s)"
            values = (username, password)
            cursor.execute(sql, values)
            db.commit()
            session["username"] = username
            return redirect("/")
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#
# CALENDAR METHODS/ROUTES
#

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        description = request.form.get("description")
        day = request.form.get("day")
        time = request.form.get("time")
        sql = "INSERT INTO events(host, description, day, time, status) VALUES(%s, %s, %s, %s, 'Scheduled')"
        values = (session["username"], description, day, time)
        cursor.execute(sql, values)
        db.commit()
        return redirect("/myevents")

    else:
        return render_template("add.html", user = session["username"])

@app.route("/myevents")
def myEvents():
    sql = "SELECT host, description, day, time, status FROM events WHERE host = %s"
    values = (session["username"],)
    cursor.execute(sql, values)
    result = cursor.fetchall()
    if len(result) == 0:
        return render_template("myevents.html", user = session["username"])
    else:
        return render_template("myevents.html", list = result, user = session["username"])

@app.route("/cancel/<int: id>")
def editEvent(id):
    sql = "UPDATE events SET status = 'Cancelled' WHERE id = %s"
    values = (id,)
    cursor.execute(sql, values)

@app.route("/update/<int:id>")
def updateEvent(methods = ["GET", "POST"]):
    if request.method == "POST":
        pass
    else:
        pass

if __name__ == '__main__':
    #import os
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    #app.run(HOST, PORT)
    app.run()