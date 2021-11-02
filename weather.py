"""Get now-weather in city from openweathermap.org"""
import requests
import random


def get_current_temp(city='Kurgan,ru'):
    if city == 'Kurgan,ru':
        random_temp = random.randrange(-10, 10, 1)
    if city == 'Sochi,ru':
        random_temp = random.randrange(20, 40, 1)
    print(f'now in {city} temperature:', {random_temp})
    return random_temp
    #print(f'now in {city} temperature:', '33')
    #return 33
    apikey = 'a3256ac125b274f106c81725ac008679'
    language = 'ru'
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={language}&units={units}'
    r = requests.get(url)
    #print("status code:", r.status_code)
    response_dict = r.json()
    now_temperature = int(response_dict.get('main').get('temp'))
    print(f'now in {city} temperature:', str(now_temperature))
    return now_temperature


def main():
    get_current_temp(city='Moscow,ru')
    get_current_temp(city='Anadyr,ru')
    get_current_temp(city='North Slope Borough,us')
    get_current_temp(city='Chicago,us')


if __name__ == '__main__':
    main()
