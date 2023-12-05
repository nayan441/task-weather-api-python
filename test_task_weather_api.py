import unittest
from unittest.mock import patch, Mock
from weather_proj.weather_api_call import fetch_avg_weather_data, analyze_data, visualize_data, store_data_mongodb, get_data_mongodb, avg_weather_data

class TestWeatherFunctions(unittest.TestCase):
    
    @patch('requests.get')
    def test_fetch_avg_weather_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'list': [{'main': {'temp': 25, 'humidity': 70}, 'wind': {'speed': 5}}]}
        mock_get.return_value = mock_response

        result = fetch_avg_weather_data('test_city')
        self.assertIsNotNone(result)

    @patch('requests.get')
    def test_fetch_avg_weather_data_failure(self, mock_get):
        mock_get.side_effect = Exception('Some error')

        result = fetch_avg_weather_data('test_city')
        self.assertIsNone(result)

    def test_analyze_data(self):
        test_data = {'list': [{'main': {'temp': 20, 'humidity': 60}, 'wind': {'speed': 3}}]}
        result_temp, result_hum = analyze_data(test_data)
        self.assertEqual(result_temp, 20)
        self.assertEqual(result_hum, 60)


    def test_store_and_get_data_mongodb(self):
        # This test assumes a running MongoDB instance and a valid connection
        city = 'test_city'
        data_to_store = [{'temperature': 22, 'humidity': 65, 'wind_speed': 4}]
        store_data_mongodb(city, data_to_store, True)
        result = get_data_mongodb(city)
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()
