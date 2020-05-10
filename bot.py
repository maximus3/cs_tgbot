import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['enter', 'start'])
def main(message):
    mid = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
    btn2 = types.InlineKeyboardButton(text='Пойдем курить', callback_data='cig')
    btn3 = types.InlineKeyboardButton(text='Куда положить печенье?', callback_data='cks')
    btn4 = types.InlineKeyboardButton(text='Как принимать матпомощь?', callback_data='mhp')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    bot.send_message(mid, 'У тебя что-то срочное?', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "test":
            bot.send_message(chat_id=call.message.chat.id, text='Борода')
        elif call.data == 'cig':
            bot.send_message(chat_id=call.message.chat.id, text='Курить вредно')
        elif call.data == 'cks':
            bot.send_message(chat_id=call.message.chat.id, text='Мне в рот')
        elif call.data == 'mhp':
            bot.send_message(chat_id=call.message.chat.id, text='Денег нет, но вы держитесь')


if __name__ == '__main__':
    bot.infinity_polling()
