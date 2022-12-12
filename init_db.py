import sqlite3

# exit(1) # защита от случайного запуска (не запускайте, потрёт бд)

connection = sqlite3.connect('users.db')


with open('scheme.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# cur.execute("insert into users (telegram_uid, nickname, balance, chat_state) values (414028769, 'kefir', 500, 1)")

connection.commit()
connection.close()