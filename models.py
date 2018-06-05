from peewee import SqliteDatabase
from peewee import Model
from peewee import DatetimeField
from peewee import CharField
from peewee import TextField
from peewee import ForeignKeyField


DATABASE = SqliteDatabase('tv.db')


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Channel(Model):
    name = CharField()


class Show(Model):
    name = CharField()


class Episode(Model):
    name = CharField()
    description = TextField()


class Airing(Model):
    channel = ForeignKeyField(Channel, related_name='airings')
    episode = ForeignKeyField(Episode, related_name='airings')
    begin_dt = DatetimeField()
    end_dt = DatetimeField()


class Label(Model):
    name = CharField()


class AiringLabelRelationship(Model):
    airing = ForeignKeyField(Airing, related_name='labels')
    label = ForeignKeyField(Label, related_name='airings')
