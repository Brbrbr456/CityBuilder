import random
import time
import threading
import telebot
from telebot import types

token = "8335377033:AAHK-ifuPPkFJwoiuDw5nLuPNZdE2bCyv_o"
bot = telebot.TeleBot(token)
money = 0
people = 0
money_min = 0
difficult = " "

residential_buildings = 1
industrial_buildings = 1
ofice_buildings = 1

empty_people = 0

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    markup.add(btn1)

    bot.reply_to(message, "Добро пожаловать в игру CityBuilder. В этой игре вы сможете построить город своей мечты.", reply_markup=markup)


@bot.message_handler(commands=["build"])
def build(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn7 = types.KeyboardButton("Построить жилое здание")
    btn8 = types.KeyboardButton("Построить промышленное здание")
    btn9 = types.KeyboardButton("Построить офисное здание")
    btn10 = types.KeyboardButton("Вернуться назад")
    markup.add(btn7,btn8,btn9,btn10)
    bot.reply_to(message, f"Выберите здание", reply_markup=markup)

@bot.message_handler(commands=["menu"])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn11 = types.KeyboardButton("Строить")
    btn12 = types.KeyboardButton("Статистика")
    markup.add(btn11,btn12)
    bot.reply_to(message,f"Денег: {money}\n"
                 f"Количество жителей: {people}\n", reply_markup=markup)

def time_money():
    global money, industrial_buildings
    while True:
        if industrial_buildings > 0:
            income = industrial_buildings * 1000
            money+=income
        time.sleep(30)




@bot.message_handler(content_types=["text"])
def handle_text(message):
    global money, people, difficult, residential_buildings, industrial_buildings, ofice_buildings, money_min, empty_people

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
        difficult = "Лёгкая"
        menu(message)

    if message.text == "Нормальная":
        money = 300000
        people = 0
        difficult = "Нормальная"
        menu(message)

    if message.text == "Сложная":
        money = 200000
        people = 0
        difficult = "Сложная"
        menu(message)

    if message.text == "Построить жилое здание":
        if money >= 20000:
            money -= 20000
            residential_people = random.randint(200, 500)
            people += residential_people
            empty_people += residential_people
            bot.reply_to(message, f"Вы построили жилое здание. Количество денег на данный момент: {money}\n"
                         f"Количество жителей: {people}")
            residential_buildings+=1
        else:
            bot.reply_to(message, f"Не хватает денег")

    if message.text == "Построить промышленное здание":
        if money >= 30000 and empty_people / industrial_buildings >= 700:
            empty_people -= 700
            money -= 30000
            bot.reply_to(message, f"Вы построили промышленное здание. Количество денег на данный момент: {money}\n"
                         f"Количество жителей: {people}")
            industrial_buildings+=1
        else:
            bot.reply_to(message, f"Не хватает денег или жителей.")

    if message.text == "Построить офисное здание":
        if money >= 30000 and empty_people / ofice_buildings >= 1000:
            empty_people -= 1000
            money -= 30000
            bot.reply_to(message, f"Вы построили офисное здание. Количество денег на данный момент: {money}\n"
                         f"Количество жителей: {people}")
            ofice_buildings+=1
        else:
            bot.reply_to(message, f"Не хватает денег или жителей.")

    if message.text == "Вернуться назад":
        menu(message)

    if message.text == "Строить":
        build(message)

    if message.text == "Статистика":
        bot.reply_to(message, f"Денег: {money}\n"
                     f"Количество жителей: {people}\n"
                     f"Жилых зданий: {residential_buildings-1}\n"
                     f"Промышленных зданий: {industrial_buildings-1}\n"
                     f"Офисных зданий: {ofice_buildings-1}")




threading.Thread(target=time_money, daemon=True).start()
bot.polling(none_stop=True, interval=0)
