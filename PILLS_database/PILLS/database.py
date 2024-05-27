import sqlite3

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()
    query = """ CREATE TABLE IF NOT EXISTS pills(id INTEGER, name TEXT, cost INTEGER, link TEXT) """
    query2 = """ CREATE TABLE IF NOT EXISTS adults(id INTEGER, dosage TEXT, doses_per_day INTEGER) """
    query3 = """ CREATE TABLE IF NOT EXISTS kids(id INTEGER, dosage TEXT, doses_per_day INTEGER) """
    query4 = """ CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id VARCHAR, age VARCHAR) """
    cursor.execute(query)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)

    db.commit()

"""insert_kids = [
    (8, '1 таблетка', 1),
    (9, '10 мл', 2),
    (10, '1 капсула на 100 мл молока', 3),
    (11, '5 мл', 4),
    (12, '50 мг', 3)
]

insert_adults = [
    (1, '1 таблетка', 2),
    (2, '1-2 капли', 3),
    (3, '1 капсула', 3),
    (4, '1 таблетка', 1),
    (5, '50 капсула', 1),
    (6, '1 таблетка', 1),
    (7, '1 таблетка', 1)
]"""

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()
    query4 = """ INSERT INTO kids(id, dosage, doses_per_day) 
                    VALUES(?,?,?) """
    query5 = """ INSERT INTO adults(id, dosage, doses_per_day) 
                        VALUES(?,?,?) """
    #cursor.executemany(query4, insert_kids)
    #cursor.executemany(query5, insert_adults)
    db.commit()


