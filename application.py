import datetime

import os

from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
from pip._vendor import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_folder = 'static'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")  # best rated, most rated, last rated
def home():
    if "is_logged" not in session:
        session["is_logged"] = False
    title = "BestBooks.com"
    headline = "HOME"

    last_revs = db.execute("SELECT users.username, users.name, users.age, "
                           "books.isbn, books.author, books.title, "
                           "reviews.score, reviews.comment "
                           "FROM reviews INNER JOIN users ON reviews.user_id=users.id "
                           "INNER JOIN books ON reviews.isbn=books.isbn "
                         "ORDER BY reviews.id DESC LIMIT 3").fetchall()

    most_rated = db.execute("SELECT isbn, author, title, revs, total "
                            "FROM books ORDER BY revs DESC LIMIT 3").fetchall()

    return render_template("index.html", title=title, headline=headline, 
    logged=session["is_logged"], last_revs=last_revs, most_rated=most_rated)


@app.route("/profile")  # username, password change, name, picture?!, reviewed books, highest, lowest, user-rating
def profile():
    title = "User Profile"
    headline = "User Profile"

    last_revs = db.execute(f"SELECT books.isbn, books.author, books.title, reviews.score, reviews.comment FROM reviews INNER JOIN books ON reviews.isbn=books.isbn WHERE reviews.user_id={session['user_id']} ORDER BY reviews.id DESC LIMIT 10 ").fetchall()
    
    return render_template("index.html", title=title, headline=headline, logged=session["is_logged"], last_revs=last_revs)


@app.route("/log", methods=["GET", "POST"])
def log():
    if session["is_logged"]:
        if request.method == "POST" and request.form.get("logout"):
            session["is_logged"] = False
            return redirect(url_for('home'))
            # return render_template("login.html", title="Log In", logged=session["is_logged"])
        return render_template("logout.html", title="Logging Out...", username=session["username"], logged=session["is_logged"])
    else:
        return render_template("login.html", title="Log In", logged=session["is_logged"])


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    err_msg = ''

    if request.method == "POST" and request.form.get("login"):
        username = request.form.get("username")
        password = request.form.get("password")
        if len(username) < 4 or len(password) < 4:
            return render_template("login.html", title="Log In", problem="Username and password should be 4 signs or more")
        # db check
        user = db.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchone()

        if not user:
            err_msg = f"No user with username '{username}'"
            return render_template("login.html", title="Log In", problem=err_msg)
        else:
            pw = user.password
            if pw != password:
                err_msg = "Wrong password"
                return render_template("login.html", title="Log In", problem=err_msg)
            else:
                session["username"] = username
                session["user_id"] = user.id
                session["user_name"] = user.name
                session["is_logged"] = True
        return redirect(url_for('home'))
        # return render_template("index.html", title="BestBooks.com", headline=f"Hello {username}!", logged=session["is_logged"])
    return render_template("login.html", title="Log In", logged=session["is_logged"])


@app.route("/register", methods=["GET", "POST"])
def register():
    us_err = ''
    pass_err = ''

    if request.method == "POST" and request.form.get("registered"):
        username = request.form.get("username")
        password_1 = request.form.get("password_1")
        password_2 = request.form.get("password_2")
        name = request.form.get("name")
        name = name if name else None
        age = request.form.get("age")
        age = age if age else None
        gender = request.form.get("gender")

        if len(username) < 4:
            us_err = "Should be 4 letters or more"
        elif not username.isalnum():
            us_err = "Username should consist only letters and digits"
        else:
            user = db.execute(f"SELECT username FROM users WHERE username = '{username}'").fetchall()
            if user:
                us_err = f"User with username '{username}' already exist"

        if len(password_1) < 4:
            pass_err = "Should be 4 signs or more. "
        if password_1 != password_2:
            pass_err += "Passwords should be identical"
        if not password_1.isalnum():
            us_err = "Password should consist only letters and digits"

        if pass_err or us_err:
            return render_template("register.html", title="Register", username_problem=us_err, password_problem=pass_err)
        else:
            # password =
            # submit to db
            db.execute("INSERT INTO users (username, password, name, age, gender) VALUES (:username, :password, :name, :age, :gender)",
                       {"username": username, "password": password_1, "name": name, "age": age, "gender": gender})

            db.commit()
            return render_template("login.html", title="Login")
    return render_template("register.html", title="Register", username_problem=us_err,
                           password_problem=pass_err)


@app.route("/search", methods=["GET", "POST"])  # ISBN number of a book, the title of a book, or the author
def search():
    if session["is_logged"]:
        results = []

        if request.method == "POST" and request.form.get("searched"):
            searched_data = request.form.get("searched")
            # all_searched_words = str(searched_data).lower().split()
            word = str(searched_data).lower()
            # for word in all_searched_words:
            results.extend(db.execute(
                f"SELECT * FROM books WHERE LOWER(isbn) LIKE '%{word}%' OR LOWER(author) LIKE '%{word}%' "
                f"OR LOWER(title) LIKE '%{word}%' ORDER BY author LIMIT 100").fetchall())
            return render_template("input.html", logged=session["is_logged"], results=results, first=False)
        return render_template("input.html", logged=session["is_logged"], results=results, first=True)
    return render_template("error.html", message="Unavailable", info="Please log in to use all functionality available")


# details about the book: title, author, publication year, ISBN number, and any reviews + Goodreads Review Data
@app.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn: str):
    isbn = isbn
    curr_book = db.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()
    session['book_isbn'] = isbn
    session['now_book'] = curr_book
    
    if session["is_logged"]:
        gave_review = db.execute(f"SELECT * FROM reviews WHERE isbn = '{isbn}' AND user_id = '{session['user_id']}'").fetchone()
        session['gave_review'] = gave_review

        reviews = db.execute(f"SELECT username, name, gender, age, score, comment FROM users JOIN reviews ON reviews.user_id=users.id "
                         f"WHERE isbn = '{isbn}' AND user_id != '{session['user_id']}' ORDER BY reviews.id DESC").fetchall()

        session['reviews'] = reviews
    #GOODREADS info
        result = requests.get("https://www.goodreads.com/book/review_counts.json",
                             params={"key": "OkeAxEncKe0vfY0MlZsiw", "isbns": f"{isbn}"})
        book_info = result.json()

        session["rating"] = book_info["books"][0]["average_rating"]
        session["count"] = book_info["books"][0]["ratings_count"]

        return render_template("book.html", logged=session["is_logged"], book=session['now_book'], gave_review=gave_review,
                           reviews=reviews, rating=session["rating"], count=session["count"], headline = isbn)

    return render_template("book.html", logged=session["is_logged"], book=session['now_book'], message="Unavailable", headline = isbn)


@app.route("/rate", methods=["GET", "POST"])  # only one customer review per book
def rate():
    if request.method == "POST" and request.form.get("score"):
        score = request.form.get("score")
        comment = request.form.get("comment")
        print(comment)
        if not comment:
            comment = None

        gave_review = db.execute(
            f"SELECT * FROM reviews WHERE isbn = '{session['book_isbn']}' AND user_id = '{session['user_id']}'").fetchone()
        session['gave_review'] = gave_review
        # submit to db
        if not gave_review:
            db.execute(
                "INSERT INTO reviews (isbn, user_id, comment, score) VALUES (:isbn, :user_id, :comment, :score)",
                {"isbn": session['book_isbn'], "user_id": session['user_id'], "comment": comment, "score": score})
            db.commit()

            session['gave_review'] = db.execute(
                f"SELECT * FROM reviews WHERE isbn = '{session['book_isbn']}' "
                f"AND user_id = '{session['user_id']}'").fetchone()

    return render_template("book.html", logged=session["is_logged"], book=session['now_book'], gave_review=session['gave_review'],
                           reviews=session['reviews'], rating=session["rating"], count=session["count"])


@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    app.config['JSON_SORT_KEYS'] = False

    book = db.execute(f"SELECT * FROM books WHERE isbn='{isbn}'").fetchone()
    if book:
        result = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "OkeAxEncKe0vfY0MlZsiw?!", "isbns": f"{isbn}"})
        book_info = result.json()

        book_data = {
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": isbn,
            "review_count": book_info["books"][0]["ratings_count"],
            "average_score": book_info["books"][0]["average_rating"]
        }

        return book_data
    return render_template("error.html", message="Error 404", info="No such book ISBN in database. Please try again.")
