# TruWeatherBot!

This is a weather bot that is set to tweet about weather along with some other things (once I get around to implementing them...).

# As of Now:

the bot currently runs on a chron job on my raspberry pi server and is set to check five past the hour, every hour, of every day. There are currently four tweets that aretriggered by a specific time of every day:
1. 6AM: the bot gives the weather report for the day (summary, temp, precip)
2. 12PM: it will give the 7 day forecast (Summary only)
3. 6PM: It will give an update on the forecast (temp, precip)
4. 10PM: It will give a forecast for the next day (summary, high, low)

# TODO:
1. Create method that checks timeline for repeate messages and deletes them before tweeting 
2. More message variety overall, different greetings, etc
3. Inspiration messages! Quotes, etcetera
4. School events (this will probably be a much bigger problem, so for later when i have a lot more time)
