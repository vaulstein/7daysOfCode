#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common
import requests

def main():
    common.start()
    parameters = {'sort': 'stars', 'order': 'desc'}
    topic = common.ask('What topic would you want your project in? Eg. AI, Machine Learning, Image Processing?',
               answer=common.str_compat, default="Machine Learning")
    language = common.ask('Any specific language?', answer=common.str_compat, default=" ")
    if topic:
        search_term = topic
    if language.strip():
        search_term += ' ' + language.strip()
    parameters['q'] = search_term

    r = requests.get('https://api.github.com/search/repositories', params=parameters).json()


if __name__ == "__main__":
    main()