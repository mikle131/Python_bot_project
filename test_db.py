from bot import connect_db

db = connect_db()
cur = db.cursor()

users = db.execute('select * from users').fetchall()
for user in users:
    print(user['telegram_uid'], user['nickname'], user['balance'], user['chat_state'], user['game_id'])
db.close()
