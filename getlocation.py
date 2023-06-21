import requests
import json
import pandas as pd


def coords(city):
    url = 'https://restapi.amap.com/v3/geocode/geo'

    params = {'key': '2fed3cca3e8ac9bdbbb76de7967a41f5',
              'address': city}
    res = requests.get(url, params)
    jd = json.loads(res.text)
    # print(jd)
    location = jd['geocodes'][0]['location']
    locations = location.split(',')
    return locations


df_route = pd.read_excel('data/可用路线.xlsx')
df_route = df_route.dropna()
df_route.drop(df_route[df_route['目的地'] == '省直辖县级行政区划'].index, inplace=True)
df_route.drop(df_route[df_route['起始地'] == '省直辖县级行政区划'].index, inplace=True)
start_cities = list(df_route['起始地'].unique())
terminal_cities = list(df_route['目的地'].unique())
city_dict = {}
cities = start_cities + terminal_cities
cities = list(set(cities))
for city in cities:
    city_dict[city] = coords(city)

with open('data/loactions.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(city_dict, ensure_ascii=False))

