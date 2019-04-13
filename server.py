#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import urllib2, json, sys, re
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

class WordCount(Resource):

    def parse(self):
        """
        This function opens the webpage given in the request.json, scrapes
        the text from it, then extracts only the text visible to the user.
        """
        self.request = sys.argv[1] # request json is passed in at command line
        print(self.request)
        with open(self.request, 'r') as infile:
            page_dict = json.load(infile)
        self.url = page_dict["url"]
        self.word = page_dict["word"]
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup(page, 'html.parser')
        [s.extract() for s in soup(['style', 'script', 'head', 'title', 'meta', '[document]'])] # remove non-visible text
        self.visible_text = soup.get_text(separator=' ') # add space between individual words (to be removed later)

    def counter(self):
        """
        This function takes the visible text as defined in the parse function,
        then separates it into individual words, and then compares those tokens
        to the desired word for the count.
        """
        words = re.findall(r"[\w']+", self.visible_text) # split by regex
        words = [word.encode('ascii', 'ignore') for word in words] # remove unicode stuff
        self.count = 0
        for word in words:
            if word.lower() == self.word:
                self.count += 1

    def get(self):
        """
        This function produces the json file that the API gets. If it runs into
        any errors during parse or counter(), it returns a fail result. Else,
        it returns a json file with what it believes to be the word count.
        """
        try:
            self.parse()
            self.counter()
        except:
            self.response = {'status':'fail', 'count':''}
            return self.response
        self.response = {'status':'ok', 'count':self.count}
        return self.response


api.add_resource(WordCount, '/wordcount') # Route_1

if __name__ == '__main__':
    app.run(port='5002')
