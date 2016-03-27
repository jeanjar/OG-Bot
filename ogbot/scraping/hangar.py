﻿import util
from mechanize import Browser
from bs4 import BeautifulSoup
import re
import logging
from scraper import *


class Hangar(Scraper):
    def get_ships(self, planet):
        self.logger.info('Getting shipyard data for planet %s' % planet)
        url = self.url_provider.get_page_url('shipyard', planet)
        res = self.open_url(url)
        soup = BeautifulSoup(res.read(), "lxml")
        refs = soup.findAll("span", { "class" : "textlabel" })

        ships = []
        for ref in refs:
            if ref.parent['class'] == ['level']:
                aux = ref.parent.text.replace('\t','')
                ship_raw_data = re.sub('  +', '', aux).encode('utf8')
                ship_id = ref.parent.parent.parent['ref']
                ship_data = ship_raw_data.split('\n');
                ship_data.append(ship_id)
                ships.append( tuple(ship_data) )

        ships = map(tuple, map(scraper.sanitize, [filter(None, i) for i in ships]))
        return [Ship(ship[0], ship[2], ship[1]) for ship in ships]



