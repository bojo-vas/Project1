import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://xqcyougdjusspx:c5adba4086424863117014771ee7d7357ab2724baf7bb92fa52d8ab0b6483708@ec2-54-165-36-134.compute-1.amazonaws.com:5432/d6650t6c77bc8k")
db = scoped_session(sessionmaker(bind=engine))


def main():
    with open("books.csv", "r") as file:
        lines = csv.reader(file, quoting=csv.QUOTE_NONE)
        for line in lines:
            if len(line) == 4:
                isbn, title, author, year = line
                db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                           {"isbn": isbn, "title": title, "author": author, "year": year})
                continue
            in_special = False
            special = ''
            result = []
            for i in line:
                if i.startswith("\"\""):
                    special += i.lstrip("\"\"")
                    in_special = True
                elif i.endswith("\"\""):
                    special += i.rstrip("\"\"")
                    in_special = False
                    result.append(special)
                elif in_special:
                    special += i
                else:
                    result.append(i.strip("\""))
            if len(result) == 4:
                isbn, title, author, year = result
                db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                           {"isbn": isbn, "title": title, "author": author, "year": year})

        db.commit()


if __name__ == '__main__':
    main()
