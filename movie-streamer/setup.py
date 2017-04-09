
from setuptools import setup

setup(name="mstream",
	  version="0.1",
	  description="Instantly stream movies/ tv episodes you want to watch",
	  url="http://vaulstein.github.com",
	  author="Vaulstein Rodrigues",
	  author_email="vaulstein@gmail.com",
	  license='MIT',
	  packages=["mstream"],
	  scripts=["bin/mstream"],
	  install_requires=[
		  'BeautifulSoup4',
		  'requests'],
	  zip_safe=False)