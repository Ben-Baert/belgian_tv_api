import falcon


class DayResource:
    def on_get(request, response):
        pass


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
api.register