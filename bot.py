from game import Game
import telebot
from telebot import types
import sqlite3

TOKEN = '5461356135:AAGR6NZs0TX7HM7t_1wdEq6b8vXPmnP3dAs'
bot = telebot.TeleBot(TOKEN)

registered_users = []  # легаси
enter_nick = dict()  # легаси

# Кнопочки главного меню
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             row_width=2,
                                             one_time_keyboard=True)
my_account = types.KeyboardButton("Мой аккаунт")
go_game = types.KeyboardButton("Новая игра")
rules = types.KeyboardButton("Правила")
main_menu_markup.add(my_account)
main_menu_markup.add(go_game)
main_menu_markup.add(rules)

# Кнопочки меню статистики
account_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=2,
                                           one_time_keyboard=True)
go_main = types.KeyboardButton("Главное меню")
get_money = types.KeyboardButton("Получить бабки")
account_markup.add(go_main)
account_markup.add(get_money)

# Кнопочки ставок
bet_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       row_width=2,
                                       one_time_keyboard=True)
st_150 = types.KeyboardButton("150💲")
st_300 = types.KeyboardButton("300💲")
st_500 = types.KeyboardButton("500💲")
st_1000 = types.KeyboardButton("1000💲")
go_main = types.KeyboardButton("Главное меню")
bet_markup.add(st_150)
bet_markup.add(st_300)
bet_markup.add(st_500)
bet_markup.add(st_1000)
bet_markup.add(go_main)

# кнопки для ходящего игрока
heat = types.KeyboardButton("Взять")
stay = types.KeyboardButton("Пас")
give_up = types.KeyboardButton("Сдаться")
first_player_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
first_player_markup.add(heat)
first_player_markup.add(stay)
first_player_markup.add(give_up)

# кнопки для ходящего игрока
give_up = types.KeyboardButton("Сдаться")
second_player_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
second_player_markup.add(give_up)

cancel_searching = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             row_width=2,
                                             one_time_keyboard=True)
canc = types.KeyboardButton("Отменить поиск")
cancel_searching.add(canc)

is_searching = dict()
searching_users_id = {150: [], 300: [], 500: [], 1000: []}
games = dict()
game_id_counter = 1


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
    cur.execute(
        f"select nickname from users where telegram_uid = {message.chat.id}")
    try:
        nn = cur.fetchone()[0]
    except:
        nn = ''
    if nn != '':
        bot.send_message(
            message.chat.id,
            'Привет-привет! Ты уже зареган). Выбери то, что тебе надо',
            reply_markup=main_menu_markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=2,
                                           one_time_keyboard=True)
        first_message = 'Привет, ' + message.from_user.username + '!👋🏼' + 2 * '\n' + 'Перед тем как начать, пожалуйста, зарегистрируйся. Это быстро📝'
        bot.send_message(message.chat.id, first_message)
        question = 'Придумай свой игровой никнейм'
        bot.send_message(message.chat.id, question)
        cur.execute(
            f"update users set chat_state = 0 where telegram_uid = {message.chat.id}"
        )
        db.commit()
    db.close()


@bot.message_handler(content_types=['text'])
def message_reply(message):
    global game_id_counter
    db = connect_db()
    cur = db.cursor()

    cur.execute(
        f"select nickname from users where telegram_uid = {message.chat.id}")

    try:
        nn = cur.fetchone()[0]
    except:
        nn = ''

    cur.execute(
        f"select chat_state from users where telegram_uid = {message.chat.id}")

    try:
        state = cur.fetchone()[0]
    except:
        state = -1

    cur.execute(f"select game_id from users where telegram_uid = {message.chat.id}")

    try:
        player_game_id = cur.fetchone()[0]
    except:
        player_game_id = 0

    def game_finder(bet):
        global game_id_counter
        cur.execute(
            f"select balance from users where telegram_uid = {message.chat.id}")
        balance = cur.fetchone()[0]
        if balance < bet:
            bot.send_message(message.chat.id,
                             'Не хватает монет',
                             reply_markup=bet_markup)
            return 1
        else:
            searching_users_id[bet].append(message.chat.id)
            is_searching[message.chat.id] = bet
            bot.send_message(message.chat.id,
                             'Поиск игры',
                             reply_markup=cancel_searching)
        if len(searching_users_id[bet]) >= 2:
            id_1 = searching_users_id[bet].pop()
            id_2 = searching_users_id[bet].pop()
            g = Game(id_1, id_2, bet)
            cur.execute(
                f"update users set game_id = {game_id_counter} where telegram_uid = {id_1}"
            )
            cur.execute(
                f"update users set game_id = {game_id_counter} where telegram_uid = {id_2}"
            )
            db.commit()
            cur.execute(f"select nickname from users where telegram_uid={id_1}")
            nn_1 = cur.fetchone()[0]
            cur.execute(f"select nickname from users where telegram_uid={id_2}")
            nn_2 = cur.fetchone()[0]
            bot.send_message(id_1, f'Игра найдена. Ваш противник: {nn_2}')
            bot.send_message(id_1, f'Ваш ход', reply_markup=first_player_markup)
            bot.send_message(id_2, f'Игра найдена. Ваш противник: {nn_1}')
            bot.send_message(id_2, f'Ход противника', reply_markup=second_player_markup)
            games[game_id_counter] = g
            game_id_counter += 1

    if nn == '' and state == -1:
        go_start = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             row_width=2,
                                             one_time_keyboard=True)
        start = types.KeyboardButton("/start")
        go_start.add(start)
        cur.execute(
            f"select count(*) from users where telegram_uid = {message.chat.id}")
        num = cur.fetchone()[0]
        if num < 1:
            cur.execute(
                "insert into users (telegram_uid, nickname, balance, chat_state, game_id) values (?, ?, ?, ?, ?)",
                (f'{message.chat.id}', f'', 0, -1, 0))
            db.commit()
        bot.send_message(
            message.chat.id,
            'Привет! Чтобы начать пользоваться ботом, введи команду /start',
            reply_markup=go_start)

    elif state == 0:
        nn = message.text
        enter_nick[message.chat.id] = 1  # легаси
        registered_users.append(message.chat.id)  # легаси
        # добавляем игрока в бд
        cur.execute(
            f"update users set nickname = '{nn}' where telegram_uid = {message.chat.id}"
        )
        cur.execute(
            f"update users set chat_state = 1 where telegram_uid = {message.chat.id}"
        )
        db.commit()
        bot.send_message(message.chat.id,
                         'Поздравляю, ты зарегистрировался! Ты в главном меню',
                         reply_markup=main_menu_markup)

    elif (player_game_id != 0):
        game = games[player_game_id]
        if message.text == 'Сдаться':
            loser = message.chat.id
            if loser == game.user_1:
                winner = game.user_2
            else:
                winner = game.user_1
            bot.send_message(loser, f'Вы проиграли. Со счёта списано {game.bet} монет', reply_markup=main_menu_markup)
            # cur.execute(f"select balance from users where telegram_uid = {loser}")
            cur.execute(f"update users set balance = balance - {game.bet} where telegram_uid = {loser}")
            bot.send_message(winner, f'Противник сдался. Вы победили! На счет начислено {game.bet} монет', reply_markup=main_menu_markup)
            cur.execute(f"update users set balance = balance + {game.bet} where telegram_uid = {winner}")
            cur.execute(f"update users set game_id = 0 where telegram_uid = {winner}")
            cur.execute(f"update users set game_id = 0 where telegram_uid = {loser}")
            db.commit()


    elif message.text == 'Мой аккаунт':
        stat = account_stat(message.chat.id, cur)  # от юзера
        bot.send_message(message.chat.id, stat, reply_markup=account_markup)

    elif message.text == 'Главное меню':
        bot.send_message(message.chat.id,
                         'Перехожу в главное меню',
                         reply_markup=main_menu_markup)

    elif message.text == 'Получить бабки':
        cur.execute(
            f"select balance from users where telegram_uid = {message.chat.id}")
        bal = cur.fetchone()[0]
        if bal < 150:  # Баланс игрока не превышает какой-то суммы
            cur.execute(
                f"update users set balance = balance + 300 where telegram_uid = {message.chat.id}"
            )
            db.commit()
            bot.send_message(message.chat.id,
                             'Твой баланс пополнен на 300 коинов',
                             reply_markup=account_markup)
        else:
            bot.send_message(
                message.chat.id,
                'Упс... Твой баланс не может быть пополнен, так как он выше 150 монет ☹️',
                reply_markup=account_markup)

    elif message.text == 'Правила':
        bot.send_message(message.chat.id, rules, reply_markup=main_menu_markup)

    elif message.text == 'Новая игра':
        is_searching[message.chat.id] = 1
        bot.send_message(message.chat.id, 'Выбери ставку', reply_markup=bet_markup)

    elif message.text == '150💲' and is_searching.get(message.chat.id,
                                                     False) == 1:
        game_finder(150)

    elif message.text == '300💲' and is_searching.get(message.chat.id,
                                                     False) == 1:
        game_finder(300)

    elif message.text == '500💲' and is_searching.get(message.chat.id,
                                                     False) == 1:
        game_finder(500)

    elif message.text == '1000💲' and is_searching.get(message.chat.id,
                                                      False) == 1:
        game_finder(1000)

    elif message.text == 'Отменить поиск':
        if is_searching.get(message.chat.id, False):
            bet = is_searching[message.chat.id]
            searching_users_id[bet].remove(message.chat.id)
            is_searching[message.chat.id] = -1
            bot.send_message(message.chat.id,
                             'Поиск отменен',
                             reply_markup=main_menu_markup)
        else:
            bot.send_message(message.chat.id,
                             'Вы не в поиске',
                             reply_markup=main_menu_markup)
    else:
        bot.send_message(
            message.chat.id,
            'Упс, такая команда не найдена. Если хочешь поиграть, тапни по кнопочке "Новая игра"',
            reply_markup=main_menu_markup)

    db.close()


if __name__ == '__main__':
    db = connect_db()
    cur = db.cursor()
    cur.execute("update users set game_id = 0")
    db.commit()
    db.close()
    bot.polling(none_stop=True, interval=0)
