# Number of tweets per hour throughout the day
# Mood of the tweet
# Base off what's trending from twitter
# TODO: Look into Algorithmia and AlchemyAPI

from __future__ import absolute_import, print_function

import tweepy, json, re
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

# Twitter Developer credentials
API_KEY = "UoxZJjMB30XE9ox7PBZe1qqbZ"
API_SECRET = "mDiSSt9IWQFn8IdZAHE8IeYbyqSmIPoN4hI80ezk2JHl0XVazp"
ACCESS_TOKEN = "115831938-Nfbk74K0xheWpWyGN4Cl2Vs9shcRl9CJ3gUdwZYV"
ACCESS_TOKEN_SECRET = "rmPh9burqeUOvzcvE1T2pkQAzkuN3bVxjfUnH4mfi4M2J"

# Locations
galvinize = [-122.451665,37.757656,-122.364925,37.80439]

def removeNonsense(data_json):
    original_data_json = data_json
    # Removes hashtags
    data_json = re.sub(r'#\w+ ?', '', data_json)
    # Removes URLs
    data_json = re.sub(r'http\S+', '', data_json)
    # Removes mentions
    data_json = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",data_json).split())
    # data_json = ' '.join(re.sub("(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+) "," ",data_json).split())
    return data_json

class StdOutListener(StreamListener):
    def on_data(self, data):
        data_json = json.loads(data)
        tweet_text = removeNonsense(data_json["text"])
        tweet_date = data_json["created_at"][11:19]
        print(tweet_date, tweet_text)
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
