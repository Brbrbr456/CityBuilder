import telebot
from telebot import types

token = "8335377033:AAGEfUD9Evq_9jJGngVdcMiUevsbXNqyZhI"
bot = telebot.TeleBot(token)
money = 0
people = 0

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    markup.add(btn1)

    bot.reply_to(message, "Добро пожаловать в игру CityBuilder. В этой игре вы сможете построить город своей мечты.", reply_markup=markup)


@bot.message_handler(commands=["build"])
def build(message):
    print("asjdajdlasjd")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn7 = types.KeyboardButton("Построить жилое здание")
    btn8 = types.KeyboardButton("Построить промышленное здание")
    btn9 = types.KeyboardButton("Построить офисное здание")
    markup.add(btn7,btn8,btn9)
    bot.reply_to(message, f"Выберите здание", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global money, people

    if message.text == "Начать игру":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Лёгкая")
        btn3 = types.KeyboardButton("Нормальная")
        btn4 = types.KeyboardButton("Сложная")
        btn5 = types.KeyboardButton("Описание сложностей")
        markup.add(btn2,btn3,btn4,btn5)
        bot.reply_to(message, "Выберить сложность игры.", reply_markup=markup)
    if message.text == "Описание сложностей":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn6 = types.KeyboardButton("Начать игру")
        markup.add(btn6)
        bot.reply_to(message, f"Бюджет города:\n"
                              f"Лёгкая: 500000$ \n"
                              f"Нормальная: 300000$ \n"
                              f"Сложная: 500000$ ", reply_markup=markup)

    if message.text == "Лёгкая":
        money = 500000
        people = 0
        bot.reply_to(message, "Введите команду /build для постройки новых зданий")

    if message.text == "Нормальная":
        money = 300000
        people = 0
        bot.reply_to(message, "Введите команду /build для постройки новых зданий")

    if message.text == "Сложная":
        money = 200000
        people = 0
        bot.reply_to(message, "Введите команду /build для постройки новых зданий")

    if message.text == "Построить жилое здание":
        money -= 20000
        bot.reply_to(message, f"Вы построили жилое здание. Количество денег на данный момент: {money}")

    if message.text == "Построить промышленное здание":
        money -= 30000
        bot.reply_to(message, f"Вы построили промышленное здание. Количество денег на данный момент: {money}")

    if message.text == "Построить офисное здание":
        money -= 30000
        bot.reply_to(message, f"Вы построили офисное здание. Количество денег на данный момент: {money}")



bot.polling(none_stop=True, interval=0)