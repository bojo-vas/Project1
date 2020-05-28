from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://xqcyougdjusspx:c5adba4086424863117014771ee7d7357ab2724baf7bb92fa52d8ab0b6483708@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d6650t6c77bc8k")
db = scoped_session(sessionmaker(bind=engine))


def main():
    db.execute("CREATE TABLE books "
               "(id SERIAL, "
               "isbn VARCHAR NOT NULL PRIMARY KEY, "
               "title VARCHAR NOT NULL, "
               "author VARCHAR NOT NULL, "
               "year INTEGER NOT NULL,"
               "revs INTEGER,"
               "total INTEGER)")

    db.execute("CREATE TABLE users ("
               "id SERIAL PRIMARY KEY, "
               "username VARCHAR NOT NULL, "
               "password VARCHAR NOT NULL, "
               "name VARCHAR, age INTEGER, "
               "gender VARCHAR)")

    db.execute("CREATE TABLE reviews ("
               "id SERIAL, "
               "isbn VARCHAR NOT NULL REFERENCES books, "
               "user_id INTEGER NOT NULL REFERENCES users, "
               "comment VARCHAR, "
               "score INTEGER NOT NULL)")

    db.commit()


    # db.execute("ALTER TABLE users ADD FOREIGN KEY (id) REFERENCES reviews(user_id)")
    # db.commit()


if __name__ == '__main__':
    main()