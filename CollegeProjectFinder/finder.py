#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import textwrap

import requests
from colorama import init, Fore, Style

import common
import terminalsize


def main():
    sizex, sizey = terminalsize.get_terminal_size()
    init(autoreset=True)
    color = True
    numb = 1
    common.start()
    parameters = {'sort': 'stars', 'order': 'desc'}
    topic = common.ask('What topic would you want your project in? Eg. AI, Machine Learning, Image Processing?',
               answer=common.str_compat, default="Machine Learning")
    language = common.ask('Any specific language?', answer=common.str_compat, default=" ")
    if topic:
        search_term = 'topic:' + topic
    if language.strip():
        search_term += ' language:' + language.strip()
    parameters['q'] = search_term

    project_request = requests.get('https://api.github.com/search/repositories', params=parameters).json()
    if 'items' in project_request:
        git_details = project_request['items']
        for project in git_details:
            if color:
                prefix = Fore.RED + Style.BRIGHT + '*' * (sizex / 4)
            else:
                prefix = Fore.MAGENTA + Style.BRIGHT + '*' * (sizex / 4)
            wrapper = textwrap.TextWrapper(initial_indent=prefix, width=sizex, subsequent_indent='    ')
            print wrapper.fill('*' * (sizex / 4))
            print('{} . Project Name: {}'.format(str(numb), project['name']))
            print('-' * (sizex / 8))
            print('Project Description: \n%s' % project['description'])
            print('-' * (sizex / 8))
            print('Project Url: %s' % project['html_url'])

            color = not color
            numb += 1
    print('\n\n')
    clone_index = common.ask('Select one of the Projects to clone. Enter index. Eg. 1 for first',
                             answer=list, default="1", options=range(1, len(git_details)))
    clone_path = common.ask('Path to clone? Leave blank if same path.', answer=common.str_compat, default=' ')
    if subprocess.check_call('git --version', shell=True) != 0:
        print('git not installed installed, please read link ' +
              'https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.')
        exit()
    else:
        clone_url = git_details[int(clone_index)]['clone_url']
        command = 'git clone ' + clone_url
        if clone_path.strip():
            if os.path.isdir(clone_path):
                command += ' ' + clone_path
        print('Cloning..')
        subprocess.check_call(command, shell=True)


if __name__ == "__main__":
    main()