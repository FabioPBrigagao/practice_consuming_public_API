import requests
import json
import time
import sys

def main():
    list_challenges = loop_possibilities()
    print(list_challenges)

def loop_possibilities():
    list = []
    for i in range(1,28):
        for j in range(1,28):
            for n in range(1,28):
                http_json = reply_http_json(
                    'https://www.brfhub.com/backend/public/api/get-challenges?language=pt&profile=startup&areas%5B%5D={}&areas%5B%5D={}&areas%5B%5D={}'
                    .format(i,j,n))
                for challenge in http_json['data']:
                    found_challenge = challenge['title']
                    list = check_list(found_challenge,list)
    return list

def check_list(challenge, temp_list):
    '''Method checks if string 'challenge' already exists in list 'temp_list'. If so, it returns the
            origin list; otherwise, it append the string into the list and returns the updated list

    input(s): string, list
    output: list
    '''
    exist_challenge = False
    for temp_challenge in temp_list:
        if(challenge == temp_challenge):
            exist_challenge = True
            break
    if(exist_challenge == False):
        temp_list.append(challenge)
    return temp_list

def reply_http_json(URL):
    ''' Returns a json from the URL inputted

    input(s): Any URL
    output: r_json
    '''
    r = requests.get(URL)
    try:
        r_json = r.json()
    except:
        if r.status_code == 429:
            r_headers = json.loads(r.headers)
            wait_time = r_headers['Retry-After'] + 1
            wait_interval(wait_time)
            return reply_http_json(URL)
        else:
            print('Invalid URL')
            sys.exit()
    return r_json

def wait_interval(sec):
    '''Function pauses the script for a specific amount of seconds

    input(s): time in seconds
    '''
    start_time = time.perf_counter()
    diff = 0
    while diff < sec :
        diff = time.perf_counter() - start_time

if __name__ == '__main__':
    main()
