from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "arav_secret_key"

# Create database
def init_db():
    conn = sqlite3.connect("jee.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                physics INTEGER,
                chemistry INTEGER,
                maths INTEGER)""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("jee.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session["user"] = username
        return redirect("/")
    else:
        return "Invalid Login"

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("jee.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/save_marks", methods=["POST"])
def save_marks():
    if "user" not in session:
        return redirect("/")

    p = request.form["physics"]
    c = request.form["chemistry"]
    m = request.form["maths"]

    conn = sqlite3.connect("jee.db")
    c1 = conn.cursor()
    c1.execute("INSERT INTO marks (username,physics,chemistry,maths) VALUES (?,?,?,?)",
               (session["user"], p, c, m))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)