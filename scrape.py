import requests
from bs4 import BeautifulSoup
from twiggy import log
from datetime import datetime, timedelta
from tv.models import Channel
from tv.models import Show
from tv.models import Episode
from tv.models import Airing
from tv.models import Label


logger = log.name('gvascraper')

TODAY = datetime.now().date()
DAYS = ['vandaag', 'morgen', 'overmorgen']
TV_STATION_PAGES = (str(i) for i in range(27))
START_URLS = (("http://www.gva.be/tv-gids/{}/{}".format(day, tv_station_page), day)
            for day in DAYS
            for tv_station_page in TV_STATION_PAGES)


def get_date(day):
    to_add = {'vandaag': 0,
              'morgen': 1,
              'overmorgen': 2}
    return TODAY + timedelta(days=to_add.get(day))


def scrape_url(url, day):
    logger.info('Accessing {}', url)
    date = get_date(day)
    r = requests.get(url).text
    s = BeautifulSoup(r, "lxml")

    channels = (item.parent
                for item in s.find_all('div', {'class': 'tv-guide__channel'}))
    for channel in channels:
        channel_name = channel.div.text.strip()
        programs = channel.find_all('div', {'class': 'program'})

        for program in programs:
            begin_time = program.div.text
            program_name = program.find('a').text
            date, channel_name, begin_time, program_name
            yield date, channel_name, begin_time, program_name



if __name__ == '__main__':
    main()
