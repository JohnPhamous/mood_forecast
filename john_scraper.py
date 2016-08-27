from __future__ import absolute_import, print_function
import tweepy, json, re, Algorithmia
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

tweet_text = None
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

def removeNonsense(data_json):
    original_data_json = data_json
    # Removes hashtags
    data_json = re.sub(r'#\w+ ?', '', data_json)
    # Removes URLs
    data_json = re.sub(r'http\S+', '', data_json)
    # Removes mentions
    data_json = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",data_json).split())
    data_json = emoji_pattern.sub(r'',tweet_text)
    data_json = re.sub(r''.tweet_text)
    # data_json = ' '.join(re.sub("(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+) "," ",data_json).split())
    return data_json

class StdOutListener(StreamListener):
    def on_data(self, data):
        global tweet_text
        data_json = json.loads(data)
        tweet_text = removeNonsense(data_json["text"])
        tweet_date = data_json["created_at"][11:19]
        print(tweet_date, tweet_text)

        #print(tweet_date, tweet_text)

        # Authenticates with Algorithmia
        client = Algorithmia.client('simMN5+/QIIoGAfFTxZtf9uPjHQ1')
        algorithm = client.algo('nlp/SocialSentimentAnalysis/0.1.3')
        print(algorithm.pipe(tweet_text))
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


