from telebot import types
import random


class UserData:

    def __init__(self, username=None, score=0):
        self.logged = (username is not None)
        self.username = username
        self.score = score

    def signup(self, username):
        self.logged = True
        self.username = username

    def logout(self):
        self.logged = False
        self.username = None
        self.score = 0


textData = {
    'Vadim_q': 'У тебя что-то срочное?',
    'signup_OK': 'Регистрация прошла успешно!',
    'signup_ERR': 'Пользователь с данным никнеймом уже существует',
    'game_result': 'Ваш результат: {} баллов из {}',
    'no_reg': 'Вы должны зарегистрироваться!',
    'game_start': 'Игра началась!',
}

Vadim_ans = {
    'yes': 'Борода',
    'cig': 'Курить вредно',
    'cks': 'Мне в рот',
    'mhp': 'Денег нет, но вы держитесь'
}


def get_Vadim_keyb():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='vadim_yes')
    btn2 = types.InlineKeyboardButton(text='Пойдем курить', callback_data='vadim_cig')
    btn3 = types.InlineKeyboardButton(text='Куда положить печенье?', callback_data='vadim_cks')
    btn4 = types.InlineKeyboardButton(text='Как принимать матпомощь?', callback_data='vadim_mhp')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    return keyboard


def make_game_keyb(point, cur):
    wrongs = point.wrong_answer.split(';')
    right = point.right_answer
    data = []
    for elem in wrongs:
        data.append((elem, 'wrong' + str(len(data)) + str(cur)))
    data.append((right, 'right' + str(cur)))
    random.shuffle(data)

    keyboard = types.InlineKeyboardMarkup()
    for elem in data:
        btn = types.InlineKeyboardButton(text=elem[0], callback_data='game_' + elem[1])
        keyboard.add(btn)
    return keyboard


def get_sum_score(points):
    sm = 0
    for point in points:
        sm += point.score
    return sm