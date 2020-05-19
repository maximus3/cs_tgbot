import telebot
from functools import wraps

import config
import utils
import views

bot = telebot.TeleBot(config.TOKEN)

sessionStorage = dict()
points = views.get_points()

def ssdecorator(func):
    @wraps(func)
    def new_func(message):
        mid = message.chat.id
        if mid not in sessionStorage:
            sessionStorage[mid] = utils.UserData()
        return func(message)

    return new_func

@bot.message_handler(commands=['enter'])
@ssdecorator
def main(message):
    keyboard = utils.get_Vadim_keyb()
    bot.send_message(message.chat.id, utils.textData['Vadim_q'], reply_markup=keyboard)


@bot.message_handler(commands=['signup'])
@ssdecorator
def signup(message):
    mid = message.chat.id
    username = views.signup_db()
    text = utils.textData['signup_OK']
    sessionStorage[mid].signup(username)
    bot.send_message(mid, text)


@bot.message_handler(commands=['game'])
@ssdecorator
def game(message):
    mid = message.chat.id
    user = sessionStorage[mid]
    user.cur = 0
    text = 'Игра началась!\n' + points[user.cur].question
    bot.send_message(mid, text)


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
def game_callback(call):
    mid = call.message.chat.id
    btn = call.data[5:]
    user = sessionStorage[mid]

    user.cur += 1
    if user.cur == len(points):
        views.save_score(user.username, user.score)
        user.logout()
        bot.edit_message_text(chat_id=mid,
                              message_id=call.message.message_id,
                              text=f"Ваш результат: {user.score} баллов!")
    else:
        text = 'Неправильно!\n'
        if btn == 'right':
            user.score += points[user.cur - 1].score
            text = 'Правильно!\n'
        text += 'Следующий вопрос:\n' + points[user.cur].question
        bot.edit_message_text(chat_id=mid,
                              message_id=call.message.message_id,
                              text=text)


if __name__ == '__main__':
    bot.infinity_polling()
