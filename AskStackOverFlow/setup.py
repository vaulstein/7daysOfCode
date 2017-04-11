#!/usr/bin/python

import sys
import os
import askquora

if sys.version_info > (3,0):
        sys.exit("AskQuora requires python 2.")

from setuptools import setup, find_packages

setup(name='AskStackOverFlow',
      version='0.1',
      description='StackOverFlow Q&A right from the command line! Inspiration from Ritesh M',
      author='Vaulstein Rodrigues',
      author_email='vaulstein@gmail.com',
      packages = find_packages(),
      entry_points={
            'console_scripts': [
                  'askstackoverflow = askstackoverflow.askstackoverflow:cli',
            ]
      },
      url='https://www.github.com/Vaulstein/7daysOfCode',
      keywords=['stackoverflow', 'terminal', 'command-line', 'question', 'python'],
      license='MIT',
      classifiers=[],
      install_requires=[
            'requests',
            'BeautifulSoup4',
            'colorama',
            'requests-cache'
      ]
     )