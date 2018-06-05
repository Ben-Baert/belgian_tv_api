import requests
import re
import locale
from bs4 import BeautifulSoup
from twiggy import log
from datetime import datetime, timedelta
from tv.models import Channel
from tv.models import Show
from tv.models import Episode
from tv.models import Airing
from tv.models import Label

locale.setlocale(locale.LC_ALL, "nl_BE")
logger = log.name('gvascraper')

TODAY = datetime.now().date()
DAYS = ['vandaag', 'morgen', 'overmorgen']
TV_STATION_PAGES = (str(i) for i in range(27))
START_URLS = (("http://www.gva.be/tv-gids/{}/{}".format(day, tv_station_page), day)
            for day in DAYS
            for tv_station_page in TV_STATION_PAGES)


def get_program_title(program):
    return program.find("h3", {"class": "program-full__title"}).text.strip()


def get_channel(program):
    string = program.find("h3", {"class": "program-full__title"}).find_next("p").text
    regex_pattern = r"^(\w+)"
    return re.search(regex_pattern, string)


def get_genre(program): 
    string = program.find("h3", {"class": "program-full__title"}).find_next("p").text
    regex_pattern = r"^(?:\w+) \| (\w+) \| "
    return re.search(regex_pattern, string)


def get_program_actors(program):
    actors_string = program.find("p", {"class": "tvguide-actors"}).text
    regex_pattern = r"((?:[A-Z][a-z]+\s*)+)(?:, | en |$)"
    return re.findall(regex_pattern, actors_string)


def get_month(month_string):
    return datetime.strptime(month_string, "%b").month


def get_day(day_string):
    return int(day_string)


def get_dts(program):
    string = program.find("span", {"class": "program-full__time"})
    regex_pattern = "(?P<date_of_week>[a-z]+) (?P<day>\d{2}) (?P<month>[a-z]{3}), (?P<begin_hour>\d{2})u(?P<begin_minutes>\d{2}) - (?P<end_hour>\d{2})u(?P<end_minutes>\d{2})"
    parsed = re.match(regex_pattern, string)

    month = get_month(parsed["month"])
    day = get_day(parsed["day"])

    begin_hour = int(parsed["begin_hour"])
    begin_minutes = int(parsed["begin_minutes"])

    end_hour = int(parsed["end_hour"])
    end_minutes = int(parsed["end_minutes"])

    begin_dt = datetime.datetime(2018, month, day, begin_hour, begin_minutes)  # CHANGE THIS!!
    end_dt = datetime.datetime(2018, month, day, end_hour, end_minutes)  # CHANGE THIS!!

    if end_dt < begin_dt:  # crossed over midnight
        end_dt + datetime.timedelta(days=1)

    return begin_dt, end_dt


def get_description(program):
    return program.find("p", {"class": "tvguide-actors"}).findNext().text.strip()


def get_labels(program):
    for label in program.find_all("span", {"class": "label"}):
        yield label.text


def add_program_to_database(program):
    pass


def scrape_start_url_from_program_detail_urls(url, day):
    logger.info('Accessing {}', url)
    request = requests.get(url).text
    soup = BeautifulSoup(request, "lxml")

    for program in soup.find_all('div', {'class': 'title'}):
        request = requests.get(program.a["href"]).text
        soup = BeautifulSoup(request, "lxml")
        program = soup.find("div", {"class": "program-full"})


def main():
    for url in START_URLS:
        scrape_url(url)


if __name__ == '__main__':
    main()
