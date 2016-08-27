# Number of tweets per hour throughout the day
# Mood of the tweet
# Base off what's trending from twitter
# TODO: Look into Algorithmia and AlchemyAPI

from __future__ import absolute_import, print_function

import tweepy, json, re
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

# Twitter Developer credentials
API_KEY = "UoxZJjMB30XE9ox7PBZe1qqbZ"
API_SECRET = "mDiSSt9IWQFn8IdZAHE8IeYbyqSmIPoN4hI80ezk2JHl0XVazp"
ACCESS_TOKEN = "115831938-Nfbk74K0xheWpWyGN4Cl2Vs9shcRl9CJ3gUdwZYV"
ACCESS_TOKEN_SECRET = "rmPh9burqeUOvzcvE1T2pkQAzkuN3bVxjfUnH4mfi4M2J"

# Locations
galvinize = [-122.451665,37.757656,-122.364925,37.80439]
tweet_data = []

class StdOutListener(StreamListener):
    def on_data(self, data):
        # print(data)
        tweet_data = data
        print(tweet_data[0])
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener()
    # Authenticates with Twitter
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)
    stream.filter(locations = galvinize)
    # stream.filter(track = ['test'])
