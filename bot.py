import game
import telebot
from telebot import types


TOKEN ='5461356135:AAGR6NZs0TX7HM7t_1wdEq6b8vXPmnP3dAs'
bot = telebot.TeleBot(TOKEN)

registered_users = []
enter_nick = dict()

#Кнопочки главного меню
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


def account_stat(user):
    message = f"""
Ник:
Количество игр:
Процент побед:
Баланс:
    """
    return message

rules = '''Текст-заглушка'''


@bot.message_handler(commands=['start'])
def hello_message(message):
    if message.chat.id in registered_users:
        bot.send_message(message.chat.id, 'Привет-привет! Ты уже зареган). Выбери, что тебе надо', reply_markup = main_menu_markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        first_message = 'Привет, ' + message.from_user.username + '!👋🏼' + 2 * '\n' + 'Перед тем как начать, пожалуйста, зарегестрируйся. Это быстро📝'
        bot.send_message(message.chat.id, first_message )
        question = 'Придуймай свой игровой никнейм'
        bot.send_message(message.chat.id, question)
        enter_nick[message.chat.id] = -1
        registered_users.append(message.chat.id)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.chat.id not in registered_users:
        go_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        start = types.KeyboardButton("/start")
        go_start.add(start)
        bot.send_message(message.chat.id, 'Привет! Чтобы начать пользоваться ботом, введи команду /start', reply_markup = go_start)
    
    elif enter_nick[message.chat.id] == -1:
        nickname = message.text
        enter_nick[message.chat.id] = 1
        registered_users.append(message.chat.id)
        #Вот тут надо добавить игрока в бдшку. 
        bot.send_message(message.chat.id, 'Поздравляю, ты зарегестрировался! Ты в главном меню', reply_markup = main_menu_markup)
    
    elif message.text == 'Мой аккаунт':
        stat = account_stat([])#от юзера
        bot.send_message(message.chat.id, stat, reply_markup = account_markup)
    
    elif message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Перехожу в главное меню', reply_markup= main_menu_markup)
    
    elif message.text == 'Получить бабки':
        if True: #Баланс игрока не превышает какой то суммы
            #users.money += 10000
            bot.send_message(message.chat.id, 'Твой баланс пополнен на 300 коинов', reply_markup= account_markup)
        else:
            bot.send_message(message.chat.id, 'Упс... Твой баланс не может быть пополнен, так как ', reply_markup= account_markup)

    elif message.text == 'Правила':
        bot.send_message(message.chat.id, rules, reply_markup= main_menu_markup)
    
    else:
        bot.send_message(message.chat.id, 'Упс, такая команда не найдена. Если хочешь поиграть, тапни по кнопочке "Новая игра"', reply_markup = main_menu_markup)
    
bot.polling(none_stop=True, interval=0)