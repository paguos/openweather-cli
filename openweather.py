'''
An CLI to interact with the OpenWeather API
'''

from datetime import datetime
from os.path import expanduser

import os
import sys
import click
import requests

WEEK_DAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wenesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

ICONS = {
    '01': ' ☀️',
    '02': ' 🌤',
    '03': ' 🌥' ,
    '04': ' ☁️',
    '09': ' 🌧',
    '10': ' 🌦',
    '11': ' ⛈',
    '13': ' 🌨',
    '50': ' 🌫'
}


@click.group()
@click.option(
    '--celsius', '-c',
    is_flag=True,
    help='Show all the temperatures in celsius',
)
@click.option(
    '--api-key', '-a',
    envvar="OW_API_KEY",
    help='Your OpenWeather API Key'
)
@click.pass_context
def cli(ctx, celsius, api_key):
    ctx.obj['CELSIUS'] = celsius
    ctx.obj['API-KEY'] = api_key


@cli.command('config', help="Configurates the OpenWeather API Key")
def config():
    """Saves the API KEY in the ~/.weather.cfg file."""
    config_file = os.path.expanduser('~/.weather.cfg')
    api_key = click.prompt(
        "Please enter your API key",
    )

    with open(config_file, 'w') as cfg:
        cfg.write(api_key)


@cli.command('current', help='Show the current weather in a given city')
@click.argument('location')
@click.pass_context
def current(ctx, location):
    """CLI command for current weather of a given location."""
    celsius = ctx.obj['CELSIUS']
    api_key = ""

    try:
        api_key = get_api_key()
    except FileNotFoundError:
        pass

    if ctx.obj['API-KEY'] is not None:
        api_key = ctx.obj['API-KEY']

    if api_key == "":
        print("Please enter your OpenWeather API KEY")
        sys.exit()

    weather = current_weather(location, celsius, api_key)
    print("OpenWeather CLI ✨\n\n" + weather)


@cli.command('forecast', help='Show the forecast weather for the next 5 days each 3 hours in a given city')
@click.argument('location')
@click.option(
    '--results', '-r',
    help='Number of days you want to show?',
)
@click.pass_context
def forecast(ctx, location, results):
    """CLI command for the forecast api."""
    celsius = ctx.obj['CELSIUS']

    api_key = ""

    try:
        api_key = get_api_key()
    except FileNotFoundError:
        pass

    if ctx.obj['API-KEY'] is not None:
            api_key = ctx.obj['API-KEY']

    if api_key == "":
        print("Please enter your OpenWeather API KEY")
        sys.exit()

    weather = forecast_weather(location, celsius, results, api_key)
    print("OpenWeather CLI ✨\n\n" + weather)


def current_weather(location, celsius, api_key=""):
    """Return the current weather in a given location."""
    url = 'http://api.openweathermap.org/data/2.5/weather'

    query_params = {
        'q': location,
        'APPID': api_key
    }

    if celsius:
        query_params['units'] = 'metric'

    response = requests.get(url, params=query_params)

    country = response.json()['sys']['country']
    city = response.json()['name']
    weather = response.json()['weather'][0]['description']
    icon = response.json()['weather'][0]['icon'][:-1]
    temp = response.json()['main']['temp']
    temp_max = response.json()['main']['temp_max']
    temp_min = response.json()['main']['temp_min']

    return "City: %s \nCountry: %s \n\n%s%s\n \nCurrent Temperature: %.2f \nMax Temperature: %.2f \nMin Temperature: %.2f" % (city, country, weather, ICONS[icon], temp, temp_max, temp_min)


def forecast_weather(location, celsius, days, api_key=""):
    """Return the forecast for the next 5 days in an 3h interval of a given localtion."""
    url = 'http://api.openweathermap.org/data/2.5/forecast'

    query_params = {
        'q': location,
        'APPID': api_key,
        'cnt': days
    }

    if celsius:
        query_params['units'] = 'metric'

    response = requests.get(url, params=query_params)
    
    country = response.json()['city']['country']
    city = response.json()['city']['name']
    weather_list = response.json()['list']

    str_list = "City: %s \nCountry: %s\n" % (city, country)

    for weather in weather_list:
        temp = weather['main']['temp']
        description = weather['weather'][0]['description']
        icon = weather['weather'][0]['icon'][:-1]

        dt_txt = weather['dt_txt']
        date = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
        day_nr = date.weekday()

        str_list = str_list + "\n%s %ih\n%s%s\nTemperature: %.2f\n" % (WEEK_DAYS[day_nr], date.hour , description , ICONS[icon], temp)
    
    return str_list


def get_api_key():
    """Return API KEY from the config file."""
    home = expanduser("~")
    with open(home + '/.weather.cfg') as f:
        first_line = f.readline()

        if first_line is not None:
            return first_line
        else:
            return None


if __name__ == "__main__":
    cli(obj={})
