from telebot import types

Vadim_q = 'У тебя что-то срочное?'

Vadim_ans = {
    'yes': 'Борода',
    'cig': 'Курить вредно',
    'cks': 'Мне в рот',
    'mhp': 'Денег нет, но вы держитесь'
}

def get_Vadim_keyb():
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
    btn2 = types.InlineKeyboardButton(text='Пойдем курить', callback_data='cig')
    btn3 = types.InlineKeyboardButton(text='Куда положить печенье?', callback_data='cks')
    btn4 = types.InlineKeyboardButton(text='Как принимать матпомощь?', callback_data='mhp')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    return keyboard


