import peewee

from config import DATABASE_NAME

database = peewee.SqliteDatabase(DATABASE_NAME)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    user_id = peewee.AutoField()
    username = peewee.CharField(null=True, unique=True)
    join_date = peewee.DateTimeField()
    score = peewee.IntegerField(default=0)


class Point(BaseModel):
    score = peewee.IntegerField()
    question = peewee.TextField()
    right_answer = peewee.TextField()
    wrong_answer = peewee.TextField()