import random
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://vyzeivwoctbgzy:c934b12faf2c3fe92c0e117e96b20aed1679e2b8406bc256d9043bbb1e447e76@ec2-3-222-30-53.compute-1.amazonaws.com:5432/dbvaqseneb84gm")
db = scoped_session(sessionmaker(bind=engine))


users_list = []
usernames = ["reader" + str(i) for i in range(50)]
names = ["", "Reader", "Read Reader", "Read Red Reader"]
ages = [i for i in range(10, 99)]
genders = ["male", "female", ""]

for username in usernames:
    password = "1111"
    name = random.choice(names)
    age = random.choice(ages)
    gender = random.choice(genders)
    # print(username, password, name, age, gender)
    db.execute(f"INSERT INTO users (username, password, name, age, gender) "
               f"VALUES ('{username}', '{password}', '{name}', '{age}', '{gender}')")

db.commit()

