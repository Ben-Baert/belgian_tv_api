from scraper import main as scrape


class TestScraper():
    def setup_method(self, method):
        self.items = list(scrape())
        self.channels = [channel for channel, _, _ in self.items]
 
    def test_channels(self):
        to_try = [
                'EEN',
                'VTM']
        assert all(channel in self.channels for channel in to_try)

    def test_programs(self):
        assert ("EEN", "19:00", "Het Journaal - Sport") in self.items

    def test_days(self):
        assert self.items.count(("EEN", "19:00", "Het Journaal - Sport")) == 3

