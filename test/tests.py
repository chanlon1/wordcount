from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import unittest, sys, os
sys.path.append(os.path.abspath("/home/clare/testAPI"))
from wordcount import *


# Basic string tests to make sure nothing has gone horribly wrong.
class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

# Various tests for the parse method of the WordCounter class.
class TestParse(unittest.TestCase):

    # Makes sure that parse correctly parses a short amount of text.
    def test_small(self):
        counter = WordCounter()
        request = "data/smalltext.json"
        text, token = counter.parse(request)
        text = text.encode('ascii', 'ignore')
        self.assertEqual(text, "This page intentionally left blank")
        self.assertEqual(token, "left")

    # Makes sure that parse is able to parse lots of text.
    def test_long(self):
        counter = WordCounter()
        request = "data/longtext.json"
        text, token = counter.parse(request)
        text = text.encode('ascii', 'ignore')
        self.assertIsNotNone(text)
        self.assertEqual(token, "Yemen")

    # Makes sure that parse throws out a bad json file.
    def test_badjson(self):
        # Makes sure that
        counter = WordCounter()
        request = "data/badjson.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse throws out a bad json file.
    def test_badjson2(self):
        counter = WordCounter()
        request = "data/badjson2.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse throws out a bad json file.
    def test_badjson3(self):
        counter = WordCounter()
        request = "data/badjson3.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse complains when given an empty json file.
    def test_emptyjson(self):
        counter = WordCounter()
        request = "data/emptyjson.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse complains when given a non-functional URL.
    def test_badurl(self):
        counter = WordCounter()
        request = "data/badurl.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse complains when not given a URL.
    def test_nourl(self):
        counter = WordCounter()
        request = "data/nourl.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse complains when not given a token.
    def test_notoken(self):
        counter = WordCounter()
        request = "data/notoken.json"
        with self.assertRaises(Exception):
            counter.parse(request)

    # Makes sure that parse complains when it can't find any text
    # from the given URL. (A design choice.)
    def test_notext(self):
        counter = WordCounter()
        request = "data/notext.json"
        with self.assertRaises(Exception):
            counter.parse(request)

# Skips parse and goes directly to counter to test it.
class TestCountDirect(unittest.TestCase):

    # Makes sure that counter correctly counts a present token.
    def test_tokenpresent(self):
        counter = WordCounter()
        text = "a bc abc ab cb abc cb b cb cbcb ab"
        token = "cb"
        count = counter.count(text, token)
        self.assertEqual(count, 3)

    # Makes sure that counter correctly counts an absent token.
    def test_tokenabsent(self):
        counter = WordCounter()
        text = "a bc abc ab cb abc cb b cb cbcb ab"
        token = "ef"
        count = counter.count(text, token)
        self.assertEqual(count, 0)

    # Makes sure that counter complains when given a non-string token.
    def test_badtoken(self):
        counter = WordCounter()
        with self.assertRaises(Exception):
            count = counter.count("text", 1)

    # Makes sure that counter complains when given non-string text.
    def test_badtext(self):
        counter = WordCounter()
        with self.assertRaises(Exception):
            count = counter.count(1, "token")

class TestCountJSON(unittest.TestCase):

    # Makes sure that counter correctly counts a present token.
    # (Test from assignment PDF)
    def test_basic(self):
        counter = WordCounter()
        request = "data/basic.json"
        text, token = counter.parse(request)
        count = counter.count(text, token)
        self.assertEqual(count, 10)

    # Makes sure that counter correctly counts an absent token.
    def test_absenttoken(self):
        counter = WordCounter()
        request = "data/absenttoken.json"
        text, token = counter.parse(request)
        count = counter.count(text, token)
        self.assertEqual(count, 0)

    # Makes sure that counter correctly counts text small enough to hand-check.
    def test_small(self):
        counter = WordCounter()
        request = "data/smalltext.json"
        text, token = counter.parse(request)
        count = counter.count(text, token)
        self.assertEqual(count, 1)

    # Makes sure that counter correctly counts a short amount of text (although
    # too long to hand-check).
    def test_long(self):
        counter = WordCounter()
        request = "data/longtext.json"
        text, token = counter.parse(request)
        count = counter.count(text, token)
        self.assertIsNotNone(count)

    # Makes sure that counter returns a number equal to what Chrome's find
    # feature calculates (whole word, case-sensitive).
    def test_pythondocs(self):
        counter = WordCounter()
        request = "data/pythondocs.json"
        text, token = counter.parse(request)
        count = counter.count(text, token)
        self.assertEqual(count, 9)

"""
I was going to test get, but I don't know enough about how APIs work to call
them directly from Python.

#class TestGet(unittest.TestCase):
"""


if __name__ == '__main__':
    unittest.main()
