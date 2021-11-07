"""Settings"""
import configparser
import os


def create_config(path):
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'cities', 'Kurgan,ru;Moscow,ru;Sochi,ru;Chicago,us;London,uk')
    config.set('Settings', 'city', 'Kurgan,ru')
    config.set('Settings', 'period', '3')
    with open(path, 'w') as config_file:
        config.write(config_file)


def write_config(path, name_setting, value_setting):
    if not os.path.exists(path):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    config.set('Settings', name_setting, value_setting)
    with open(path, 'w') as config_file:
        config.write(config_file)


def read_config(path, name_setting):
    if not os.path.exists(path):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    return config.get('Settings', name_setting)


if __name__ == "__main__":
    path = "settings.ini"
    if not os.path.exists(path):
        create_config(path)
    #write_config(path, 'city', 'Moscow,ru')
    print(read_config(path, 'city'))
    print(read_config(path, 'period'))
