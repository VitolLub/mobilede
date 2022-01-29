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
        try:
            # insert or update
            db.update_one({'car_id':car_id}, {'$set':car_id}, upsert=True)
        except:
            db.insert_one({'car_id':car_id,'sold':False})


    # get first 100 records from database
    def get_data(self):
        db = self.connect()
        db = db['car_id']
        try:
            # get first 100 records
            data = db.find({'check':False}).limit(5)
            return data
        except:
            return None

    def update_test(self):
        db = self.connect()
        db = db['car_id']
        try:
            # update all records
            db.update_many({}, {'$set':{'check':False}})
        except:
            return None

    # update data if sold
    def update_data(self,car_id):
        db = self.connect()
        db = db['car_id']
        try:
            # update
            db.update_one({'car_id':str(car_id)}, {'$set':{'sold':True}})
        except:
            pass

    def save_car_posts(self,car_id,posts):
        db = self.connect()
        db = db['car_posts']
        try:
            # insert or update
            db.update_one({'car_id':car_id}, {'$set':posts}, upsert=True)
        except:
            db.insert_one({'car_id':car_id,'posts':posts})

    def inser_all(self, arr):
        # insert many
        db = self.connect()
        db = db['car_posts']
        try:
            db.insert_many(arr)
        except:
            pass

    def update_data_check(self, param):
        db = self.connect()
        db = db['car_id']
        try:
            # update
            db.update_one({'car_id': str(param)}, {'$set': {'check': True}})
        except:
            pass


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
        r = requests.get(url, timeout=10, headers=header, cookies=self.cookie) #, proxies=proxies
        #print(r.content)
        return r.content

    # parse data from mobile.de
    def parse_data(self,arr):

        data = self.make_request()
        soup = BeautifulSoup(data, 'html.parser')
        element_dict = {}

        #print(soup)
        if self.get_values(soup,element_dict) != 0:
            element_dict['ad_title'] = self.get_title(soup)
            element_dict['price'] = self.get_price(soup)
            element_dict['car_id'] = self.id
            element_dict['features'] = self.get_features(soup)
            arr.append(element_dict)
            return True
        if self.get_values(soup,element_dict) == 0:
            db = Database()
            db.update_data(self.id)
            return False



    def get_values(self,soup,element_dict):
        # find div by id td-box
        div = soup.find('div', {'id':'td-box'})
        print(div)
        #print(div)
        # find all divs with class g-row u-margin-bottom-9
        try:
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
        except:
            # update sold status in db
            return None



    def get_title(self,soup):
        try:
            title = soup.find('h1', {'id':'ad-title'})
            return title.text
        except:
            pass

    def get_price(self,soup):
        try:
            price = soup.find('span', {'data-testid': 'prime-price'})
            # replace \xa0
            return price.text.replace('\xa0',' ')
        except:
            pass

    def get_features(self, soup):
        element_arr = []
        try:
            # find div by id features
            div = soup.find('div', {'id':'features'})

            #find all divs with class g-col-6
            elem = div.find_all('div', {'class':'g-col-6'})

            for i in elem:
                text = i.text
                element_arr.append(text.strip())
        except Exception as e:
            pass

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

class Origin:

    def make_request(self):
        db = Database()


        fir_100 = db.get_data()
        for le in fir_100:
            arr = []
            print(le)
            r = Request_by_id(le['car_id'])
            res = r.parse_data(arr)
            if res == True:
                db.update_data(le['car_id'])
                print('updated')
                print(arr)
                db.inser_all(arr)

                # set True if check
                db.update_data_check(le['car_id'])
        self.make_request()

if __name__ == '__main__':
    stat = Origin()
    stat.make_request()

