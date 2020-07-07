'''
The purpose of this code is to demonstrate how to use twython to connection to Twitter's streaming API and download tweets containing certain keywords.

The script has been tested on Mac OS X 10.11.3 (El Capitan) and Python 3.5.

NB: For examples of the tweepy library, see the following tutorials:
	- http://socialmedia-class.org/twittertutorial.html
	- https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
	- http://adilmoujahid.com/posts/2014/07/twitter-analytics/
	- http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
'''

# Import libraries
import twython as twy
import json
import datetime as dt

# Key, secret, token, token_secret for one of my developer accounts.
# Update with your own strings as necessary
APP_KEY = 'E0FnotCZMhpbuO7YtwTkKEdGy'
APP_SECRET = 'sWjudpoeluzvaBu6PBXMSsaQy3agFiVNa2DjgnYmg2TjUp5PRg'
OAUTH_TOKEN = '1273199416476708871-qItbL8Nh3FL5Tv7JniuC8BLQC5D0xg'
OAUTH_TOKEN_SECRET = '06CZqFiq8jM9R7hLRGMbiTC4HVwKHokGECUbGrip6R0LY'


# Make class
class MyStreamer(twy.TwythonStreamer):
    fileDirectory = '/Users/chuzhengtian/Desktop/twitter/'
    # Any result from this class will save to this directory

    stop_time = dt.datetime.now() + dt.timedelta(minutes=3)

    # Connect to Twitter for 60 minutes.  Comment out if do not want it timed.

    def on_success(self, data):
        if dt.datetime.now() > self.stop_time:
            # Once minutes=60 have passed, stop.  Comment out these 2 lines if do not want timed connection.
            raise Exception('Time expired')

        fileName = self.fileDirectory + 'keywordsTweets_' + dt.datetime.now().strftime("%Y_%m_%d_%H") + '.txt'
        # File name includes date out to hour.
        open(fileName, 'a').write(json.dumps(data) + '\n')  # Append tweet to the file

    # NB: Because the file name includes the hour, a new file is created automatically every hour.

    def on_error(self, status_code, data):
        fileName = self.fileDirectory + dt.datetime.now().strftime("%Y_%m_%d_%H") + '_Errors.txt'
        open(fileName, 'a').write(json.dumps(data) + '\n')


# Make function.  Tracks key words.
def streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=['LeBron James, Steph Curry, NBA, basketball, Warriors, GSW, Cavaliers, espn com'])


# Execute
streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
