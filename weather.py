import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int

def get_lat_lon(city_name, state_code, country_code, API_key):
    resp = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}").json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

def get_temp(lat, lon, API_key):
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=imperial").json()
    data = (resp.get('main')).get('temp')
    return data

def get_data(lat, lon, API_key):
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=imperial").json()
    data = WeatherData(
        main = resp.get('weather')[0].get('main'),
        description = resp.get('weather')[0].get('description'),
        icon = resp.get('weather')[0].get('icon'),
        temperature = int((resp.get('main')).get('temp'))
    )
    return data
    
def main(city_name, state_name, country_name):
    lat, lon = get_lat_lon(city_name, state_name, country_name, api_key)
    return get_data(lat, lon, api_key)

if __name__ == "__main__":
    lat, lon = get_lat_lon('Andover', 'MA', 'US', api_key)
    print(get_data(lat, lon, api_key))