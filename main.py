import discord, os, requests, json, time, random, textwrap
import pandas as pd
import datetime as dt
from discord.ext import commands
from keep_alive import keep_alive

prefix = "lw2"
intents = discord.Intents.all()
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix=prefix, case_insensitive=False, intents=intents)


@client.event
async def on_ready():
    print(f"I am ready to go - {client.user.name}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{client.command_prefix}help. This bot is made by LordWile.",
        )
    )


# MovieDB Application
class TheMovieDB:
    def __init__(self):
        self.apiUrl = "https://api.themoviedb.org/3"
        self.apiKey = os.getenv("movieApiKey")

    def getTopRateds(self):
        response = requests.get(
            f"{self.apiUrl}/movie/top_rated?api_key={self.apiKey}&language=en-US&page=1"
        )
        return response.json()

    def getNowPlaying(self):
        response = requests.get(
            f"{self.apiUrl}/movie/now_playing?api_key={self.apiKey}&language=en-US&page=1"
        )
        return response.json()

    def getSearchMovie(self, aranan):
        response = requests.get(
            f"{self.apiUrl}/search/movie?api_key={self.apiKey}&language=en-US&query={aranan}&page=1&include_adult=true"
        )
        return response.json()


# Rock-Paper-Scissors Application
class Rps:
    def shapes(self, choices):
        if choices == 0:
            message = ":punch:"
            return message
        elif choices == 1:
            message = ":hand_splayed:"
            return message
        elif choices == 2:
            message = ":vulcan:"
            return message

    def userChoiceConv(self, choice):
        if choice == "r":
            choice = 0
        elif choice == "p":
            choice = 1
        elif choice == "s":
            choice = 2
        else:
            choice = 3
        return choice


# Weather Forecast Application
class WeatherForecast:
    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/weather?"
        self.apiKey = os.getenv("weatherApiKey")

    def getWeather(self, search):
        searchQuery = f"{self.url}appid={self.apiKey}&q={search}"
        response = requests.get(searchQuery).json()
        return response, searchQuery

    def kelvinToCelcius(self, kelvin):
        celcius = kelvin - 273.15
        return celcius


rps = Rps()
movieApi = TheMovieDB()
weather = WeatherForecast()


@client.command(name="topRate")
async def topRate(ctx):
    movies = movieApi.getTopRateds()
    cikti = ""
    for index, movie in enumerate(movies["results"]):
        cikti = cikti + (
            f"{str(index+1)}. Name: {movie['title']} -- Score:{movie['vote_average']}\n"
        )
    await ctx.send(cikti)


@client.command(name="nowPlaying")
async def nowPlaying(ctx):
    movies = movieApi.getNowPlaying()
    cikti = ""
    for movie in movies["results"]:
        cikti = cikti + (
            f"Movie name: {movie['title']} -- Score:{movie['vote_average']}\n"
        )
    await ctx.send(cikti)


@client.command(name="search")
async def search(ctx):
    await ctx.send("Write the name of movie you want to see!")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    movies = movieApi.getSearchMovie(msg.content)
    result = ""
    counter = 0
    movieDict = {}
    movieTitle = {}
    if movies["results"]:
        for counter, movie in enumerate(movies["results"], start=1):
            cikti = f"\n{counter}.Movie name: {movie['title']} -- Score:{movie['vote_average']} -- Adult:{movie['adult']}\n"
            movieDict[counter] = movie["overview"]
            movieTitle[counter] = movie["title"]
            await ctx.send(cikti)
            if counter % 5 == 0:
                await ctx.send("Would you like to see 5 more results? (y/n)")
                fiveMore = await client.wait_for("message", check=check)
                if fiveMore.content == "y":
                    continue
                elif fiveMore.content == "n":
                    await ctx.send("Do you want to see summary of any result?(y/n)")
                    summaryAnsw = await client.wait_for("message", check=check)
                    if summaryAnsw.content == "y":
                        await ctx.send("Enter the id of movie you want to see")
                        summaryNo = await client.wait_for("message", check=check)
                        summaryNo = int(summaryNo.content)
                        while summaryNo > counter and summaryNo < 0:
                            await ctx.send(f"There is only {counter} movies")
                            summaryNo = await client.wait_for("message", check=check)
                            summaryNo = int(summaryNo.content)
                        await ctx.send(movieTitle[summaryNo])
                        await ctx.send(movieDict[int(summaryNo)])
                        break
                    else:
                        await ctx.send("You know :/")
                        break
                else:
                    await ctx.send("Wrong code!")
                    break
        if counter % 5 != 0:
            await ctx.send("Do you want to see summary of any result?(y/n)")
            overviewAnsw = await client.wait_for("message", check=check)
            if overviewAnsw.content == "y":
                await ctx.send("Enter the id of movie you want to see")
                summaryNo = await client.wait_for("message", check=check)
                summaryNo = int(summaryNo.content)
                await ctx.send(movieDict[int(summaryNo)])
            else:
                await ctx.send("You know :/")
    else:
        await ctx.send("Couldn't find any movies :(")


# Rock-Paper-Scissors game
@client.command(name="rps")
async def rpsGame(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send(
        "Welcome to rock-paper-scissors game.\nYou can choose by typing r(rock), p(paper), s(scissors)"
    )
    botChoice = random.randint(0, 2)
    # rock=0,paper=1,scissors=2
    userChoice = await client.wait_for("message", check=check)
    intUserChoice = rps.userChoiceConv(userChoice.content)
    while intUserChoice == 3:
        await ctx.send("There is no such choice!")
        await ctx.send("Try again")
        userChoice = await client.wait_for("message", check=check)
        intUserChoice = rps.userChoiceConv(userChoice.content)
    userShape = rps.shapes(intUserChoice)
    botShape = rps.shapes(botChoice)
    await ctx.send("Your choice:")
    await ctx.send(userShape)
    await ctx.send("Bot's choice")
    await ctx.send(botShape)
    if intUserChoice == botChoice:
        await ctx.send("Draw")
    elif intUserChoice + 1 == botChoice or (intUserChoice == 2 and botChoice == 0):
        await ctx.send("You lose!")
    else:
        await ctx.send("You won!")


# Weather Forecast
@client.command(name="weather")
async def weatherForecast(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send("Enter a city to see its weather forecast")
    city = await client.wait_for("message", check=check)
    weatherRes, searchQuery = weather.getWeather(city.content)
    while weatherRes["cod"] == str(404):
        await ctx.send("There is no such city please try again")
        city = await client.wait_for("message", check=check)
        weatherRes = weather.getWeather(city)

    # Getting and fetching data
    tempKelvin = weatherRes["main"]["temp"]
    tempCelcius = weather.kelvinToCelcius(tempKelvin)
    feelsLikeKelvin = weatherRes["main"]["feels_like"]
    feelsLikeCelcius = weather.kelvinToCelcius(feelsLikeKelvin)
    description = weatherRes["weather"][0]["description"]
    sunriseTime = dt.datetime.utcfromtimestamp(
        weatherRes["sys"]["sunrise"] + weatherRes["timezone"]
    ).strftime("%H:%M")
    sunsetTime = dt.datetime.utcfromtimestamp(
        weatherRes["sys"]["sunset"] + weatherRes["timezone"]
    ).strftime("%H:%M")
    windSpeed = weatherRes["wind"]["speed"]
    humidity = weatherRes["main"]["humidity"]
    await ctx.send(f"Displaying weather report for: {city.content.upper()} ")
    await ctx.send(
        f"""Temperature: {tempCelcius:.2f}°C and feels like {feelsLikeCelcius:.2f}°C
Humidity: {humidity}%
Wind speed: {windSpeed}m/s
Sun rises at {sunriseTime} and sun sets at {sunsetTime}"""
    )
    await ctx.send(f"General Weather: {description}")


keep_alive()
client.run(os.getenv("TOKEN"))
