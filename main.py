"""
This is a Python script for a Discord chatbot with several functionalities. It
has commands for playing rock-paper-scissors, getting movie recommendations, and
asking general questions to an AI chatbo

The bot uses the Discord API to communicate with users, and it also uses several
APIs to get data for the different functionalities. It uses the requests module
to make HTTP requests and get the responses from these APIs

The script defines a Discord client using the discord.ext module, and it also
defines several commands that the bot responds to
"""
import datetime as dt
import logging
import os
import random

import discord
from discord.ext import commands

from APIs import handleAPIs
from apps.chatBot import ChatGPT
from apps.movieDB import TheMovieDB
from apps.RockPaperScissors import Rps
from apps.weatherForecast import WeatherForecast
from keep_alive import keep_alive

prefix = "lw"
intents = discord.Intents.all()
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)


@client.event
async def on_ready():
    """
    sets the bot's status and activity when it is first started up
    """
    print(f"I am ready to go - {client.user.name}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{client.command_prefix}help. This bot is made by LordWile.",
        )
    )


rps = Rps()
movieApi = TheMovieDB()
weather = WeatherForecast()


# #! BASIC DISCORD EVENTS - NEEDS FIX
# @client.command(name="clear")
# async def clearMessages(ctx, amount: int):
#     """
#     Deletes specified amount of messages.
#     Args:
#         amount (int): number of messages to delete.
#     """
#     print("what")
#     print(type(amount) + amount)
#     await ctx.channel.purge(limit=amount)


#! CHATGPT
@client.command(name="chat")
async def askQuestion(ctx):
    """
    Asks the user for a question, waits for their response, passes the question
    to an AI model to get an answer, and sends the answer back to the user.
    """

    await ctx.send("What do you want to ask?")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    chatGPT = ChatGPT(msg.author.name)
    answer = chatGPT.getAnswerFromAI(msg.content)
    await ctx.send(answer)


@client.command(name="SetAPI")
async def setUserAPI(ctx):
    await ctx.send("Please provide your API key")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    chatGPT = ChatGPT(msg.author.name)
    result = chatGPT.setAPI(msg.content)
    await msg.delete()
    await ctx.send(result)


#! MOVIE DB
@client.command(name="topRate")
async def topRate(ctx):
    """
    Retrieves the top rated movies from the movie API and sends a formatted
    message with their names and scores.
    """
    movies = movieApi.getTopRateds()

    await ctx.send(movies)


@client.command(name="nowPlaying")
async def nowPlaying(ctx):
    """
    Retrieves the list of movies currently playing in theaters from the movie
    API and sends a formatted message with their names and scores.
    """
    answer = movieApi.getNowPlaying()

    await ctx.send(answer)


@client.command(name="movSearch")
async def search(ctx):
    """
    Handles the core functionality of the movie search command and provides the
    user with an interactive experience to browse and view movie details.
    """
    await ctx.send("Write the name of movie you want to see!")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check=check)
    userSearch = msg.content.lower()
    movies = movieApi.getSearchMovie(userSearch)
    counter = 0
    movieOverviews = {}
    movieTitles = {}
    if not movies["results"]:
        await ctx.send("Couldn't find any movies :(")
    else:
        for counter, movie in enumerate(movies["results"], start=1):
            answer = f"""\n{counter}.Movie name: {movie['title']}\
--Score: {movie['vote_average']}--Adult: {movie['adult']}\n"""
            movieOverviews[counter] = movie["overview"]
            movieTitles[counter] = movie["title"]
            await ctx.send(answer)
            if counter % 5 == 0:
                await ctx.send("Would you like to see 5 more results? (y/n)")
                fiveMore = await client.wait_for("message", check=check)
                if fiveMore.content == "y":
                    continue
                elif fiveMore.content == "n":
                    await ctx.send("Do you want to see summary of any result?(y/n)")
                    summaryAnsw = await client.wait_for("message", check=check)
                    if not summaryAnsw.content == "y":
                        await ctx.send("You know :/")
                        break
                    else:
                        await ctx.send("Enter the id of movie you want to see")
                        summaryNo = await client.wait_for("message", check=check)
                        summaryNo = int(summaryNo.content)
                        while summaryNo > counter and summaryNo < 0:
                            await ctx.send(f"There is only {counter} movies")
                            summaryNo = await client.wait_for("message", check=check)
                            summaryNo = int(summaryNo.content)
                        await ctx.send(movieTitles[summaryNo])
                        await ctx.send(movieOverviews[int(summaryNo)])
                        break
                else:
                    await ctx.send("Wrong code!")
                    break
        if counter % 5 != 0:
            await ctx.send("Do you want to see summary of any result?(y/n)")
            overviewAnsw = await client.wait_for("message", check=check)
            if not overviewAnsw.content == "y":
                await ctx.send("You know :/")
            else:
                await ctx.send("Enter the id of movie you want to see")
                summaryNo = await client.wait_for("message", check=check)
                summaryNo = int(summaryNo.content)
                await ctx.send(movieOverviews[int(summaryNo)])


#! Rock-Paper-Scissors
@client.command(name="rps")
async def rpsGame(ctx):
    """
    Rock-Paper-Scissors game for users.
    """
    MAX_ATTEMPTS = 3

    validChoices = "r(rock), p(paper), s(scissors)"
    await ctx.send(
        "Welcome to rock-paper-scissors game.\nYou can choose by typing" + validChoices
    )

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    for i in range(MAX_ATTEMPTS):
        msg = await client.wait_for("message", check=check)
        userChoice = msg.content.lower()
        intUserChoice = rps.userChoiceConv(userChoice)
        if intUserChoice in [1, 2]:
            break
        else:
            await ctx.send(
                f"There is no such choice! Valid choices:{validChoices}, try again."
            )
        if i == MAX_ATTEMPTS - 1:
            await ctx.send("Max attempts reached. Exiting game...")
    userShape = rps.shapes(intUserChoice)
    botChoice = random.randint(0, 2)  # rock=0,paper=1,scissors=2
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


#! Weather Forecast
@client.command(name="weather")
async def weatherForecast(ctx):
    """
    Display the weather forecast for a given city.
    """
    MAX_ATTEMPTS = 2

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send("Enter a city to see its weather forecast")

    for i in range(MAX_ATTEMPTS):
        msg = await client.wait_for("message", check=check)
        city = msg.content.lower()
        weatherRes = weather.getWeather(city)
        if weatherRes["cod"] == str(404):
            await ctx.send("There is no such city please try again")
        else:
            break
        if i == MAX_ATTEMPTS - 1:
            await ctx.send("Max attempts reached. Exiting...")

    # ? Getting and fetching data
    tempKelvin = weatherRes["main"]["temp"]
    tempCelcius = weather.kelvinToCelcius(tempKelvin)

    feelsLikeKelvin = weatherRes["main"]["feels_like"]
    feelsLikeCelcius = weather.kelvinToCelcius(feelsLikeKelvin)

    sunriseTime = dt.datetime.utcfromtimestamp(
        weatherRes["sys"]["sunrise"] + weatherRes["timezone"]
    ).strftime("%H:%M")

    sunsetTime = dt.datetime.utcfromtimestamp(
        weatherRes["sys"]["sunset"] + weatherRes["timezone"]
    ).strftime("%H:%M")

    description = weatherRes["weather"][0]["description"]
    windSpeed = weatherRes["wind"]["speed"]
    humidity = weatherRes["main"]["humidity"]
    await ctx.send(f"Displaying weather report for: {city} ")
    await ctx.send(
        f"""Temperature:{tempCelcius:.2f}°C and feels like \
{feelsLikeCelcius:.2f}°C \nHumidity: {humidity}% Wind speed:{windSpeed}m/s\
Sunrises at {sunriseTime} and sun sets at {sunsetTime}"""
    )
    await ctx.send(f"General Weather: {description}")


#! ERROR HANDLING
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command.")


@clearMessages.error
async def clearError(ctx, error):  # ? MissingRequiredArgument
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the amount of messages to delete.")


keep_alive()
handleAPIs.configure()

client.run(os.getenv("discordTOKEN"))
