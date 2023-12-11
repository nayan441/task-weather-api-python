import os
import requests
import asyncio
import httpx
import logging
import matplotlib.pyplot as plt
from db_connect import db
from datetime import datetime
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')




def fetch_avg_weather_data(city):
    try:
        avg = 6
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={avg}&appid={api_key}'
        response = requests.get(url)
        data = response.json()
        logging.info(f"Successfully fetched weather data for {city}")
        return data
    except Exception as e:
        logging.error(f"Error retrieving weather data from api: {e}")

def analyze_data(data):

    try:
        avg_hum = 0
        avg_temp = 0
        for i in data[0]['weather_data_6']:
            avg_temp += i['temperature']
            avg_hum += i['humidity']
        temperature = avg_temp // 6
        humidity = avg_hum // 6
        logging.info(f"Successfully analyzed weather data")
        return temperature, humidity
    except (KeyError, IndexError) as e:
        logging.error(f"Error analyzing weather data: {e}")
        return None, None


def visualize_data(average_temperature, average_humidity, city):
    try:
        labels = [
            f'Temperature {average_temperature} K',
            f'Humidity {average_humidity} %']
        values = [average_temperature, average_humidity]
        plt.bar(labels, values)
        plt.xlabel('Metrics')
        plt.ylabel('Average Values')
        plt.title(f'Average Temperature and Humidity for {city}')
        plt.savefig(
                f'sync_weather_chart_{city}_today.png')

        current_directory = os.getcwd()

        print(f"Average Temperature and Humidity graph  for {city}" +
              f" got saved with in name 'weather_chart_{city}_today.png'" +
              f" at location {current_directory}/sync_weather_chart_{city}_today.png")
        logging.info(f"Saved graph to {current_directory}/sync_weather_chart_{city}_today.png")

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
        result = weather_collection.update_one(
            filter_criteria, update_data, upsert=True)
        if result.upserted_id is not None:

            logging.info(f"Data inserted with ObjectId: {result.upserted_id} in database")
        else:
            logging.info(f"Data updated for city: {city.lower()}")

    except Exception as e:
        logging.error(f"Error storing weather data in MongoDB: {e}")


def get_data_mongodb(city):
    try:
        weather_collection = db['avg_weather_collection']
        data = list(weather_collection.find({'city': city.lower()}))
        logging.info(f"Successful retrival weather data from MongoDB")
        return data
    except Exception as e:
        logging.error(f"Error retrieving weather data from MongoDB: {e}")
        return None


def avg_weather_data(city):
    logging.info("\n\n Inside avg_weather_data\n\n")
    try:
        city = city.strip()
        weather_data = fetch_avg_weather_data(city)
        logging.info("Fetch data for sync call")
        if weather_data['cod'] != '200':
            logging.info(f"Error fetching weather data. Please check the city name and try again.")
            print("Error fetching weather data. Please check the city name and try again.")
            return
        relevent_data_list = list()
        for weather_data_obj in weather_data['list']:
            relevent_data = {
                "temperature": weather_data_obj['main']['temp'],
                "humidity": weather_data_obj['main']['humidity'],
                "wind_speed": weather_data_obj['wind']['speed']
            }
            relevent_data_list.append(relevent_data)
        store_data_mongodb(city, relevent_data_list, True)
        visualize_data_temp, visualize_data_humid = analyze_data(
            get_data_mongodb(city))
        visualize_data(visualize_data_temp, visualize_data_humid, city)
    except Exception as e:
        logging.error(f"Error while executing function: {e}")
        return None
