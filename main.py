#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Lubomir Vitol"
__copyright__   = "Copyright 2022, Planet Earth"

import requests
import json
from bs4 import BeautifulSoup
import re

"""

    This is the main file of the project.
    It contains the main function and the main loop.
    Parse data from mobile.de and save in json
    
"""


params = {"Schadstoffklasse":"emission_class","Preis":"price","Kategorie":"", "Leistung":"hp","Kraftstoffart":"fuel_type","Anzahl Sitzplätze":"number_of_seats","Anzahl der Türen":"number_of_doors","Getriebe":"gearbox",
                       "Erstzulassung":"Initial registration","Anzahl der Fahrzeughalter":"Number of vehicle owners","HU":"Main inspection","Klimatisierung":"Air conditioning",
                       "Einparkhilfe":"Parking assistance","Airbags":"Airbags","Farbe (Hersteller)":"color_manufacturer",
                       "Farbe":"color","Innenausstattung":"interior"
                       }
arr = []
class Helper:
    def cookie(self):
        cookies = {
            '__gads': 'ID=1520b794fe127d46:T=1643188159:S=ALNI_MbyWcRxZEA29CVGk1t_y4QY8CAMew',
            '_abck': '1742DD56712AE08182DA0AFEDF7A2C17~0~YAAQRggQAgAPCXN+AQAA/FA5lwe97mLvvdLS+4ffbY+oz01dAeMU9H8BJkZv0gwU/ce3b+6cAiakFuxaRqG2b/QKXXBl7GS0ct40nxWXxypIoG1//cMaUrKN2YMvuxTpAsJjpHgAx9/ixcPLO676wyNcclLb+jBbIxXXVCuACXHm5fyRvdB6AgW+5RRe20M1vLkzEH8SBbAEZG99OtFFiu08o6/DZJbdrcROxqf6x7oKyM3hjCXeKwE7JIsPjFCVQvGEJbJoNAiYDsQR3SoevaxJ2Y3TVJgJ8PFkBPjoJSzyz+wxpAM/kCdvWkFCDbNLouipewYy35ziKAtldsxtANzR5OpxMF6D4a52ElhdFlrOH165DWYzo35DZOzNaoPv1AAdVED4qpfLHJL0GRi2bovklTjzycA=~-1~-1~-1',
            '_clck': '13mnxd0|1|eyg|0',
            '_clsk': '1i5ql6m|1643192652219|3|0|h.clarity.ms/collect',
            '_fbp': 'fb.1.1643190455664.287716889',
        }
        return cookies

    def header(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        return header

    def proxyes(self):
        pass

class Request_by_id:

    def __init__(self, id):
        self.id = id
        self.params = {"Schadstoffklasse":"emission_class","Preis":"price","Kategorie":"category", "Leistung":"hp","Kraftstoffart":"fuel_type","Anzahl Sitzplätze":"number_of_seats","Anzahl der Türen":"number_of_doors","Getriebe":"gearbox",
                       "Erstzulassung":"Initial registration","Anzahl der Fahrzeughalter":"Number of vehicle owners","HU":"Main inspection","Klimatisierung":"Air conditioning",
                       "Einparkhilfe":"Parking assistance","Airbags":"Airbags","Farbe (Hersteller)":"color_manufacturer",
                       "Farbe":"color","Innenausstattung":"interior"
                       }
        self.cookie = Helper().cookie()

    def make_request(self):
        #url = f"https://suchen.mobile.de/fahrzeuge/details.html?id={str(self.id)}&damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&makeModelVariant1.makeId=1900&makeModelVariant1.modelId=9&pageNumber=1&ref=quickSearch&scopeId=C&sfmr=false&fnai=prev&searchId=2f5045cf-c8d4-a09e-056f-051ab33794cc"
        url = f"https://suchen.mobile.de/auto-inserat/seat-alhambra-2-0tdi-style-xenon-7-sitze-alu-tempomat-sonnefeld-gestungshausen/{str(self.id)}.html"
        print(url)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

        proxies = {'http':'150.129.148.99:35101'}
        r = requests.get(url, timeout=20, headers=header, cookies=self.cookie, proxies=proxies)
        #print(r.content)
        return r.content

    # parse data from mobile.de
    def parse_data(self):
        data = self.make_request()
        soup = BeautifulSoup(data, 'html.parser')
        element_dict = {}

        #print(soup)
        self.get_values(soup,element_dict)
        element_dict['ad_title'] = self.get_title(soup)
        element_dict['price'] = self.get_price(soup)
        element_dict['features'] = self.get_features(soup)
        arr.append(element_dict)



    def get_values(self,soup,element_dict):
        # find div by id td-box
        div = soup.find('div', {'id':'td-box'})
        #print(div)
        # find all divs with class g-row u-margin-bottom-9
        elem = div.find_all('div', {'class':'g-row u-margin-bottom-9'})

        for i in elem:
            el = i.find_all('div', {'class':'g-col-6'})
            for index,j in enumerate(el):
                text = j.text
                #print(text.strip())
                if text.strip() in self.params:
                    #print('yes')
                    #print(el[1].text.strip())
                    res = re.sub('[^A-Za-z0-9]+', '', el[1].text.strip())
                    element_dict[self.params[text.strip()]] = res


    def get_title(self,soup):
        title = soup.find('h1', {'id':'ad-title'})
        return title.text

    def get_price(self,soup):
        price = soup.find('span', {'data-testid': 'prime-price'})
        # replace \xa0
        return price.text.replace('\xa0',' ')

    def get_features(self, soup):
        # find div by id features
        div = soup.find('div', {'id':'features'})

        #find all divs with class g-col-6
        elem = div.find_all('div', {'class':'g-col-6'})
        element_arr = []
        for i in elem:
            text = i.text
            element_arr.append(text.strip())

        return element_arr

    def get_starts(self,soup):
        # find div by id td-box
        start = soup.find('span', {'class':'star-rating-s u-valign-middle u-margin-right-9'})
        # get attribute data-rating
        return start['data-rating']

    def get_company_name(self,soup):
        # get company name by class h3 seller-title__inner
        company = soup.find('div', {'class':'h3 seller-title__inner'})
        return company.text

    def get_description(self,soup):
        # get description by class cBox-body cBox-body--vehicledescription
        pass


class GbabMain:
    def __init__(self):
        self.url = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0&isSearchRequest=true&ref=quickSearch&sfmr=false&vc=Car&ms="
        self.cookie = Helper().cookie()
        self.header = Helper().header()

    def make_request(self):
        # params = auto model
        param = "3500"

        # make request by ulr
        r = requests.get(self.url+param, timeout=20, headers=self.header, cookies=self.cookie)
        print(r.content)

    def parse_data(self):
        data = self.make_request()

        soup = BeautifulSoup(data, 'html.parser')

        # get hit counter
        self.hit_counder(soup)

    def hit_counder(self, soup):
        pass


if __name__ == '__main__':
    res = GbabMain()
    res.make_request()

    # elments_ids = [338014347,336291920,338349571,336300676]
    # for le in elments_ids:
    #     r = Request_by_id(le)
    #     r.parse_data()
    #
    # # save to json
    # with open('data.txt', 'w') as outfile:
    #     json.dump(arr, outfile)



