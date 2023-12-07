import pytest
from weather_api_call import fetch_avg_weather_data
import os

api_key = os.getenv('API_KEY')


@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch('requests.get')


def test_fetch_avg_weather_data(mock_requests_get):
    mock_response = {'cod': '200', 'list': [
        {'main': {'temp': 300, 'humidity': 50}, 'wind': {'speed': 10}}]}
    mock_requests_get.return_value.json.return_value = mock_response

    # Call the function
    city = ''
    result = fetch_avg_weather_data(city)

    mock_requests_get.assert_called_once_with(
        f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=6&appid={api_key}')

    # Assert that the function returned the expected result
    assert result == mock_response
