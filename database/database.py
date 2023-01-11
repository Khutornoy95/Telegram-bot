from peewee import *


db = SqliteDatabase('database/history.db')

class BaseModel(Model):
    class Meta:
        database = db

class History(BaseModel):
    chat_id = IntegerField()
    command = CharField()
    date = DateTimeField()
    hotels = CharField()
