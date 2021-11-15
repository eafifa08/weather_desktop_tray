"""Get now-weather in city from openweathermap.org"""
import requests
import random
import datetime


def get_current_temp(apikey, city='Kurgan,ru'):
    time = datetime.datetime.now()
    str_time = time.strftime("%Y-%m-%d, %H:%M:%S")
    print(str_time)

    if city == 'Kurgan,ru':
        random_temp = random.randrange(-10, 10, 1)
    elif city == 'Sochi,ru':
        random_temp = random.randrange(20, 40, 1)
    else:
        random_temp = 0
    print(f'now in {city} temperature:', random_temp)
    return {'temp': random_temp, 'time': str_time}

    language = 'ru'
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={language}&units={units}'
    r = requests.get(url)
    response_dict = r.json()
    now_temperature = int(response_dict.get('main').get('temp'))
    print(f'now in {city} temperature:', str(now_temperature))
    return {'temp': now_temperature, 'time': str_time}


def main():
    apikey = 'a3256ac125b274f106c81725ac008679'
    get_current_temp(apikey, city='Kurgan,ru')
    get_current_temp(apikey, city='Sochi,ru')
    get_current_temp(apikey, city='North Slope Borough,us')
    get_current_temp(apikey, city='Chicago,us')


if __name__ == '__main__':
    main()
