import falcon
import json
import datetime

from wsgiref import simple_server

from models import Airing
from models import Channel


class AiringResource:
    def on_get(self, request, response):
        body = {}
        today = datetime.datetime.now().date()
        airings = (Airing
                   .select())
                   #.where(Airing.show_name == "Thuis"))


        body["count"] = airings.count()
        body["airings"] = []

        for airing in airings:
            body["airings"].append(airing.dict())

        response.body = json.dumps(body)
        response.status == falcon.HTTP_200


class ChannelResource:
    def on_get(self, request, response):
        channels = Channel.select()
        body = {}

        body["count"] = channels.count()
        body["channels"] = [channel.name for channel in channels]

        response.body = json.dumps(body)
        response.status = falcon.HTTP_200


api = falcon.API()

airings = AiringResource()
api.add_route('/airing', airings)

channels = ChannelResource()
api.add_route("/channel", channels)



if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
