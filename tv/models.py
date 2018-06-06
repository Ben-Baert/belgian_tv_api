from peewee import SqliteDatabase
from peewee import Model
from peewee import DateTimeField
from peewee import CharField
from peewee import TextField
from peewee import ForeignKeyField


DATABASE = SqliteDatabase('tv.db')


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Actor(BaseModel):
    name = CharField()


class Genre(BaseModel):
    name = CharField()


class Channel(BaseModel):
    name = CharField()


class Show(BaseModel):
    name = CharField()
    genre = ForeignKeyField(Genre, related_name='shows')


class Episode(BaseModel):
    show = ForeignKeyField(Show, related_name='episodes')
    description = TextField()


class Airing(BaseModel):
    channel = ForeignKeyField(Channel, related_name='airings')
    episode = ForeignKeyField(Episode, related_name='airings')
    begin_dt = DateTimeField()
    end_dt = DateTimeField()


class Label(BaseModel):
    name = CharField()


class AiringLabelRelationship(BaseModel):
    airing = ForeignKeyField(Airing, related_name='labels')
    label = ForeignKeyField(Label, related_name='airings')


class ActorEpisodeRelationship(BaseModel):
    actor = ForeignKeyField(Actor, related_name='episodes')
    episode = ForeignKeyField(Episode, related_name='actors')
