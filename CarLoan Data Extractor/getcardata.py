from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import time, math, random, string

store_data = MongoClient('mongodb://localhost:27017')['cardata']['india_user']

initial_link = 'http://cars.indian.net.in/'

first_requests = requests.get(initial_link)


def unique_id_gen(prefix='', more_entropy=False):
    m = time.time()
    unique_id = '%8x%05x' % (math.floor(m), (m - math.floor(m)) * 1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0, 10, 1):
            entropy_string += random.choice(valid_chars)
        unique_id = unique_id + entropy_string
    unique_id = prefix + unique_id
    return unique_id

data = first_requests.text
soup = BeautifulSoup(data, 'html.parser')

product_url = soup.find_all('li', {'class', "list-group-item"})

for url_data in product_url:
    car_url = 'http://cars.indian.net.in' + url_data.find('a')['href']

    try:
        first_requests = requests.get(car_url)
        data = first_requests.text
        soup = BeautifulSoup(data, 'html.parser')
        div = soup.find('table', {'id': "dgData"})
        ps = div.find_all('tr')

        count = 0
        dict_cars = {}
        header_dict = {}
        for p in ps:
            each_cell = p.find_all('td')
            for index, cell in enumerate(each_cell):
                if count == 0:
                    header_dict[index] = cell.text
                    dict_cars[cell.text] = {}
                else:
                    dict_cars[header_dict[index]] = cell.text
                try:
                    if count > 0:
                        store_data.insert_one(dict_cars)
                except Exception as e:
                    dict_cars['_id'] = unique_id_gen()
                    inserted_data = store_data.insert_one(dict_cars)
                count += 1
                print(dict_cars)
                time.sleep(20)
    except Exception as e:
            pass