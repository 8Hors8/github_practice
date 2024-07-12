import pprint

import requests

url = 'https://httpbin.org/get'
r = requests.get('https://netology.ru/')
print(r.text)