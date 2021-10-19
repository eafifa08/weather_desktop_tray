"""
weather app for desktop by Sergey Meshkov
"""
import requests


def get_current_temp(city='Kurgan,ru'):
    print(f'now in {city} temperature:', '33')
    return 33
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
