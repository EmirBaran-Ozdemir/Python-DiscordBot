"""
This module provides the WeatherForecast class, which can be used to fetch
weather data and perform temperature conversions. It uses the OpenWeatherMap API
to fetch weather data for a specified location,and provides a method for
converting temperatures from Kelvin to Celsius.
"""
import os
import requests
from APIs import handleAPIs


# Weather Forecast Application
class WeatherForecast:
    """
    A class for fetching weather data and performing temperature conversions.
    """

    def __init__(self):
        """
        Initializes the WeatherForecast object with the OpenWeatherMap API URL and API key.
        """
        handleAPIs.configure()
        self.url = "https://api.openweathermap.org/data/2.5/weather?"
        self.apiKey = os.getenv("weatherAPIKey")

    def getWeather(self, search):
        """
        Fetches weather data for the specified location

        Args:
            search (str): The name of the location to search for.

        Returns:
            tuple: A tuple containing the weather data as a JSON
                response and the search query used to fetch the data.
        """
        searchQuery = f"{self.url}appid={self.apiKey}&q={search}"
        response = requests.get(searchQuery, timeout=100).json()
        return response

    def kelvinToCelcius(self, kelvin):
        """
        Converts a temperature in Kelvin to Celsius.

        Args:
            kelvin (float): The temperature in Kelvin to be converted to Celsius.

        Returns:
            float: The temperature in Celsius.
        """
        celcius = kelvin - 273.15
        return celcius
