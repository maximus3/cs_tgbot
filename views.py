from models import *
from datetime import date
import os


def create_tables():
    if os.path.exists(DATABASE_NAME):
        return
    with database:
        database.create_tables([User, Point])
    Point.create(score=1,
                 question='Какой ответ верный?',
                 right_answer='Этот',
                 wrong_answer='Не этот')
    Point.create(score=7,
                 question='Сколько стоит рубль?',
                 right_answer='1 рубль',
                 wrong_answer='75 рублей;5 рублей;2 рубля')
    Point.create(score=3,
                 question='Квадратный корень из 256',
                 right_answer='16',
                 wrong_answer='25;13;256;6;36')
    Point.create(score=9,
                 question='В мире лучше нет пока',
                 right_answer='факультета ВМК',
                 wrong_answer='молока и огурца;Я вчера купил слона;Ратата тата тата;Мда')


def signup_db(username=None, score=0):
    try:
        if username is not None:
            user = User.create(username=username, join_date=date.today(), score=score)
        else:
            user = User.create(join_date=date.today(), score=score)
            user.username = 'user' + str(user.user_id)
            user.save()
    except peewee.IntegrityError:
        return None
    return user.username


def get_points():
    return Point.select()


def save_score(username, score):
    query = User.update(score=score).where(User.username==username)
    return query.execute()