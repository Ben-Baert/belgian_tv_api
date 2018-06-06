import datetime
import bs4

from tv.scraper import get_title
from tv.scraper import get_genre
from tv.scraper import get_channel
from tv.scraper import get_actors
from tv.scraper import get_labels
from tv.scraper import get_description
from tv.scraper import get_month
from tv.scraper import get_day
from tv.scraper import get_dts


CASE_1 = bs4.BeautifulSoup("""
<div class="program-full">
                    <h3 class="program-full__title"> Lentebeelden</h3>
                    <p>EEN | Sfeerbeelden vanuit diverse Europese bestemmingen | <span class="program-full__time">woensdag 06 jun, 09u00 - 10u00</span>.</p>
                    
                </div>
""", "lxml")

CASE_1_ATTRIBUTES = {
    "title": "Lentebeelden",
    "genre": "Sfeerbeelden vanuit diverse Europese bestemmingen",
    "channel": "EEN",
    "actors": [],
    "labels": [],
    "dts": (datetime.datetime(2018, 6, 6, 9, 0), datetime.datetime(2018, 6, 6, 10, 0))
}

CASE_2 = bs4.BeautifulSoup("""
<div class="program-full">
                    <h3 class="program-full__title"> Thuis</h3>
                    <p>EEN | Soapserie | <span class="program-full__time">woensdag 06 jun, 20u10 - 20u40</span>.</p>
                    <p class="tvguide-actors">met Jeroen Lenaerts, Katrien De Ruysscher, An Vanderstighelen en Moora Vander Veken</p>  <p> Adil schiet in actie. Leo is bezorgd over Marianne en na een bezoek van Tom schiet hij helemaal uit zijn krammen. Jacques doet Joren een voorstel, maar zullen Tim en Sam daarmee akkoord willen gaan? Waldek zit met enorm veel vragen waarop hij geen antwoord heeft.</p><span class="label label--beta">Teletekst</span>
                </div>
""", "lxml")

CASE_2_ATTRIBUTES = {
    "title": "Thuis",
    "genre": "Soapserie",
    "channel": "EEN",
    "actors": ["Jeroen Lenaerts",  "Katrien De Ruysscher", "An Vanderstighelen", "Moora Vander Veken"],
    "description": "Adil schiet in actie. Leo is bezorgd over Marianne en na een bezoek van Tom schiet hij helemaal uit zijn krammen. Jacques doet Joren een voorstel, maar zullen Tim en Sam daarmee akkoord willen gaan? Waldek zit met enorm veel vragen waarop hij geen antwoord heeft.",
    "labels": ["Teletekst"],
    "dts": (datetime.datetime(2018, 6, 6, 20, 10), datetime.datetime(2018, 6, 6, 20, 40))
}

def test_get_month():
    assert get_month("jun") == 6


def test_get_day():
    assert get_day("6") == 6


def test_case_one_get_title():
    assert get_title(CASE_1) == CASE_1_ATTRIBUTES["title"]


def test_case_two_get_title():
    assert get_title(CASE_2) == CASE_2_ATTRIBUTES["title"]


def test_case_one_get_genre():
    assert get_genre(CASE_1) == CASE_1_ATTRIBUTES["genre"]


def test_case_two_get_genre():
    assert get_genre(CASE_2) == CASE_2_ATTRIBUTES["genre"]


def test_case_one_get_channel():
    assert get_channel(CASE_1) == CASE_1_ATTRIBUTES["channel"]


def test_case_two_get_channel():
    assert get_channel(CASE_2) == CASE_2_ATTRIBUTES["channel"]


def test_case_one_get_actors():
    assert get_actors(CASE_1) == CASE_1_ATTRIBUTES["actors"]


def test_case_two_get_actors():
    assert get_actors(CASE_2) == CASE_2_ATTRIBUTES["actors"]


def test_case_one_get_labels():
    assert get_labels(CASE_1) == CASE_1_ATTRIBUTES["labels"]


def test_case_two_get_labels():
    assert get_labels(CASE_2) == CASE_2_ATTRIBUTES["labels"]


def test_case_one_get_dts():
    assert get_dts(CASE_1) == CASE_1_ATTRIBUTES["dts"]


def test_case_two_get_dts():
    assert get_dts(CASE_2) == CASE_2_ATTRIBUTES["dts"]
