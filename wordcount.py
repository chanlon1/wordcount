#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import urllib2, json, sys, re
from bs4 import BeautifulSoup

"""
Clare Hanlon
April 14th, 2019
A word-counting API for Virtusize.
"""

app = Flask(__name__)
api = Api(app)

"""
This class takes care of parsing and counting. It's separate from the API
itself to make testing easier.
"""
class WordCounter:

    """
    This function opens the webpage given in the request.json, scrapes
    the text from it, then extracts only the text visible to the user.
    It takes the name of a json file as input and returns all visible text
    as output.
    """
    def parse(self, request):
        with open(request, 'r') as infile:
            page_dict = json.load(infile)
        url = page_dict["url"]
        word = page_dict["word"]
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        [s.extract() for s in soup(['style', 'script', 'head', 'title', 'meta', '[document]'])] # remove non-visible text
        visible_text = soup.get_text(separator=' ') # add space between individual words (to be removed later)
        visible_text = visible_text.strip() # remove newlines (to make testing easier)
        return visible_text, word

    """
    NOTE: token comparison is case-sensitive.
    This function takes the visible text as defined in the parse function,
    then separates it into individual words, and then compares those tokens
    to the desired word for the count.
    It has two parameters - the string to search through, and the token
    to search that text for. Both are expected to be strings, and the function
    will throw an error if they are not.
    """
    def count(self, text, token):
        if not isinstance(text, basestring):
            raise Exception("Invalid text provided.")
        if not isinstance(token, basestring):
            raise Exception("Invalid token provided.")

        words = re.findall(r"[\w']+", text) # split by regex
        words = [word.encode('ascii', 'ignore') for word in words] # remove unicode stuff
        count = 0
        for word in words:
            if word == token:
                count += 1
        return count

"""
This class consitutes the actual API. It's separate from the word-counting
process itself to make testing easier.
"""
class WordCounterAPI(Resource):

    """
    This function produces the json file that the API gets. If it runs into
    any errors during parse or counter(), it returns a fail result. Else,
    it returns a json file with what it believes to be the word count.
    """
    def get(self):
        if len(sys.argv) < 2:
            e = "FAIL - No data file provided."
            response = {'status':e, 'count':''}
            return response
        request = sys.argv[1] # request json is passed in at command line
        counter = WordCounter()

        try:
            text, token = counter.parse(request)
            count = counter.count(text, token)
        except:
            e = 'FAIL: ' + str(sys.exc_info()[0])
            response = {'status':e, 'count':''}
            return response

        response = {'status':'OK', 'count':count}
        return response


api.add_resource(WordCounterAPI, '/wordcount')

if __name__ == '__main__':
    app.run(port='5002')
