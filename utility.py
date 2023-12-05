from datetime import datetime

def convert_to_unix_timestamp(date_str):
    date_object = datetime.strptime(date_str, "%d-%m-%Y")
    timestamp = int(date_object.timestamp())
    return timestamp

start_date_str = "01-12-2023"
end_date_str = "05-12-2023"

start_timestamp = convert_to_unix_timestamp(start_date_str)
end_timestamp = convert_to_unix_timestamp(end_date_str)

print(f"Start timestamp: {start_timestamp}")
print(f"End timestamp: {end_timestamp}")


# ====================================================================================================================
# Historical weather data

def fetch_historical_weather_data(city, start, end):
    try:
        url = f'https://history.openweathermap.org/data/2.5/history/city?q={city}&type=hour&start={start}&end={end}&appid={api_key}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data for {city}: {e}")
        return None
