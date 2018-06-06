import falcon
import json
import datetime

from wsgiref import simple_server

from models import Airing
from models import Channel
from models import Show


class AiringResource:
    def on_get(self, request, response):
        body = {}
        begin_dt = request.
        airings = (Airing
                   .select())
                   #.where(Airing.show_name == "Thuis"))


        body["count"] = airings.count()
        body["airings"] = []

        for airing in airings:
            body["airings"].append(airing.dict())

        response.body = json.dumps(body)
        response.status == falcon.HTTP_200

        # filter by begin_dt
        # filter by end_dt
        # filter by show
        # filter by actor
        # filter by channel
        # option to sort
        # cache with REDIS


class ChannelResource:
    def on_get(self, request, response):
        channels = Channel.select()
        body = {}

        body["count"] = channels.count()
        body["channels"] = [channel.name for channel in channels]

        response.body = json.dumps(body)
        response.status = falcon.HTTP_200

        # cache with REDIS


class ShowResource:
    def on_get(self, request, response):
        shows = Show.select()
        body = {}

        body["count"] = shows.count()
        body["shows"] = [show.name for show in shows]

        response.body = json.dumps(body)
        response.status = falcon.HTTP_200

        # cache with REDIS


api = falcon.API()

airings = AiringResource()
api.add_route('/airing', airings)

channels = ChannelResource()
api.add_route("/channel", channels)

shows = ShowResource()
api.add_route("/show", shows)



if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
