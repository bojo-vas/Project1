import csv
counter = 1
file = open("books.csv", "r")
lines = csv.reader(file, quoting=csv.QUOTE_NONE)

for line in lines:
    if len(line) == 4 and line[0]!= 'isbn':
        print(f"{counter} : {line}")
        counter +=1
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
        print(f"{counter} : {result}")
        counter += 1

file.close()