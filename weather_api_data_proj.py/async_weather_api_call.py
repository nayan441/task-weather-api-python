import os
import asyncio
import logging
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
from db_connect import db
from datetime import datetime
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()
# Access environment variables
api_key = os.getenv('API_KEY')

async def fetch_weather_data_async(city, session):
    try:
        cnt = 6
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={cnt}&appid={api_key}'
        async with session.get(url) as response:
            data = await response.json()
            logging.info(f"Successfully fetched weather data for {city}")
            return city, data
    except Exception as e:
        logging.error(f"Error retrieving weather data from api: {e}")


async def fetch_all_weather_data(cities):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather_data_async(city, session) for city in cities]
        results = await asyncio.gather(*tasks)
        return results


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


async def visualize_data(average_temperature, average_humidity, city):
    try:
        save_folder = "graph_images/async_graph_images"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        labels = [
            f'Temperature {average_temperature} K',
            f'Humidity {average_humidity} %']
        values = [average_temperature, average_humidity]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Average Values')
        ax.set_title(f'Average Temperature and Humidity for {city}')
        fig.savefig(
            os.path.join(
                save_folder,
                f'async_weather_chart_{city}_today.png'))
        plt.close(fig) 

        print(f"Average Temperature and Humidity graph for {city}" +
              f" got saved with the name 'async_weather_chart_{city}_today.png'" +
              f" at location {os.getcwd()}/{save_folder}/async_weather_chart_{city}_today.png")
        logging.info(f"Saved graph to {os.getcwd()}/{save_folder}/async_weather_chart_{city}_today.png")

    except Exception as e:
        logging.error(f"Error visualizing weather data: {e}")
        print(f"Error visualizing weather data: {e}")
        return




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
        # Retrieve all data from the collection
        data = list(weather_collection.find({'city': city.lower()}))
        logging.info(f"Successful retrival weather data from MongoDB")

        return data
    except Exception as e:
        logging.error(f"Error retrieving weather data from MongoDB: {e}")
        return None


async def async_avg_weather_data(cities):
    logging.info("\n\n Inside async_avg_weather_data\n\n")

    try:
        # Asynchronous API requests
        results = await fetch_all_weather_data(cities)
        logging.info("Fetch data for sync call")

        for city, data in results:
            if data is not None and data['cod'] == '200':
                relevent_data_list = list()
                for weather_data_obj in data['list']:
                    relevent_data = {
                        "temperature": weather_data_obj['main']['temp'],
                        "humidity": weather_data_obj['main']['humidity'],
                        "wind_speed": weather_data_obj['wind']['speed']
                    }
                    relevent_data_list.append(relevent_data)

                # Synchronous operations
                store_data_mongodb(city, relevent_data_list, True)
                visualize_data_temp, visualize_data_humid = analyze_data(
                    get_data_mongodb(city))
                
                print(visualize_data_temp,visualize_data_humid)
                if visualize_data_temp is not None and visualize_data_humid is not None:
                    await visualize_data(visualize_data_temp, visualize_data_humid, city)
                    
            else:
                logging.info(f"Error fetching weather data for {city}. Please check the city name and try again.")

                print(
                    f"Error fetching weather data for {city}. Please check the city name and try again.")
    except Exception as e:
        logging.error(f"Error while executing function: {e}")
        return None
