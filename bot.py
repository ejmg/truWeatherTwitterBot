"""
This is a bot that tells the weather & gives inspirational quotes for the
Truman State University area.

author: elias g
version 17.11.16
"""

# IMPORT DECLARATIONS

import tweepy as ty
import random
import arrow
import requests
from truSecret import (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                       ACCESS_SECRET, DARK_SKY_SECRET)

# CONSTANTS

# lat and long for Truman State University
LATITUDE = "40.1876"
LONGITUDE = "-92.5819"

# sets the request url with the auth token, coordinates, excludes hourly
# minutely, and flags values with ?exclude= block
DARK_SKY_URL = ("https://api.darksky.net/forecast/{}/{},{}"
                "?exclude=hourly,minutely,flags".format(DARK_SKY_SECRET,
                                                        LATITUDE,
                                                        LONGITUDE))


def setTwitterAuth():
    """
    obtains authorization from twitter API
    """
    # sets the auth tokens for twitter using tweepy
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api


def getWeather():
    try:
        weather = requests.get(DARK_SKY_URL)
    except requests.exceptions.Timeout:
        api.update_status("Hmm, I can't seem to request data from the API "
                          "right now. DM my owner to check for a bug!")
        return None
    except requests.exceptions.TooManyRedirects:
        api.update_status("Hmm, the url for the API seems to not work anymore."
                          " Please DM my owner and let him know!")
    except requests.exceptions.RequestException as e:
        api.update_status("Yikes, DM my owner! Error: {}".
                          format(e))
    finally:
        return weather


def deleteDuplicates(api, tweet):
    """
    takes to-be tweet and deletes any exact duplicates from the last 20 on
    the bot's timeline. Added benefit of keeping timeline short for upkeep.
    """
    oldTweets = api.user_timeline("@TrumanWeather", count=36)
    for oldTweet in oldTweets:
        if oldTweet.text == tweet:
            api.destroy_status(oldTweet.id)


def getCurrentlyWeather(weather):
    """
    gets all major indicators from 'currently', what is used depends on the
    tweet itself.
    """
    summary = weather['currently']['summary']
    cloudCover = weather['currently']['cloudCover']
    visibility = weather['currently']['visibility']
    windSpeed = weather['currently']['windSpeed']
    temperature = weather['currently']['temperature']
    apparentTemperature = weather['currently']['apparentTemperature']
    precipProb = weather['currently']['precipProbability']
    return (summary, cloudCover, visibility, windSpeed, temperature,
            apparentTemperature, precipProb)


def getNextDayWeather(weather):
    """
    gets all major indicators for the next day from 'daily', what is used
    depends on the tweet itself
    """
    summary = weather['daily']['data'][1]['summary']
    low = weather['daily']['data'][1]['apparentTemperatureMin']
    high = weather['daily']['data'][1]['apparentTemperatureMax']
    visibility = weather['daily']['data'][1]['visibility']
    windSpeed = weather['daily']['data'][1]['windSpeed']
    precipProb = weather['daily']['data'][1]['precipProbability']
    return summary, low, high, visibility, windSpeed, precipProb


def getWeeklyReport(weather):
    """
    gets the weekly report from the 'daily' category
    """
    weekly = weather['daily']['summary']
    return weekly


# TODO: Modularize the operations within main. Way too much stuff for a driver.
if __name__ == "__main__":
    time = arrow.now("US/Central").format("HH:mm")
    api = setTwitterAuth()
    test = False  # boolean for testing

    weather = getWeather()

    weather = weather.json()
    tweet = ""

    if time[0:2] == "03":
        (summary, cloudCover, visibility, windSpeed, temperature,
         apparentTemperature, precipProb) = getCurrentlyWeather(weather)
        tweet = ("Hey, U! Yeah! U! Try to get some sleep! Naps are a great "
                 "way of managing all nighters if you must. Anyway, "
                 "it's {:.0f}°F. Now try 2 sleep!".format(temperature))
        deleteDuplicates(api, tweet)
        api.update_status(tweet)

    elif time[0:2] == "06":
        (summary, cloudCover, visibility, windSpeed, temperature,
         apparentTemperature, precipProb) = getCurrentlyWeather(weather)
        tweet = ("Today's weather is set to be {} at {:.0f}°F"
                 ", with {:.0f}% of precipitation. Have a great day!".
                 format(
                     summary,
                     temperature,
                     (precipProb * 100)))
        deleteDuplicates(api, tweet)
        api.update_status(tweet)

    elif time[0:2] == "12":
        weekly = getWeeklyReport(weather)
        tweet = ("Hope you are having a great day! Here's your weekly"
                 " forecast...")
        deleteDuplicates(api, tweet)
        api.update_status(tweet)
        tweet = ("...{}".format(weekly))
        deleteDuplicates(api, tweet)
        api.update_status(tweet)

    elif time[0:2] == "18":
        (summary, cloudCover, visibility,
         windSpeed, temperature, apparentTemperature,
         precipProb) = getCurrentlyWeather(weather)
        tweet = ("The current temperature is {:.0f}°F, "
                 "with {:.0f}% of precipitation. Have a great evening!".
                 format(
                     temperature,
                     (precipProb * 100)))
        deleteDuplicates(api, tweet)
        api.update_status(tweet)

    elif time[:2] == "21":
        (summary, low, high, visibility, windSpeed,
         precipProb) = getNextDayWeather(weather)
        tweet = ("Good evening, Bulldogs! Here is tomorrow's report: "
                 "{}...".format(summary))
        deleteDuplicates(api, tweet)
        api.update_status(tweet)
        tweet = ("...with an expected high of {:.0f} and low of {:.0f}°F,"
                 " with a {:.0f}% of precipitation. Try to get some sleep!".
                 format(high, low, precipProb * 100))
        deleteDuplicates(api, tweet)
        api.update_status(tweet)
        # This is a test clause for debugging crontab, uses random # to prevent
        # duplicate tweets (which twitter would block)
    elif test:
        api.update_status("This is a test tweet for debugging Chron!"
                          " It worked, @EliasJMGarcia! Random #{}".
                          format(random.randint(0, 100000)))
