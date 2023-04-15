"""
This is a Python module that contains the TheMovieDB class for interacting with
The Movie Database API and retrieving top rated movies, currently playing
movies, and search movies based on a search query.
"""
import os
import requests
from APIs import handleAPIs


class TheMovieDB:
    """
    A class for interacting with The Movie Database API.
    """

    def __init__(self):
        handleAPIs.configure()
        self.apiUrl = "https://api.themoviedb.org/3"
        self.apiKey = os.getenv("movieAPIKey")

    def getTopRateds(self):
        """
        Fetches a list of the top rated movies from MDB API.

        Returns:
            A string object that contains movies from the API.
        """
        response = requests.get(
            f"""{self.apiUrl}/movie/top_rated?api_key={self.apiKey}\
&language=en-US&page=1""",
            timeout=10,
        )
        movies = self.parseMovieFromJson(response.json())
        return movies

    def getNowPlaying(self):
        """
        Sends a GET request to the TMDb API to retrieve a list of the top rated movies.
        """
        response = requests.get(
            f"""{self.apiUrl}/movie/now_playing?\
api_key={self.apiKey}&language=en-US&page=1""",
            timeout=10,
        )
        movies = self.parseMovieFromJson(response.json())
        return movies

    def getSearchMovie(self, searchQuery):
        """
        Sends a GET request to the TMDb API to search for movies based on a
        search query.

        Args:
            searchQuery(str): A string containing the search query.

        Returns:
            A json object containing the search results from the API.
        """
        response = requests.get(
            f"""{self.apiUrl}/search/movie?api_key={self.apiKey}\
&language=en-US&query={searchQuery}&page=1&include_adult=true""",
            timeout=10,
        )
        return response.json()

    def parseMovieFromJson(self, movies):
        """
        Parses a dictionary of movie data in JSON format and returns a string.

        Args:
            movies(json): Movie data in JSON format.

        Returns:
            A string containing a formatted list of the movies and their
            corresponding scores, sorted in descending order by score
        """
        answer = ""
        for index, movie in enumerate(movies["results"]):
            answer = answer + (
                f"{str(index+1)}) Name: {movie['title']}--Score:{movie['vote_average']}\n"
            )
        return answer
