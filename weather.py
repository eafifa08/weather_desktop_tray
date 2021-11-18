"""Get now-weather in city from openweathermap.org"""
import requests
import random
import datetime


def get_current_temp(city='Kurgan,ru', apikey='NO_API_KEY'):
    time = datetime.datetime.now()
    str_time = time.strftime("%Y-%m-%d, %H:%M:%S")
    print(str_time)

    """
    if city == 'Kurgan,ru':
        random_temp = random.randrange(-10, 10, 1)
    elif city == 'Sochi,ru':
        random_temp = random.randrange(20, 40, 1)
    else:
        random_temp = 0
    print(f'now in {city} temperature:', random_temp)
    return random_temp
    """

    language = 'ru'
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={language}&units={units}'
    r = requests.get(url)
    response_dict = r.json()
    now_temperature = int(response_dict.get('main').get('temp'))
    print(f'{city}:', str(now_temperature))
    return now_temperature


def get_forecast(city='Kurgan,ru', apikey='NO_API_KEY'):
    time = datetime.datetime.now()
    str_time = time.strftime("%Y-%m-%d, %H:%M:%S")
    print(str_time)
    language = 'ru'
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={language}&units={units}'
    url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&lang={language}&units={units}'
    r = requests.get(url2)
    response_dict = r.json()
    now_temperature = int(response_dict.get('main').get('temp'))
    print(f'now in {city} temperature:', str(now_temperature))
    return now_temperature


def main():
    apikey = 'a3256ac125b274f106c81725ac008679'

    #get_current_temp(city='Kurgan,ru', apikey=apikey)
    #get_current_temp(city='Sochi,ru', apikey=apikey)
    #get_current_temp(city='North Slope Borough,us', apikey=apikey)
    #get_current_temp(city='Chicago,us', apikey=apikey)
    get_forecast(city='Kurgan,ru', apikey=apikey)

if __name__ == '__main__':
    main()
