import datetime

from peewee import SqliteDatabase, Model, CharField, FloatField, DateTimeField, IntegerField

SqliteDB = SqliteDatabase('SQLite.db')


class SQLiteModel(Model):
    class Meta:
        database = SqliteDB


class ConfigModel(SQLiteModel):
    base_url = CharField()
    api_key = CharField()
    model = CharField()
    button_time = FloatField(null=True)
    button_select = CharField()
    history_num = IntegerField()


class HistoryModel(SQLiteModel):
    create_time = DateTimeField(default=datetime.datetime.now)
    context = CharField()
