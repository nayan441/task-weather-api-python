import os
import asyncio
import httpx
import logging
import matplotlib.pyplot as plt
from db_connect import db
from datetime import datetime
from colorama import Fore, Style
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



async def fetch_weather_data_async(city, session):
    cnt = 6
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={cnt}&appid={api_key}'
    
    # Await the asynchronous response
    async with session.get(url) as response:
        response.raise_for_status()
        data = await response.json()
        return city, data

async def fetch_all_weather_data(cities):
    async with httpx.AsyncClient() as session:
        tasks = [fetch_weather_data_async(city, session) for city in cities]
        results = await asyncio.gather(*tasks)
        return results

async def main(cities):
    results = await fetch_all_weather_data(cities)
    for city, data in results:
        print(f"Weather data for {city}: {data}")

if __name__ == "__main__":
    cities_data = ['delhi', 'mumbai']
    asyncio.run(main(cities_data))



# def analyze_data(data):
#     try:
#         avg_hum = 0
#         avg_temp = 0
#         for i in data['list']:
#             avg_temp += i['main']['temp']
#             avg_hum += i['main']['humidity']
#         temperature = avg_temp // len(data['list'])
#         humidity = avg_hum // len(data['list'])
#         return temperature, humidity
#     except (KeyError, IndexError) as e:
#         logging.error(f"Error analyzing weather data: {e}")
#         return None, None


# def visualize_data(average_temperature, average_humidity, city):
#     try:
#         labels = ['Temperature', 'Humidity']
#         values = [average_temperature, average_humidity]
#         plt.bar(labels, values)
#         plt.xlabel('Metrics')
#         plt.ylabel('Average Values')
#         plt.title(f'Average Temperature and Humidity for {city}')
#         plt.savefig(f'weather_chart_{city}.png')  # Save the figure to a file
#         current_directory = os.getcwd()

#         print(f"Average Temperature and Humidity graph for {city}" +
#               f" got saved with the name 'weather_chart_{city}.png'" +
#               f" at location {current_directory}/weather_chart_{city}.png")
#     except Exception as e:
#         logging.error(f"Error visualizing weather data: {e}")


# def store_data_mongodb(city, weather_data, avg_weather_collection=False):
#     try:
#         weather_collection = db['avg_weather_collection']
#         date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         avg_weather_data = {
#             'city': city.lower(),
#             'weather_data_6': weather_data,
#             'date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#         result = weather_collection.insert_one(avg_weather_data)
#         print(f"Data inserted with ObjectId: {result.inserted_id} in database")

#     except Exception as e:
#         logging.error(f"Error storing weather data in MongoDB: {e}")


# def get_data_mongodb(city):
#     try:
#         weather_collection = db['avg_weather_collection']
#         # Retrieve all data from the collection
#         data = list(weather_collection.find({'city': city.lower()}))
#         return data
#     except Exception as e:
#         logging.error(f"Error retrieving weather data from MongoDB: {e}")
#         return None


# async def main(cities):
#     # Asynchronous API requests
#     results = await fetch_all_weather_data(cities)

#     for city, data in results:
#         if data is not None and data['cod'] == '200':
#             relevent_data_list = list()
#             for weather_data_obj in data['list']:
#                 relevent_data = {
#                     "temperature": weather_data_obj['main']['temp'],
#                     "humidity": weather_data_obj['main']['humidity'],
#                     "wind_speed": weather_data_obj['wind']['speed']
#                 }
#                 relevent_data_list.append(relevent_data)
#             print("relevent_data_list\n\n")
#             print(relevent_data_list)
#             # Synchronous operations
#             # store_data_mongodb(city, relevent_data_list, True)
#             # visualize_data_temp, visualize_data_humid = analyze_data(get_data_mongodb(city))
#             # if visualize_data_temp is not None and visualize_data_humid is not None:
#             #     visualize_data(visualize_data_temp, visualize_data_humid, city)
#         else:
#             print(f"Error fetching weather data for {city}. Please check the city name and try again.")


# if __name__ == "__main__":
#     print("Weather data from multiple cities")
#     # count = int(input("How many cities' data do you want to retrieve: "))
#     cities_data = ['delhi','mumbai']
#     # for i in range(count):
#     #     city = input(f"Enter city {i+1}: ")
#     #     cities_data.append(city.strip())
#     # print(f"Selected cities: {', '.join(cities_data)}\n\n")
#     asyncio.run(main(cities_data))
