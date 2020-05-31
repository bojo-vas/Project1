from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://vyzeivwoctbgzy:c934b12faf2c3fe92c0e117e96b20aed1679e2b8406bc256d9043bbb1e447e76@ec2-3-222-30-53.compute-1.amazonaws.com:5432/dbvaqseneb84gm")
db = scoped_session(sessionmaker(bind=engine))

db.execute("ALTER TABLE books ADD av_score AS "
           "CASE WHEN revs = 0 THEN 0 "
           "ELSE (total / revs) "
           "END")
db.commit()

# db.execute(f"UPDATE books SET revs = 0, total = 0")
# db.commit()

# all_revs = db.execute("SELECT isbn, score FROM reviews ORDER BY isbn").fetchall()
# print("Started...")
# counter = 0
# for rev in all_revs:
#     isbn, score = rev
#     # print(f"isbn: {isbn}, score={score}")
#
#     db.execute(f"UPDATE books SET revs = revs + 1, total = total + {score} WHERE isbn = '{isbn}'")
#     db.commit()
#     counter += 1
#     print(f"{counter} done...")
print("All done!")

# # db.execute("ALTER TABLE users ADD FOREIGN KEY (id) REFERENCES reviews(user_id)")
