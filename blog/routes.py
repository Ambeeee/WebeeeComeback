from flask import render_template, request, flash
from blog import app


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/password", methods = ["POST", "GET"])
def password():
    attempt = str(request.form["pw_input"])
    if attempt == "6414":
        flash("Welcome, sir.")
    else:
        flash("Hai sbagliato mammoccio")
    return render_template("home.html")
