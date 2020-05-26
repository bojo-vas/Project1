import datetime

import os

from flask import Flask, render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    headline = "HOME"
    return render_template("index.html", headline=headline)


# @app.route("/<name>")
# def hello(name: str):
#
#     return f"<h1>Hello there {name.capitalize()}!!!</h1>"


@app.route("/exit")
def bye():
    headline = "Goodbye"

    return render_template("index.html", headline=headline)


@app.route("/birthday")
def birthday():
    now = datetime.datetime.now()
    is_birthday = now.month == 7 and now.day == 9

    return render_template("birthday.html", is_birthday=is_birthday)


@app.route("/loop")
def loop():
    names = ["Bojo", "Iva", "Pesho", "Gosho", "David"]

    return render_template("loop.html", names=names)


@app.route("/input")
def submit():
    return render_template("input.html")


@app.route("/hello_name", methods=["GET", "POST"])
def hello_name():
    if request.method == "GET":
        return "Please use the form!"
    name = request.form.get("name").capitalize()
    return render_template("error.html", name=name)


@app.route("/notes", methods=["GET", "POST"])
def add_note():
    if not session["notes"]:
        session["notes"] = []
    if request.method == "POST" and request.form.get("note"):
        session["notes"].append(request.form.get("note"))
    elif request.method == "POST" and request.form.get("clear"):
        if session["notes"]:
            session["notes"].pop()
    elif request.method == "POST" and request.form.get("clearall"):
        session["notes"] = []

    return render_template("notes.html", notes=session["notes"])