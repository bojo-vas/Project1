from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import time


engine = create_engine("postgres://usikokxwpbezaa:248c35887b5c3a4ad629c674948883391e225622a81d0f8b2a6588dd1b714068@ec2-52-72-65-76.compute-1.amazonaws.com:5432/dfe3fqnavc11kn")
db = scoped_session(sessionmaker(bind=engine))

print("Started...")
start = time.time()

# change all passwords :)
db.execute(f"UPDATE users SET password = '53.53.53.53'")
db.commit()

# db.execute("ALTER TABLE books ADD av_score AS "
#            "CASE WHEN revs = 0 THEN 0 "
#            "ELSE (total / revs) "
#            "END")
# db.commit()

# total and revs = 0

# db.execute(f"UPDATE books SET revs = 0, total = 0")
# db.commit()

# Count total and revs per book isbn

# all_revs = db.execute("SELECT isbn, score FROM reviews ORDER BY isbn").fetchall()
#
# counter = 0
# for rev in all_revs:
#     isbn, score = rev
#     # print(f"isbn: {isbn}, score={score}")
#
#     db.execute(f"UPDATE books SET revs = revs + 1, total = total + {score} WHERE isbn = '{isbn}'")
#     db.commit()
#     counter += 1
#     print(f"{counter} done...")


# Delete duplicates?!

# last_isbn, last_user_id = 0, 0
# reviewed = db.execute("SELECT id, isbn, user_id FROM reviews ORDER BY isbn").fetchall()
# for line in reviewed:
#     iid, isbn, user_id = line
#     if isbn == last_isbn and user_id == last_user_id:
#         db.execute(f"DELETE FROM reviews WHERE id = {iid}")
#         db.commit()
#         print(f"Deleted {isbn} review ID - {iid} from user_ID {user_id}")
#     else:
#         last_isbn = isbn
#         last_user_id = user_id
#
finish = time.time()
delta = finish - start
print("All done!")
print(f"In Seconds = {delta}")
print(f"Operation time: {delta // 60} mins and {delta % 60} secs")

# # db.execute("ALTER TABLE users ADD FOREIGN KEY (id) REFERENCES reviews(user_id)")
