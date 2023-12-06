# Weather Data Dashboard

This Python script provides functionality to fetch and visualize weather data. It uses the OpenWeatherMap API to retrieve average weather data for a specified city, store it in MongoDB, and visualize the results.

## Features

- Fetch average temperature and humidity for a desired city.
- Store weather data in MongoDB for future reference.
- Visualize temperature and humidity using matplotlib.

## Prerequisites

Before running the script, ensure you have the following:

- Python installed (version 3.x recommended)
- Required Python packages: requests, matplotlib, pymongo, httpx, colorama, dotenv

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Weather-Data-Dashboard.git

2. Create virtual environment and activate:

   ```bash
   virtualenv venv
   source venv/bin/activate

3. Install required packages:

   ```bash
   pip install -r requirements.txt

4. Run script(For sync):

   ```bash
   python3 weather_api_call.py

5. Run script (For async):

   ```bash
   python3 async_weather_api_call.py