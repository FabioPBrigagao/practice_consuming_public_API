import sys
import json
import time
from itertools import combinations

import requests
from ratelimit import limits, sleep_and_retry

def loop_possibilities(upper_bound, n_combinations=3):
    return combinations(range(1, upper_bound + 1), n_combinations)

@sleep_and_retry
@limits(calls=5, period=30) # decorator
def _http_request(url, method='GET', params={}, json_data={}):
    ''' Returns a json from the url inputted

    input(s): Any url
    output: r_json
    '''
    prep = requests.Request(method, url).prepare()
    if json_data:
        prep.prepare_body(data=json_data, files=None, json=True)
    return requests.Session().send(prep)

def main():

    # pegar endpoint que retorna a lista de possibilidades do formulário anterior
    # ao endpoint dos desafios

    list_possibilities = loop_possibilities(27, 3)

    list_data = []
    for combination in list_possibilities:
        url = 'https://www.brfhub.com/backend/public/api/get-challenges?language=pt&profile=startup&areas%5B%5D={}&areas%5B%5D={}&areas%5B%5D={}'.format(combination[0], combination[1], combination[2])

        r = _http_request(url, 'GET')
        if r.status_code != 200:
            continue

        dict_data = r.json()
        list_data.append(dict_data['data']) # olhar depois

    return list_data

if __name__ == '__main__':
    print(main())
