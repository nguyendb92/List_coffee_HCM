from requests_html import HTMLSession
import os
import time
import json

api_key = os.environ.get('api_key')
location = '&location=10.779614,106.699256'
radius = '&radius=5000'
type = '&type=cafe'
key = '&key={}'.format(api_key)
query = 'query=coffee'
link = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
tokens = '{}{}{}{}{}{}'.format(link, query, location, radius, type, key)

session = HTMLSession()
resp = session.get(tokens)
data = resp.json()

next_token = link + 'pagetoken={}' + key
fina_data = [dic['name'] for dic in data['results']]
print(next_token.format(data['next_page_token']))
while 'next_page_token' in data:
        try:
            resp = session.get(next_token.format(data['next_page_token']))
            data = resp.json()
            print(data['next_page_token'])
            fina_data.extend([name['name'] for name in data['results']])
            time.sleep(10)
        except KeyError:
            break


with open('coffee.json', 'wt', encoding='utf-8') as f:
    coffee_json = json.jumps(fina_data[:50])
    f.write(coffee_json)
