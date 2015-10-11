#!/usr/bin/python

import requests
import sys
from bs4 import BeautifulSoup
import argparse


class GeneralResource:
    def __init__(self, url):
        self.url = url
        self.data = ""
        self.text = ""
        self.img_src = ""
        self.title = ""
        self.soup = None
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/45.0.2454.101 Safari/537.36'}

    def __str__(self):
        return self.url

    def print_result(self):
        print self.title + "\n"
        print self.img_src + "\n"
        print self.text

    def process_url(self):
        self.get_data_from_url()
        self.get_title_from_data()
        self.get_text_from_data()
        self.get_imgsrc_from_data()


    def get_data_from_url(self):
        r = requests.get(self.url, headers=self.headers)

        if r.status_code == 200:
            self.data = r.text
            self.soup = BeautifulSoup(self.data, 'html.parser')


class Xakep(GeneralResource):
    def get_text_from_data(self):
        result = self.soup.find(id="content-anchor-inner")

        self.text = result.get_text()

    def get_title_from_data(self):
        self.title = self.soup.title.string

    def get_imgsrc_from_data(self):
        result = self.soup.find_all('img')

        self.img_src = result[0]['src']


class Opennet(GeneralResource):
    def get_text_from_data(self):
        result = self.soup.find(id="r_memo")

        self.text = result.get_text()

    def get_title_from_data(self):
         self.title = self.soup.title.string       
        
    def get_imgsrc_from_data(self):
        element = self.soup.find(id="r_memo")
        result = element.find_all('img')

        self.img_src = result[0]['src']


class Geektimes(GeneralResource):
    def get_text_from_data(self):
        self.post_number = self.url.split('/')[-2]
        result = self.soup.find(id="post_%s" % self.post_number)

        self.text = result.get_text()

    def get_title_from_data(self):
         self.title = self.soup.title.string       
        
    def get_imgsrc_from_data(self):
        element = self.soup.find(id="post_%s" % self.post_number)
        result = element.find_all('img')

        self.img_src = result[0]['src']


class Habrahabr(GeneralResource):
    def get_text_from_data(self):
        self.post_number = self.url.split('/')[-2]
        result = self.soup.find(id="post_%s" % self.post_number)

        self.text = result.get_text()

    def get_title_from_data(self):
         self.title = self.soup.title.string       
        
    def get_imgsrc_from_data(self):
        element = self.soup.find(id="post_%s" % self.post_number)
        result = element.find_all('img')

        self.img_src = result[0]['src']

def get_object(url):
    if 'http' not in url:
        print "Provide schema http or https"
        sys.exit(2)

    if 'geektimes.ru' in url:
        return Geektimes(url)
    elif 'habrahabr.ru' in url:
        return Habrahabr(url)
    elif 'xakep.ru' in url:
        return Xakep(url)
    elif 'opennet.ru' in url:
        return Opennet(url)
    else:
        print "Unknow domain, sorry"
        sys.exit(3)

def get_args():
    parser = argparse.ArgumentParser(description="Get data from url")
    parser.add_argument("url", type=str, help="URL for parsing")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    pr = get_object(args.url)
    pr.process_url()
    pr.print_result()


if __name__ == '__main__':
    main()
