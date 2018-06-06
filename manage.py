from tv.models import Channel
from tv.models import Genre
from tv.models import Show
from tv.models import Episode
from tv.models import Airing
from tv.models import Label
from tv.models import Actor
from tv.models import ActorEpisodeRelationship
from tv.models import AiringLabelRelationship


def create_tables(fail_silently=True):
    Channel.create_table(fail_silently=fail_silently)
    Genre.create_table(fail_silently=fail_silently)
    Show.create_table(fail_silently=fail_silently)
    Episode.create_table(fail_silently=fail_silently)
    Airing.create_table(fail_silently=fail_silently)
    Label.create_table(fail_silently=fail_silently)
    Actor.create_table(fail_silently=fail_silently)
    ActorEpisodeRelationship.create_table(fail_silently=fail_silently)
    AiringLabelRelationship.create_table(fail_silently=fail_silently)
