import random
import time
import threading
import telebot
from telebot import types
import json

token = "8335377033:AAHK-ifuPPkFJwoiuDw5nLuPNZdE2bCyv_o"
bot = telebot.TeleBot(token)
money = 0
people = 0
money_min = 0
difficult = " "
user_json = 'users.json'

residential_buildings = 1
industrial_buildings = 1
office_buildings = 1

empty_people = 0

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать игру")
    markup.add(btn1)

    bot.reply_to(message, "Добро пожаловать в игру CityBuilder. В этой игре вы сможете построить город своей мечты.", reply_markup=markup)

def load_data():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

def get_user(user_id):
    data = load_data()

    if str(user_id) not in data:
        data[str(user_id)] = {
            "money": 0,
            "people": 0,
            "industrial_buildings": 0,
            "residential_buildings": 0,
            "office_buildings": 0,
            "empty_people": 0
        }
        save_data(data)
    return data


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
    user_id = message.from_user.id
    data = get_user(user_id)
    user = data[str(user_id)]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn11 = types.KeyboardButton("Строить")
    btn12 = types.KeyboardButton("Статистика")
    markup.add(btn11,btn12)
    bot.reply_to(message,f"Денег: {user['money']}\n"
                 f"Количество жителей: {user['people']}\n", reply_markup=markup)

def time_money():
    global money, industrial_buildings
    while True:
        if industrial_buildings > 0:
            industrial_income = industrial_buildings * 2000
            money+=industrial_income
        time.sleep(30)

        if office_buildings > 0:
            ofice_income = industrial_buildings * 3000
            money+=ofice_income
        time.sleep(30)


def reset_values(message, money):
    user_id = message.from_user.id
    data = get_user(user_id)
    user = data[str(user_id)]

    user["money"] = money
    user["people"] = 0
    user["empty_people"] = 0
    user["industrial_buildings"] = 0

    save_data(data)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global money, people, difficult, residential_buildings, industrial_buildings, office_buildings, money_min, empty_people
    user_id = message.from_user.id
    data = get_user(user_id)
    user = data[str(user_id)]

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
        reset_values(message, 500000)
        difficult = "Лёгкая"
        menu(message)

    if message.text == "Нормальная":
        reset_values(message, 300000)
        difficult = "Нормальная"
        menu(message)

    if message.text == "Сложная":
        reset_values(message, 200000)
        difficult = "Сложная"
        menu(message)

    if message.text == "Построить жилое здание":
        if user["money"] >= 20000:
            user["money"] -= 20000
            residential_people = random.randint(200, 500)
            user["people"] += residential_people
            user["empty_people"] += residential_people
            bot.reply_to(message, f"Вы построили жилое здание. Количество денег на данный момент: {user['money']}\n"
                         f"Количество жителей: {user['people']}\n"
                         f"Количество свободных жителей: {user['empty_people']}")
            user["residential_buildings"] += 1
        else:
            bot.reply_to(message, f"Не хватает денег")
        save_data(data)

    if message.text == "Построить промышленное здание":
        print(f"{user['empty_people']} / {(user['industrial_buildings'] + 1)}")
        if user["money"] >= 30000 and user["empty_people"] >= 700:
            user["empty_people"] -= 700
            user["money"] -= 30000
            user["industrial_buildings"] += 1
            bot.reply_to(message, f"Вы построили промышленное здание. Количество денег на данный момент: {user['money']}\n"
                         f"Количество жителей: {user['people']}\n"
                         f"Количество свободных жителей: {user['empty_people']}")
        else:
            bot.reply_to(message, f"Не хватает денег или жителей.")
        save_data(data)

    if message.text == "Построить офисное здание":
        if user["money"] >= 40000 and user["empty_people"] >= 1000:
            user["empty_people"] -= 1000
            user["money"] -= 40000
            user["industrial_buildings"] += 1
            bot.reply_to(message, f"Вы построили офисное здание. Количество денег на данный момент: {user['money']}\n"
                         f"Количество жителей: {user['people']}\n"
                         f"Количество свободных жителей: {user['empty_people']}")
        else:
            bot.reply_to(message, f"Не хватает денег или жителей.")
        save_data(data)

    if message.text == "Вернуться назад":
        menu(message)

    if message.text == "Строить":
        build(message)

    if message.text == "Статистика":
        bot.reply_to(message, f"Денег: {money}\n"
                     f"Количество жителей: {people}\n"
                     f"Жилых зданий: {residential_buildings-1}\n"
                     f"Промышленных зданий: {industrial_buildings-1}\n"
                     f"Офисных зданий: {office_buildings-1}")




threading.Thread(target=time_money, daemon=True).start()
bot.polling(none_stop=True, interval=0)
