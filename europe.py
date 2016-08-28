from __future__ import absolute_import, print_function
import tweepy, json, re, Algorithmia
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

# Twitter Developer credentials
API_KEY = "UoxZJjMB30XE9ox7PBZe1qqbZ"
API_SECRET = "mDiSSt9IWQFn8IdZAHE8IeYbyqSmIPoN4hI80ezk2JHl0XVazp"
ACCESS_TOKEN = "115831938-Nfbk74K0xheWpWyGN4Cl2Vs9shcRl9CJ3gUdwZYV"
ACCESS_TOKEN_SECRET = "rmPh9burqeUOvzcvE1T2pkQAzkuN3bVxjfUnH4mfi4M2J"

# Plotly Authentication
plotly.tools.set_credentials_file(username = 'PhamousJ', api_key = 'csc7od4qv1')
stream_token1 = 'tx29w0wrch'
stream_token2 = 'p4hfwgvo54'
stream_1 = dict(token = stream_token1, maxpoints = 200)
stream_2 = dict(token = stream_token2, maxpoints = 200)
trace_1 = go.Scatter(x = [], y = [], mode = 'lines+markers', stream = stream_1,
                    name = "Live Tweets")
trace_2 = go.Scatter(x = [], y = [], mode = 'lines', stream = stream_2, name =
                    "Average")
data = go.Data([trace_1, trace_2])
# layout = go.Layout(title = "San Francisco")
fig = go.Figure(data = data)
py.plot(fig, filename = "USA Mood")
s = py.Stream(stream_token1)
s2 = py.Stream(stream_token2)
s.open()
s2.open()

# Locations
galvinize = [-125.4,23.8,-65.0,49.6]

tweet_text = None
tweet_counter = 1.0
tweet_time = None
mood = 0.0
mood_average = 0.0

def removeNonsense(data_json):
    original_data_json = data_json
    # Removes hashtags
    data_json = re.sub(r'#\w+ ?', '', data_json)
    # Removes URLs
    data_json = re.sub(r'http\S+', '', data_json)
    # Removes mentions
    data_json = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",data_json).split())
    return data_json

class StdOutListener(StreamListener):
    def on_data(self, data):
        global tweet_text
        global tweet_counter
        global tweet_time
        global mood_average
        global mood

        data_json = json.loads(data)
        tweet_text = removeNonsense(data_json["text"])
        tweet_time = data_json["created_at"][11:19]

        # Authenticates with Algorithmia
        client = Algorithmia.client('simMN5+/QIIoGAfFTxZtf9uPjHQ1')
        algorithm = client.algo('nlp/SocialSentimentAnalysis/0.1.3')
        text_formatted = '{"sentence":' +  tweet_text + '}'
        analyzed_text = algorithm.pipe(text_formatted.encode("utf-8"))
        # analyzed_text = algorithm.pipe(text_formatted)
        # print(analyzed_text)
        analyzed_text_dict = analyzed_text[0]
        print("Tweet:", tweet_text)
        print("Time:", tweet_time)
        current_mood = analyzed_text_dict.items()[4][1]
        print("Current mood:", current_mood)
        if current_mood != 0:
            # Adds to graph
            s.write(dict(x = tweet_time, y = current_mood, text = tweet_text))
            s2.write(dict(x = tweet_time, y = mood_average))
            mood += current_mood
            mood_average = mood / tweet_counter 
            print("Average mood out of {}: {}\n".format(tweet_counter, mood_average))
            tweet_counter += 1.0
        else:
            print("Tweet is ignored: too short or made no sense\n")
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


