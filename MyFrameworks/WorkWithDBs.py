import sqlite3


def getBooks(name, authorName):
    con = sqlite3.connect("DBs/Authors_db.sqlite")  # получаем id автора из БД
    cur = con.cursor()
    author = cur.execute(f"""SELECT * FROM Authors
                        WHERE name LIKE '%{authorName}%'""").fetchone()
    con.close()
    if name and authorName:  # подбираем фильтры для вывода книг
        wheres = f"WHERE name LIKE '%{name}%' AND author LIKE '%{author[0]}%'"
    elif name:
        wheres = f"WHERE name LIKE '%{name}%'"
    elif authorName:
        wheres = f"WHERE author LIKE '%{author[0]}%'"
    else:
        wheres = ''
    con = sqlite3.connect("DBs/Books_db.sqlite")  # получаем книги из БД
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM Books
                        {wheres}""").fetchall()
    con.close()
    con = sqlite3.connect("DBs/Authors_db.sqlite")  # получаем id автора из БД
    cur = con.cursor()
    for i in range(len(result)):
        result[i] = list(result[i])
        result[i][2] = cur.execute(f"""SELECT name FROM Authors
                    WHERE id = ?""", (result[i][2],)).fetchone()[0]
    con.close()
    return result

def open_book(btnName):
    con = sqlite3.connect("DBs/Books_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT id, name, textLink FROM Books
                WHERE btnName = '{btnName}'""").fetchone()
    con.close()
    return result