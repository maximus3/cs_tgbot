from models import *
from datetime import date


def create_tables():
    with database:
        database.create_tables([User, Point])


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