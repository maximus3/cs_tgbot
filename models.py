import peewee

database = peewee.SqliteDatabase('game.db')


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
    wrong_answer = peewee.TextField()
    right_answer = peewee.TextField()