import requests
import re
import datetime
import locale
from bs4 import BeautifulSoup
from twiggy import log
from tv.models import Channel
from tv.models import Genre
from tv.models import Show
from tv.models import Episode
from tv.models import Airing
from tv.models import Label
from tv.models import Actor
from tv.models import ActorEpisodeRelationship
from tv.models import AiringLabelRelationship


locale.setlocale(locale.LC_ALL, "nl_BE")
logger = log.name('gvascraper')

TODAY = datetime.datetime.now().date()
DAYS = ['vandaag', 'morgen', 'overmorgen']
TV_STATION_PAGES = (str(i) for i in range(27))
START_URLS = ("http://www.gva.be/tv-gids/{}/{}".format(day, tv_station_page)
              for day in DAYS
              for tv_station_page in TV_STATION_PAGES)


def get_title(program):
    return program.find("h3", {"class": "program-full__title"}).text.strip()


def get_channel(program):
    string = (program
              .find("h3", {"class": "program-full__title"})
              .find_next("p")
              .text)
    regex_pattern = r"[^\|]*"
    return re.search(regex_pattern, string)[0].strip()


def get_genre(program):
    try:
        string = (program
                  .find("h3", {"class": "program-full__title"})
                  .find_next("p")
                  .text)
    except AttributeError:
        return "Onbekend"
    regex_pattern = r"^(?:\w+) \| ([\w\s]+) \| "

    try:
        return re.search(regex_pattern, string)[1].strip()
    except TypeError:
        return "Onbekend"


def get_actors(program):
    try:
        actors_string = program.find("p", {"class": "tvguide-actors"}).text
    except AttributeError:  # actors not found
        return []
    regex_pattern = r"((?:[A-Z][a-z]+\s*)+)(?:, | en |$)"
    return re.findall(regex_pattern, actors_string)


def get_month(month_string):
    return datetime.datetime.strptime(month_string, "%b").month


def get_day(day_string):
    return int(day_string)


def get_dts(program):
    string = program.find("span", {"class": "program-full__time"}).text
    regex_pattern = r"(?P<date_of_week>[a-z]+) "
    regex_pattern += r"(?P<day>\d{2}) "
    regex_pattern += r"(?P<month>[a-z]{3}), "
    regex_pattern += r"(?P<begin_hour>\d{2})u(?P<begin_minutes>\d{2}) - "
    regex_pattern += r"(?P<end_hour>\d{2})u(?P<end_minutes>\d{2})"
    parsed = re.match(regex_pattern, string)

    month = get_month(parsed["month"])
    day = get_day(parsed["day"])

    if month == 12 and day > 25:
        raise NotImplementedError("Year will cause problems soon...")

    begin_hour = int(parsed["begin_hour"])
    begin_minutes = int(parsed["begin_minutes"])

    end_hour = int(parsed["end_hour"])
    end_minutes = int(parsed["end_minutes"])

    current_year = TODAY.year

    begin_dt = datetime.datetime(
        current_year,
        month,
        day,
        begin_hour,
        begin_minutes)
    end_dt = datetime.datetime(
        current_year,
        month,
        day,
        end_hour,
        end_minutes)

    if end_dt < begin_dt:  # crossed over midnight
        end_dt + datetime.timedelta(days=1)

    return begin_dt, end_dt


def get_description(program):
    try:
        return (program
                .find("p", {"class": "tvguide-actors"})
                .findNext()
                .text
                .strip())
    except AttributeError:
        return ""


def get_labels(program):
    return [label.text
            for label in program.find_all(
                "span", {"class": "label"})]


def add_program_to_database(program):
    title = get_title(program)
    channel = get_channel(program)
    channel = Channel.get_or_create(name=channel)[0]
    begin_dt, end_dt = get_dts(program)

    actors = get_actors(program)
    description = get_description(program)
    genre = get_genre(program)
    genre = Genre.get_or_create(name=genre)[0]
    labels = get_labels(program)

    show = Show.get_or_create(name=title, genre=genre)[0]
    episode = Episode.get_or_create(show=show, description=description)[0]
    airing = Airing.get_or_create(
        episode=episode,
        channel=channel,
        begin_dt=begin_dt,
        end_dt=end_dt)[0]

    for name in actors:
        actor = Actor.get_or_create(name=name)[0]
        ActorEpisodeRelationship.get_or_create(actor=actor, episode=episode)

    for name in labels:
        label = Label.get_or_create(name=name)[0]
        AiringLabelRelationship(airing=airing, label=label)


def scraper(url):
    logger.info('Accessing {}', url)
    request = requests.get(url).text
    soup = BeautifulSoup(request, "lxml")

    for program in soup.find_all('div', {'class': 'title'}):
        request = requests.get(program.a["href"]).text
        soup = BeautifulSoup(request, "lxml")
        program = soup.find("div", {"class": "program-full"})
        add_program_to_database(program)


def main():
    for url in START_URLS:
        scraper(url)


if __name__ == '__main__':
    main()
