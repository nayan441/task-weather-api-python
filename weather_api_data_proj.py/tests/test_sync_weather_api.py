import os
import pytest
from weather_api_call import fetch_avg_weather_data

from requests.exceptions import RequestException
from unittest.mock import patch
api_key = os.getenv('API_KEY')

@pytest.fixture
def mock_response():
    return {"cod":"200","message":0,"cnt":6,"list":[{"dt":1702242000,"main":{"temp":289.27,"feels_like":288.53,"temp_min":289.27,"temp_max":289.27,"pressure":1014,"sea_level":1014,"grnd_level":956,"humidity":61,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":1.78,"deg":92,"gust":1.84},"visibility":10000,"pop":0,"sys":{"pod":"n"},"dt_txt":"2023-12-10 21:00:00"},{"dt":1702252800,"main":{"temp":289.01,"feels_like":288.3,"temp_min":288.49,"temp_max":289.01,"pressure":1014,"sea_level":1014,"grnd_level":957,"humidity":63,"temp_kf":0.52},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":1.15,"deg":90,"gust":1.21},"visibility":10000,"pop":0,"sys":{"pod":"n"},"dt_txt":"2023-12-11 00:00:00"},{"dt":1702263600,"main":{"temp":290.61,"feels_like":289.95,"temp_min":290.61,"temp_max":291.28,"pressure":1016,"sea_level":1016,"grnd_level":959,"humidity":59,"temp_kf":-0.67},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":1.45,"deg":118,"gust":1.75},"visibility":10000,"pop":0,"sys":{"pod":"d"},"dt_txt":"2023-12-11 03:00:00"},{"dt":1702274400,"main":{"temp":296.83,"feels_like":296.38,"temp_min":296.83,"temp_max":296.83,"pressure":1016,"sea_level":1016,"grnd_level":959,"humidity":43,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":1.38,"deg":158,"gust":1.5},"visibility":10000,"pop":0,"sys":{"pod":"d"},"dt_txt":"2023-12-11 06:00:00"},{"dt":1702285200,"main":{"temp":298.59,"feels_like":298.05,"temp_min":298.59,"temp_max":298.59,"pressure":1012,"sea_level":1012,"grnd_level":956,"humidity":33,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":0},"wind":{"speed":1.75,"deg":275,"gust":2.68},"visibility":10000,"pop":0,"sys":{"pod":"d"},"dt_txt":"2023-12-11 09:00:00"},{"dt":1702296000,"main":{"temp":295,"feels_like":294.34,"temp_min":295,"temp_max":295,"pressure":1013,"sea_level":1013,"grnd_level":956,"humidity":42,"temp_kf":0},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":{"all":2},"wind":{"speed":0.8,"deg":344,"gust":1.07},"visibility":10000,"pop":0,"sys":{"pod":"d"},"dt_txt":"2023-12-11 12:00:00"}],"city":{"id":1275841,"name":"Bhopal","coord":{"lat":23.2667,"lon":77.4},"country":"IN","population":1599914,"timezone":19800,"sunrise":1702257688,"sunset":1702296331}}

def test_fetch_avg_weather_data_success(mock_response):
    city = "London"
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response

        result = fetch_avg_weather_data(city)

    assert result == mock_response
    mock_get.assert_called_once_with(
        f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=6&appid={api_key}'
    )

def test_fetch_avg_weather_data_failure():
    city = "NonExistentCity"
    
    with patch("requests.get") as mock_get:
        mock_get.side_effect = RequestException("Mocked RequestException")

        result = fetch_avg_weather_data(city)

    assert result is None
