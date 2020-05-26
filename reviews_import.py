import random
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://vyzeivwoctbgzy:c934b12faf2c3fe92c0e117e96b20aed1679e2b8406bc256d9043bbb1e447e76@ec2-3-222-30-53.compute-1.amazonaws.com:5432/dbvaqseneb84gm")
db = scoped_session(sessionmaker(bind=engine))

raw_isbns = db.execute(f"SELECT isbn FROM books")
isbns = [i[0] for i in raw_isbns]
user_ids = [i for i in range(10, 51)]
comments = ["Great book!", "Best book ever", "Liked alot", "Cant say I liked it", "Too Bad", "Worst book ever",
            "Should have spent my time wiser", "Read it if you like fantasy novels", "The book is fine but not the best",
            "Go read smth else", "Stupid book", "Try to find one better", "Wow", "Alwesome", ""]
scores = [1, 2, 3, 4, 5]

for i in range(4000):
    isbn = random.choice(isbns)
    user_id = random.choice(user_ids)
    comment = random.choice(comments)
    score = random.choice(scores)

    # print(username, password, name, age, gender)
    db.execute(f"INSERT INTO reviews (isbn, user_id, comment, score) "
               f"VALUES ('{isbn}', {user_id}, '{comment}', {score})")

db.commit()

print(isbns)
