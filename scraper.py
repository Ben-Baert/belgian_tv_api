import requests
from bs4 import BeautifulSoup


urls = ("http://www.gva.be/tv-gids/vandaag/{}".format(str(i)) for i in range(27))
for url in urls:
    r = requests.get(url).text
    s = BeautifulSoup(r)

    channels = (item.parent for item in s.find_all('div', {'class': 'tv-guide__channel'}))
    for channel in channels:
        channel_name = channel.div.text.strip()
        programs = channel.find_all('div', {'class': 'program'})

        for program in programs:
            begin_time = program.div.text
            program_name = program.find('a').text
            print(channel_name, begin_time, program_name)

