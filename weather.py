import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    time: str
    city: str
    state: str
    description: str
    icon: str
    temperature: int
    precipitation: float
    
@dataclass
class FinalData:
    startData: WeatherData
    endData: WeatherData

def get_lat_lon(city_name, state_code, country_code, API_key):
    resp = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}").json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

def get_city_state(lat, lon, API_key):
    resp = requests.get(f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={1}&appid={API_key}").json()
    data = resp[0]
    city, state = data.get('name'), data.get('state')
    return city, state

def get_temp(lat, lon, API_key):
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=imperial").json()
    data = (resp.get('main')).get('temp')
    return data

def get_data(lat, lon, API_key):
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=imperial").json()
    data = WeatherData(
        description = resp.get('weather')[0].get('description'),
        icon = resp.get('weather')[0].get('icon'),
        temperature = int((resp.get('main')).get('temp')),
        precipitation = 0,
        city = "",
        state = "",
        time = ""
    )
    return data
    
def get_forecast(lat, lon, API_key, dt):
    city_, state_ = get_city_state(lat, lon, API_key)
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=imperial").json()
    forecast = resp.get('list')[0]
    min = 999999999999999999999
    #finds closest datetime in the forecast to the given datetime
    for e in resp.get('list'):
        if (abs(e.get('dt')-dt) < min):
            forecast = e
            min = abs(e.get('dt')-dt)
    data = WeatherData(
        description = forecast.get('weather')[0].get('description'),
        icon = forecast.get('weather')[0].get('icon'),
        temperature = int((forecast.get('main')).get('temp')),
        precipitation = int(forecast.get('pop')*100),
        city = city_,
        state = state_,
        time = forecast.get('dt_txt')
    )
    return data

def get_dt(month, day, hr, min):
    year = datetime.utcnow().year
    dt = datetime(year, month, day, hr, min)
    dt_utc = dt.replace(tzinfo=timezone.utc)
    time = int((dt_utc - datetime(1970,1,1,tzinfo=timezone.utc))/timedelta(seconds=1))
    return time+18000
    
def get_weather(start_lat, start_lon, end_lat, end_lon, month, day, hr, minute, duration):
    data = FinalData(
        startData = get_forecast(start_lat, start_lon, api_key, get_dt(month, day, hr, minute)),
        endData = get_forecast(end_lat, end_lon, api_key, get_dt(month, day, hr, minute)+duration)
    )
    return data
    
def main(city_name, state_name, country_name):
    lat, lon = get_lat_lon(city_name, state_name, country_name, api_key)
    return get_data(lat, lon, api_key)

def getDate(dateStr):
    x = dateStr.split("-")
    month, day = int(x[1]), int(x[2])
    return month, day

def getTime(timeStr):
    x = timeStr.split(":")
    hour, minutes = int(x[0]), int(x[1])
    return hour, minutes

if __name__ == "__main__":
    
    #test code
    start_lat, start_lon = get_lat_lon('Boston', 'MA', 'US', api_key)
    end_lat, end_lon = get_lat_lon('New York', 'NY', 'US', api_key)
    
    print(get_lat_lon('Boston', 'MA', 'US', api_key))
    print(get_lat_lon('New York', 'NY', 'US', api_key))
    
    
    print(get_weather(start_lat, start_lon, end_lat, end_lon, 12, 4, 4, 53, 0))
    print(get_dt(12, 4, 4, 53))
    
    print(getDate('2023-12-05'))