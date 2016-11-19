"""
This is a bot that tells the weather & gives inspirational quotes for the
Truman State University area.

author: elias g
version 17.11.16
"""

import tweepy as ty
import random
import arrow
import requests
from truSecret import (consumerKey, consumerSecret, accessToken, accessSecret,
                       darkSkySecret)

# lat and long for Truman State University, per Google Maps
latitude = "40.1876"
longitude = "-92.5819"

# sets the https request url with the auth token, coordinates, excludes hourly
# minutely, and flags values with ?exclude= block
darkSkyURL = ("https://api.darksky.net/forecast/{}/{},{}"
              "?exclude=hourly,minutely,flags".format(darkSkySecret,
                                                      latitude,
                                                      longitude))


def setTwitterAuth():
    # sets the auth tokens for twitter using tweepy
    auth = ty.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    api = ty.API(auth)
    return api


def getCurrentlyWeather(weather):
    currently = weather['currently']['summary']
    # TODO: figure out how to determine cloud coverage in simple/readable form
    # cloudCover = ['currently']['cloudCover']
    temperature = weather['currently']['apparentTemperature']
    precipProb = weather['currently']['precipProbability']
    return currently, temperature, precipProb


def getNextDayWeather(weather):
    tomorrow = weather['daily']['data'][1]['summary']
    low = weather['daily']['data'][1]['apparentTemperatureMin']
    high = weather['daily']['data'][1]['apparentTemperatureMax']
    precipProb = weather['daily']['data'][1]['precipProbability']
    return tomorrow, low, high, precipProb


def getWeeklyReport(weather):
    weekly = weather['daily']['summary']
    return weekly

# TODO: Modularize the operations within main. Way too much stuff for a driver.
if __name__ == "__main__":
    time = arrow.now("US/Central").format("HH:mm")
    api = setTwitterAuth()
    test = False  # boolean for testing

    try:
        weather = requests.get(darkSkyURL)
    except requests.exceptions.Timeout:
        api.update_status("Hmm, I can't seem to request data from the API "
                          "right now. DM my owner to check for a bug!")
    except requests.exceptions.TooManyRedirects:
        api.update_status("Hmm, the url for the API seems to not work anymore."
                          " Please DM my owner and let him know!")
    except requests.exceptions.RequestException as e:
        api.update_status("Yikes, DM my owner! Error: {}".
                          format(e))

    weather = weather.json()
    tweet = ""

    if time[0:2] == "03":
        currently, temperature, precipProb = getCurrentlyWeather(weather)
        tweet = ("Hey, U! Yeah! U! Try to get some sleep! Naps are a great "
                 "way of managing all nighters if you must. Anyway, "
                 "it's {:.0f}°F. Now try 2 sleep!".format(temperature))
        api.update_status(tweet)

    elif time[0:2] == "06":
        currently, temperature, precipProb = getCurrentlyWeather(weather)
        tweet = ("Today's weather is set to be {} at {:.0f}°F"
                 ", with {:.0f}% of precipitation. Have a great day!".
                 format(
                     currently,
                     temperature,
                     (precipProb * 100)))
        api.update_status(tweet)

    elif time[0:2] == "12":
        weekly = getWeeklyReport(weather)
        tweet = ("Hope you are having a great day! Here's your weekly"
                 " forecast...")
        api.update_status(tweet)
        tweet = ("...{}".format(weekly))
        api.update_status(tweet)

    elif time[0:2] == "18":
        currently, temperature, precipProb = getCurrentlyWeather(weather)
        tweet = ("The current temperature is {:.0f}°F, "
                 "with {:.0f}% of precipitation. Have a great evening!".
                 format(
                     temperature,
                     (precipProb * 100)))
        api.update_status(tweet)

    elif time[:2] == "21":
        tomorrow, low, high, precipProb = getNextDayWeather(weather)
        tweet = ("Good evening, Bulldogs! Here is tomorrow's report: "
                 "{}...".format(tomorrow))
        api.update_status(tweet)
        tweet = ("...with an expected high of {:.0f} and low of {:.0f}°F,"
                 " with a {:.0f}% of precipitation. Try to get some sleep!".
                 format(high, low, precipProb * 100))
        api.update_status(tweet)
        # This is a test clause for debugging crontab, uses random # to prevent
        # duplicate tweets (which twitter would block)
    elif test:
        api.update_status("This is a test tweet for debugging Chron!"
                          " It worked, @EliasJMGarcia! Random #{}".
                          format(random.randint(0, 100000)))
