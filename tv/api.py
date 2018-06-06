import falcon
import json
from models import Airing
from api_helpers import get_name


class DayResource:
    def on_get(request, response):
        body = []
        today = datetime.datetime.now().date()
        airings = (Airing
                   .select()
                   .where(Airing.begin_dt.date() == today))

        for airing in airings:
            airing_dict = {}
            airing_dict["name"] = airing.show_name
            airing_dict["description"] = airing.description
            airing_dict["begin_dt"] = airing.begin_dt
            airing_dict["end_dt"] = airing.end_dt
            airing_dict["channel"] = airing.channel_name
            airing_dict["genre"] = airing.genre
            airing_dict["actors"] = airing.actor_names
            airing_dict["labels"] = airing.label_names
            body.append(airing_dict)

        response.body = json.dumps(airing_dict)
        response.status_code == 200


class ChannelResource:
    def on_get(request, response):
        pass


class ShowResource:
    def on_get(request, response):
        pass


class ActorResource:
    def on_get(request, response):
        pass


class GenreResource:
    def on_get(request, response):
        pass

api = falcon.API()
days = DayResource()
api.register('/day', days)
