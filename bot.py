import telebot
from telebot import types

import config
import utils

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['enter', 'start'])
def main(message):
    keyboard = utils.get_Vadim_keyb()
    bot.send_message(message.chat.id, utils.Vadim_q, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: call.message and call.message.text == utils.Vadim_q)
def Vadim_callback(call):
    mid = call.message.chat.id
    bot.edit_message_text(chat_id = mid,
            message_id = call.message.message_id,
            text = call.message.text)
    bot.send_message(chat_id=mid, text=utils.Vadim_ans[call.data])


if __name__ == '__main__':
    bot.infinity_polling()
