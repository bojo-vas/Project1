import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://vyzeivwoctbgzy:c934b12faf2c3fe92c0e117e96b20aed1679e2b8406bc256d9043bbb1e447e76@ec2-3-222-30-53.compute-1.amazonaws.com:5432/dbvaqseneb84gm")
db = scoped_session(sessionmaker(bind=engine))


def main():
    with open("books.csv", "r") as file:
        lines = csv.reader(file, quoting=csv.QUOTE_NONE)
        for line in lines:
            if line[0]== 'isbn':
                continue
            
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
