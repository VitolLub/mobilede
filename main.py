#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__      = "Lubomir Vitol"
__copyright__   = "Copyright 2022, Planet Earth"

import requests
import json
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import random
import time

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

    def proxies(self):
        proxy = ["177.104.125.173:55443","45.79.230.234:80","43.224.10.11:6666","195.91.221.230:55443","185.142.67.23:8080","185.34.22.225:37879","123.231.221.242:6969"]

        # random number
        r = random.randint(0,len(proxy)-1)
        return {"http":proxy[r]}

    def generate_ref_id(self):
        # generate ref id = eed68f73-d54f-1c19-6009-ba50697b11fc
        ref_id = ""
        for i in range(0,8):
            ref_id += random.choice("0123456789abcdefghijklmnopqrstuvwxyz")
        ref_id += "-"
        for i in range(0,4):
            ref_id += random.choice("0123456789abcdefghijklmnopqrstuvwxyz")
        ref_id += "-"
        for i in range(0,4):
            ref_id += random.choice("0123456789abcdefghijklmnopqrstuvwxyz")
        ref_id += "-"
        for i in range(0,4):
            ref_id += random.choice("0123456789abcdefghijklmnopqrstuvwxyz")
        ref_id += "-"
        for i in range(0,12):
            ref_id += random.choice("0123456789abcdefghijklmnopqrstuvwxyz")
        return ref_id


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
        r = requests.get(url, timeout=20, headers=header, cookies=self.cookie) #, proxies=proxies
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


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        db = MongoClient('mongodb+srv://vitol:vitol486070920@ebay.elcsu.mongodb.net/test?retryWrites=true&w=majority')
        db = db['pc_scrap_data']
        return db

    def insert_data(self,car_id):
        db = self.connect()
        db = db['car_id']
        print(car_id)
        try:
            print(db.find_one({'car_id': car_id}))
            # check if car_id is already in database
            if db.find_one({'car_id':car_id}) is None:

                db.insert_one({'car_id': car_id, 'sold': False, 'check': False})
            #db.update_one({'car_id':car_id}, {'$set':car_id}, upsert=True)
        except:
            pass





class GbabMain:
    def __init__(self):
        self.url = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0&isSearchRequest=true"
        self.rest_of_url = "&ref=srp&s=Car&sfmr=false&vc=Car"
        self.cookie = Helper().cookie()
        self.header = Helper().header()
        self.proxies = Helper().proxies()
        self.db = Database().connect()
        self.db_functions = Database()
        self.page_param = "&pageNumber="

    def make_request(self,param,page=1,sub_param=None,url_type=0):
        # generate refId
        ref_id = Helper().generate_ref_id()
        print(f"sub_param : {sub_param}")
        if sub_param == None:
            sub_param_origin = ''
        if sub_param != None:
            sub_param_origin = "%3B"+str(sub_param)
        # params = auto model

        # make request by ulr

        session = requests.Session()
        session.cookies.set('Host', 'mobile.de', domain='.mobile.de', path='/')
        session.cookies.set('region', 'US', domain='.mobile.de', path='/')
        #ul = "https://suchen.mobile.de/fahrzeuge/search.html?dam=0&isSearchRequest=true&ms=1100&ref=srp&s=Car&sfmr=false&vc=Car&pageNumber=1"
        #self.url+str(param)+";"+str(sub_param)+"&pageNumber="+str(page)
        #+";"+str(sub_param)
        if url_type == 0:
            r = session.get(self.url+"&ms="+str(param)+sub_param_origin+"&pageNumber="+str(page)+self.rest_of_url, timeout=20, headers=self.header, cookies=self.cookie ) #, proxies=self.proxies
            print(self.url + "&ms=" + str(param) + sub_param_origin + "&pageNumber=" + str(page) + self.rest_of_url)

        if url_type == 1:
            url = f'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&makeModelVariant1.makeId={str(param)+sub_param_origin}&pageNumber={str(page)}&ref=srpNextPage&refId={ref_id}&scopeId=C&sfmr=false'
            print(url)
            r = session.get(url,
                timeout=20, headers=self.header, cookies=self.cookie)
            #print(r.content)
        return r.content

    def parse_data(self,param):
        data = self.make_request(param)

        soup = BeautifulSoup(data, 'html.parser')

        # get ItemId's from first page
        try:
            self.get_item_ids(soup)
        except Exception as e:
            raise e

        # get hit counter
        hit_counter = self.hit_counder(soup).replace('.','')
        print(hit_counter)
        range_loop = int(hit_counter) / 20
        range_loop = round(range_loop) - 1
        print(f"page count {range_loop}")
        if hit_counter != None:
            if range_loop >= 50:

                for sub_param in range(1,200):
                    for page in range(1,range_loop):
                        url_type = 1
                        data = self.make_request(param,page,sub_param,url_type)
                        self.get_item_ids2(data)
            else:
                print('parse2')
                # parse by main categories
                # page by page
                for page in range(2, range_loop):
                    print(page)
                    url_type = 1
                    data = self.make_request(param, page, None, url_type)
                    self.get_item_ids2(data)

    def hit_counder(self, soup):
        # find span by class hit-counter
        print('hit_counder')
        try:
            span = soup.find('span', {'class':'hit-counter'})
            print(span.text)
            return span.text
        except Exception as e:
            return None

    def get_item_ids(self, soup):

        # find class cBox cBox--content cBox--resultList
        div = soup.find('div', {'class':'cBox cBox--content cBox--resultList'}) #cBox cBox--content cBox--resultList

        # find all a with class link--muted no--text--decoration result-item
        elem = div.find_all('a', {'class':'link--muted no--text--decoration result-item'})
        for i in elem:
            # get href
            car_id = i['data-ad-id']

            # sae in db
            self.db_functions.insert_data(car_id)

    def get_item_ids2(self, data):
        #print(data)
        soup = BeautifulSoup(data, 'html.parser')
        # # find class cBox cBox--content cBox--resultList
        # div = soup.find('div', {'class':'cBox cBox--content cBox--resultList '})  # cBox cBox--content cBox--resultList
        # print(div)
        # find all a with class link--muted no--text--decoration result-item
        elem = soup.find_all('a', {'class':'link--muted no--text--decoration result-item'})
        for i in elem:
            # get href
            car_id = i['data-ad-id']

            # sae in db
            self.db_functions.insert_data(car_id)


if __name__ == '__main__':
    res = GbabMain()
    models_arr = [1400,25650,113,25300,25100,25200,24500,24400,24200,24100,135,189,23825,23800,23600,23500,23100,100,188,
                  23000,22900,22500,22000,21800,125,21700,21600,20700,20200,20100,20000,4,19800,19600,19300,
                  149,19000,18975,18875,18700,17900,17700,17500,30011,17300,17200,137,16800,16700,16600,15900,16200,
                  15500,15400,15200,14845,14800,14700,14600,14400,13900,13450,13450,12600,12400,12100,11900,11650,11600,
                  11050,11000,10850,186,122,9900,204,205,9000,8800,172,8800,8600,235,255,7700,31864,7400,7000,6800,6600,3,
                  6325,6200,5900,5700,5600,83,5300,112,4700,4400,3500,375]

    for param in models_arr:
        print(param)
        res.parse_data(param)






