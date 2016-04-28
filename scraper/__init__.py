import requests
from bs4 import BeautifulSoup
from twiggy import log


logger = log.name('gvascraper')

DAYS = ['vandaag', 'morgen', 'overmorgen']
URLS = ("http://www.gva.be/tv-gids/{}/{}".format(day, str(i)) for day in DAYS for i in range(27))

def scrape_url(url):
    logger.info('Accessing {}', url) 
    r = requests.get(url).text
    s = BeautifulSoup(r, "lxml")

    channels = (item.parent for item in s.find_all('div', {'class': 'tv-guide__channel'}))
    for channel in channels:
        channel_name = channel.div.text.strip()
        programs = channel.find_all('div', {'class': 'program'})

        for program in programs:
            begin_time = program.div.text
            program_name = program.find('a').text
            yield channel_name, begin_time, program_name

def main():
    for url in URLS:
        yield from scrape_url(url)

if __name__ == '__main__':
    main()

