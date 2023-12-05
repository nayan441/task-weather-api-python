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
    try:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={avg}&appid={api_key}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data for {city}: {e}")
        return None

def analyze_data(data):
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
        plt.savefig(f'weather_chart_{city}_today.png')  # Save the figure to a file
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

def avg_weather_data():

    city = input("Enter the city: ")
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







def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def print_menu():
    print(f"{Fore.BLUE}Press 1){Style.RESET_ALL} for average temperature and humidity of a desired city")
    print(f"{Fore.BLUE}Press 2){Style.RESET_ALL} for weather data from multiple cities")
    print(f"{Fore.RED}Enter 'q' to quit{Style.RESET_ALL}")


if __name__ == "__main__":
    clear_screen()
    print(api_key)

    while True:
        print_menu()
        user_choice = input("\nEnter your choice: ")

        if user_choice == '1':
            print("Average temperature and humidity of your city today")
            avg_weather_data()
        elif user_choice == '2':
            print("Weather data from multiple cities")
            count = int(input("How many cities' data do you want to retrieve: "))
            cities_data = []
            for i in range(count):
                city = input(f"Enter city {i+1}: ")
                cities_data.append(city)
            print(f"Selected cities: {', '.join(cities_data)}")

        # elif user_choice == '3':
        #     print("Historical weather data")
        #     print("\nList of cities we have in our database and their temperature measured date")
        #     print("Cities      From Date")
        elif user_choice.lower() == 'q':
            print("Exiting...")
            break
        else:
            print(f"{Fore.RED}Please enter a valid choice{Style.RESET_ALL}")

        input("\nPress Enter to continue...")
        clear_screen()
