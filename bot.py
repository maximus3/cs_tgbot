import telebot
from functools import wraps

import config
import utils
import views

bot = telebot.TeleBot(config.TOKEN)

views.create_tables()

sessionStorage = dict()
points = views.get_points()
sum_score = utils.get_sum_score(points)


def ssdecorator(func):
    @wraps(func)
    def new_func(message):
        mid = message.chat.id
        if mid not in sessionStorage:
            sessionStorage[mid] = utils.UserData()
        return func(message)
    return new_func


def check_reg(func):
    @wraps(func)
    def new_func(message):
        mid = message.chat.id
        if not sessionStorage[mid].logged:
            bot.send_message(mid, utils.textData['no_reg'])
        else:
            return func(message)
    return new_func


def check_reg_call(func):
    @wraps(func)
    def new_func(call):
        mid = call.message.chat.id
        if mid not in sessionStorage or not sessionStorage[mid].logged:
            bot.send_message(mid, utils.textData['no_reg'])
        else:
            return func(call)
    return new_func


@bot.message_handler(commands=['start'])
@ssdecorator
def start(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['enter'])
@ssdecorator
def enter(message):
    keyboard = utils.get_Vadim_keyb()
    bot.send_message(message.chat.id, utils.textData['Vadim_q'], reply_markup=keyboard)


@bot.message_handler(commands=['signup'])
@ssdecorator
def signup(message):
    mid = message.chat.id
    if sessionStorage[mid].logged:
        bot.send_message(mid, 'Вы уже зарегистрированны')
        return
    username = views.signup_db()
    text = utils.textData['signup_OK']
    sessionStorage[mid].signup(username)
    bot.send_message(mid, text)


@bot.message_handler(commands=['game'])
@ssdecorator
@check_reg
def game(message):
    mid = message.chat.id
    user = sessionStorage[mid]
    user.cur = 0
    text = utils.textData['game_start'] + '\n' + points[user.cur].question
    keyboard = utils.make_game_keyb(points[user.cur], user.cur)
    bot.send_message(mid, text, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
@ssdecorator
def echo(message):
    bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: call.message and call.data.startswith('vadim_'))
def Vadim_callback(call):
    mid = call.message.chat.id
    btn = call.data[6:]

    bot.edit_message_text(chat_id=mid,
                          message_id=call.message.message_id,
                          text=call.message.text)
    bot.send_message(chat_id=mid, text=utils.Vadim_ans[btn])


@bot.callback_query_handler(func=lambda call: call.message and call.data.startswith('game_'))
@check_reg_call
def game_callback(call):
    mid = call.message.chat.id
    btn = call.data[5:]
    user = sessionStorage[mid]

    user.cur += 1
    text = 'Неправильно!\n'
    if btn.startswith('right'):
        user.score += points[user.cur - 1].score
        text = 'Правильно!\n'
    if user.cur == len(points):
        views.save_score(user.username, user.score)
        score = user.score
        user.logout()
        bot.edit_message_text(chat_id=mid,
                              message_id=call.message.message_id,
                              text=text + utils.textData['game_result'].format(score, sum_score))
    else:
        text += 'Следующий вопрос:\n' + points[user.cur].question
        keyboard = utils.make_game_keyb(points[user.cur], user.cur)
        bot.edit_message_text(chat_id=mid,
                              message_id=call.message.message_id,
                              text=text,
                              reply_markup=keyboard)


if __name__ == '__main__':
    bot.infinity_polling()
