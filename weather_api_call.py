import os
import requests
import asyncio
import httpx
import logging
import matplotlib.pyplot as plt
from db_connect import db
from datetime import datetime
from colorama import Fore, Style

api_key = os.getenv('API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def fetch_avg_weather_data(city):
    avg=6
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={avg}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data
  

def analyze_data(data):
    print(analyze_data)
    print(data)
    try:
        avg_hum = 0
        avg_temp = 0
        for i in  data[0]['weather_data_6']:
            avg_temp +=i['temperature']
            avg_hum +=i['humidity']
        temperature = avg_temp//6
        humidity = avg_hum//6
        return temperature, humidity
    except (KeyError, IndexError) as e:
        logging.error(f"Error analyzing weather data: {e}")
        return None, None

def visualize_data(average_temperature, average_humidity, city):
    try:
        labels = ['Temperature', 'Humidity']
        values = [average_temperature, average_humidity]
        plt.bar(labels, values)
        plt.xlabel('Metrics')
        plt.ylabel('Average Values')
        plt.title(f'Average Temperature and Humidity for {city}')
        # Add values on top of the bars
        for i, v in enumerate(values):
            plt.text(i, v + 0.1, str(round(v, 2)), color='black', ha='center', va='bottom')

        plt.savefig(f'weather_chart_{city}_today.png')  
        current_directory = os.getcwd()

        print(f"Average Temperature and Humidity graph  for {city}"+
            f" got saved with in name 'weather_chart_{city}_today.png'"+ 
            f" at location {current_directory}/weather_chart_{city}_today.png")
    except Exception as e:
        logging.error(f"Error visualizing weather data: {e}")

def store_data_mongodb(city, weather_data, avg_weather_collection=False):
    try:
        weather_collection = db['avg_weather_collection']
        filter_criteria = {'city': city.lower()}
        update_data = {
                    '$set': {
                        'weather_data_6': weather_data,
                        'date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
        result = weather_collection.update_one(filter_criteria, update_data, upsert=True)
        if result.upserted_id is not None:
            print(f"Data inserted with ObjectId: {result.upserted_id} in database")
        else:
            print(f"Data updated for city: {city.lower()}")


    except Exception as e:
            logging.error(f"Error storing weather data in MongoDB: {e}")

def get_data_mongodb(city):
    try:
        weather_collection = db['avg_weather_collection']
        # Retrieve all data from the collection
        data = list(weather_collection.find({'city': city.lower()}))
        return data
    except Exception as e:
        logging.error(f"Error retrieving weather data from MongoDB: {e}")
        return None

def avg_weather_data(city):
    city=city.strip()
    weather_data = fetch_avg_weather_data(city)
    if weather_data['cod'] != '200':
        print("Error fetching weather data. Please check the city name and try again.")
        return
    relevent_data_list = list()
    for weather_data_obj in weather_data['list']:
        relevent_data={
        "temperature" : weather_data_obj['main']['temp'],
        "humidity" : weather_data_obj['main']['humidity'],
        "wind_speed" : weather_data_obj['wind']['speed']
        }
        relevent_data_list.append(relevent_data)
    store_data_mongodb(city, relevent_data_list,True)
    visualize_data_temp, visualize_data_humid = analyze_data(get_data_mongodb(city))
    visualize_data(visualize_data_temp, visualize_data_humid, city)
