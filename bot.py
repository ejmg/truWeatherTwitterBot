# !/bin/python3
"""
This is a bot that tells the weather & gives inspirational quotes for the
Truman State University area.

author: elias g
version 17.11.16
"""

import tweepy as ty
import time
import sys
from truSecret import consumerKey, consumerSecret, accessToken, accessSecret

auth = ty.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)
api = ty.API(auth)

api.update_status("In the beginning there was darkness..."
                  "with a chance of rain!")
