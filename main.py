import os
from colorama import Fore, Style
from weather_api_call import avg_weather_data
import time
api_key = os.getenv('API_KEY')

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
    while True:
        print_menu()
        user_choice = input("\nEnter your choice: ")

        if user_choice == '1':
            city = input("Enter the city: ")
            print("Average temperature and humidity of your city today")
            start = time.time()
            avg_weather_data(city)
            end = time.time()
            total_time =  (end-start) * 1000
            print(f"Total time taken: {total_time:.2f} milliseconds")
            
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
