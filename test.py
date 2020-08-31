from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from io import BytesIO
import requests
import os
from pathlib import Path
import sys

import random
import string

import re

agreement = ["y", "yes", "ja", "j"]

class Scraper:
    def __init__(self, directory=None, url=None):
        if not Path(directory).is_dir():
            os.makedirs(directory)

        self.tag = 'a'
        self.classes = 'fileThumb'
        self.should_download = True

        setQuery = input("Set query selector? (y/n)")
        if setQuery in agreement:
            self.set_query_selector()

    def run(self):
        self.elements = []

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=url, headers=headers) 
        response = urlopen(req).read() 

        self.soup = BeautifulSoup(response, 'html.parser')
        self.elements = self.soup.find_all(self.tag, {"class": self.classes})

        if len(self.elements) == 0:
            print("No elements on the page found that are conform the query selector.")
            
        for element in self.elements:
            imageUrl = element['href']
            if not imageUrl.startswith('http'):
                link = 'http:' + imageUrl
                file_name = link.split('/')[-1]

            if self.should_download:
                self.download(element)
            else:
                print("Found: {} ({}/{}) ".format(file_name, self.elements.index(element) + 1, len(self.elements) ) )

    def download(self, file_name, element):
        file_name = link.split('/')[-1]
        print("downloading: {} ({}/{}) ".format(file_name, self.elements.index(element) + 1, len(self.elements) ) )
        response = requests.get(link)
        f = open(directory + '/' + file_name, 'wb+')
        f.write(response.content)
        f.close()

    def set_query_selector(self):
        while true:
            query = input("Set your query selector (I.E: tag.first-class.other-class):")

            self.tag = re.search(r'\w+', query).group(0)
            self.classes = re.findall(r'(?<=\.)\w+', query)
            self.ids = re.findall(r'(?<=\#)\w+', query)
            self.should_download = True

            print("tag = {}\nclasses = {}\n ids = {}".format(self.tag, self.classes, self.ids))
            should_redo = input("Is this correct: (y/n)")
            if should_redo in agreement:
                break


def start(script_name=None, url=None, save_location=None, third=None, fourth=None):
        if url is None:
            url = input("please pass a valid url ~>")

        if save_location is None:
            save_location = get_random_string(8)
            print("saving in: " + save_location)

        scraper = Scraper(save_location, url)
        scraper.run()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == "__main__":
    start( *sys.argv)
    