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

    @property
    def show_name(self):
        return self.episode.show.name

    @property
    def channel_name(self):
        return self.channel.name

    @property
    def description(self):
        return self.episode.description

    @property
    def genre(self):
        return self.show.genre.name

    @property
    def actor_names(self):
        return [actor.actor.name for actor in self.episode.actors]

    @property
    def label_names(self):
        return [label.label.name for label in self.labels]


class Label(BaseModel):
    name = CharField()


class AiringLabelRelationship(BaseModel):
    airing = ForeignKeyField(Airing, related_name='labels')
    label = ForeignKeyField(Label, related_name='airings')


class ActorEpisodeRelationship(BaseModel):
    actor = ForeignKeyField(Actor, related_name='episodes')
    episode = ForeignKeyField(Episode, related_name='actors')
