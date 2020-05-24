# for book page
isbn = 0

result = request.get("https://www.goodreads.com/book/review_counts.json", params={"key": "OkeAxEncKe0vfY0MlZsiw", "isbns": f"{isbn}"})
book_info = result.json()

av_rating = book_info["books"][0]["average_rating"]
rat_count = book_info["books"][0]["ratings_count"]

# api address
# @app.route("/api/<string: isbn>", methods=["GET"])
def api(isbn):
    book = db.execute(f"SELECT * FROM books WHERE isbn='f{isbn}'").fetchone()

    result = request.get("https://www.goodreads.com/book/review_counts.json", params={"key": "OkeAxEncKe0vfY0MlZsiw?!", "isbns": f"{isbn}"})
    book_info = result.json()
    book_data = {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "reviews_count": book_info["books"][0]["ratings_count"],
        "average_score": book_info["books"][0]["average_rating"]
    }

#api on goodreads
# https://www.goodreads.com/book/review_counts.json?isbns=0441172717&key=OkeAxEncKe0vfY0MlZsiw

'''
{"books":
[
{"id":53180949,
"isbn":"0441172717",
"isbn13":"9780441172719",
"ratings_count":73,
"reviews_count":213,
"text_reviews_count":6,
"work_ratings_count":702216,
"work_reviews_count":1243238,
"work_text_reviews_count":20007,
"average_rating":"4.23"},
]
}
'''