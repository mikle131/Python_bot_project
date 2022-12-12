import game
import telebot
from telebot import types
import sqlite3


TOKEN = '5461356135:AAGR6NZs0TX7HM7t_1wdEq6b8vXPmnP3dAs'
bot = telebot.TeleBot(TOKEN)

registered_users = []  # легаси
enter_nick = dict()  # легаси

# Кнопочки главного меню
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
my_account = types.KeyboardButton("Мой аккаунт")
go_game = types.KeyboardButton("Новая игра")
rules = types.KeyboardButton("Правила")
main_menu_markup.add(my_account)
main_menu_markup.add(go_game)
main_menu_markup.add(rules)

#Кнопочки меню статистики
account_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
go_main = types.KeyboardButton("Главное меню")
get_money = types.KeyboardButton("Получить бабки")
account_markup.add(go_main)
account_markup.add(get_money)


def account_stat(user, cur):
    cur.execute(f"select nickname from users where telegram_uid = {user}")
    nn = cur.fetchone()[0]
    cur.execute(f"select balance from users where telegram_uid = {user}")
    balance = cur.fetchone()[0]
    message = f"""
Ник: {nn}
Количество игр:
Процент побед:
Баланс: {balance}
    """
    return message

rules = '''Текст-заглушка'''


def connect_db():
    """Соединяет с бд"""
    rv = sqlite3.connect('users.db')
    rv.row_factory = sqlite3.Row
    return rv


@bot.message_handler(commands=['start'])
def hello_message(message):
    db = connect_db()
    cur = db.cursor()
    cur.execute(f"select count(*) from users where telegram_uid = {message.chat.id}")
    num = cur.fetchone()[0]
    if num == 1:
        bot.send_message(message.chat.id, 'Привет-привет! Ты уже зареган). Выбери то, что тебе надо', reply_markup = main_menu_markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        first_message = 'Привет, ' + message.from_user.username + '!👋🏼' + 2 * '\n' + 'Перед тем как начать, пожалуйста, зарегистрируйся. Это быстро📝'
        bot.send_message(message.chat.id, first_message)
        question = 'Придумай свой игровой никнейм'
        bot.send_message(message.chat.id, question)
        cur.execute("insert into users (chat_state) values (-1)")
        db.commit()
    db.close()

@bot.message_handler(content_types=['text'])
def message_reply(message):
    db = connect_db()
    cur = db.cursor()
    cur.execute(f"select chat_state from users where telegram_uid = {message.chat.id}")
    state = cur.fetchone()[0]
    cur.execute(f"select count(*) from users where telegram_uid = {message.chat.id}")
    num = cur.fetchone()[0]
    if num == 0:
        go_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        start = types.KeyboardButton("/start")
        go_start.add(start)
        bot.send_message(message.chat.id, 'Привет! Чтобы начать пользоваться ботом, введи команду /start', reply_markup = go_start)

    elif state == -1:
        nn = message.text
        enter_nick[message.chat.id] = 1  # легаси
        registered_users.append(message.chat.id)
        # добавляем игрока в бд
        cur.execute("insert into users (telegram_uid, nickname, balance, chat_state) values (?, ?, ?, ?)",
                    (f'{message.chat.id}', f'{nn}', '500', 1)
                    )
        db.commit()
        bot.send_message(message.chat.id, 'Поздравляю, ты зарегистрировался! Ты в главном меню', reply_markup = main_menu_markup)

    elif message.text == 'Мой аккаунт':
        stat = account_stat(message.chat.id, cur)  # от юзера

        bot.send_message(message.chat.id, stat, reply_markup = account_markup)

    elif message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Перехожу в главное меню', reply_markup= main_menu_markup)

    elif message.text == 'Получить бабки':
        if True: #Баланс игрока не превышает какой то суммы
            db = connect_db()
            cur = db.cursor()
            cur.execute(f"update users set balance = balance + 300 where telegram_uid = {message.chat.id}")
            db.commit()
            bot.send_message(message.chat.id, 'Твой баланс пополнен на 300 коинов', reply_markup= account_markup)
        else:
            bot.send_message(message.chat.id, 'Упс... Твой баланс не может быть пополнен, так как ', reply_markup= account_markup)

    elif message.text == 'Правила':
        bot.send_message(message.chat.id, rules, reply_markup= main_menu_markup)

    else:
        bot.send_message(message.chat.id, 'Упс, такая команда не найдена. Если хочешь поиграть, тапни по кнопочке "Новая игра"', reply_markup = main_menu_markup)

    db.close()


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)