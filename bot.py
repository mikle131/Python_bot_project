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
main_menu_markup.add(my_account)
main_menu_markup.add(go_game)


@bot.message_handler(commands=['start'])
def hello_message(message):
    if message.chat.id in registered_users:
        go_main = types.KeyboardButton("Главное меню")
        markup.add(go_main)
        bot.send_message(message.chat.id, 'Привет-привет! Ты уже зареган). Перейди в главное меню, чтобы начать игру', reply_markup = markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        first_message = 'Привет, ' + message.from_user.username + '!👋🏼' + 2 * '\n' + 'Перед тем как начать, пожалуйста, зарегестрируйся. Это быстро📝'
        bot.send_message(message.chat.id, first_message )
        question = 'Придуймай свой игровой никнейм'
        bot.send_message(message.chat.id, question)
        enter_nick[message.chat.id] = -1

@bot.message_handler(content_types=['text'])
def message_reply(message):
    if enter_nick[message.chat.id] == -1:
        nickname = message.text
        enter_nick[message.chat.id] = 1
        registered_users.append(message.chat.id)
        #Вот тут надо добавить игрока в бдшку. 
        bot.send_message(message.chat.id, 'Поздравляю, ты зарегестрировался! Ты в главном меню', reply_markup = main_menu_markup)

    if message.chat.id not in registered_users:
        go_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        start = types.KeyboardButton("/start")
        go_start.add(start)
        bot.send_message(message.chat.id, 'Привет! Чтобы начать пользовать ботом, введи команду /start', reply_markup = go_start)
    
    