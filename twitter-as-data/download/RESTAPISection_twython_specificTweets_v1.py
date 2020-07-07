"""
The purpose of this script is to demonstrate how to use the twython package to connect to Twitter\'s  REST API to download tweets when the tweet identification number is known.

The script has been tested on Mac OS X 10.11.3 (El Capitan) and Python 3.5.
"""

import pandas as pd
import twython as twy
import os
import json

# Set working directory
os.chdir(
    '/Users/chuzhengtian/Desktop/twitter/')  # I set my parent directory to a folder containing subfolders for data,
# figures, and scripts

# Get OAuth credentials.  Need to copy the access token and access token secret as well.  Run this code each time you
# are using twitteR.
APP_KEY = 'E0FnotCZMhpbuO7YtwTkKEdGy'
APP_SECRET = 'sWjudpoeluzvaBu6PBXMSsaQy3agFiVNa2DjgnYmg2TjUp5PRg'
OAUTH_TOKEN = '1273199416476708871-qItbL8Nh3FL5Tv7JniuC8BLQC5D0xg'
OAUTH_TOKEN_SECRET = '06CZqFiq8jM9R7hLRGMbiTC4HVwKHokGECUbGrip6R0LY'

# Connect
connection = twy.Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Load tweet IDs.  This step assumes you already have the tweet IDs, such as from here:
# http://dfreelon.org/2012/02/11/arab-spring-twitter-data-now-available-sort-of/
tweet_IDs = pd.read_csv('/Users/chuzhengtian/Desktop/twitter/algeria_ids.csv', names=['ID','userid'], dtype={'ID': 'str'})

# Load one tweet, the newest
firstTweet = connection.show_status(id=tweet_IDs['ID'][0])


# Multiple tweets. Below function splits a list into chunks.  It is taken from
# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks?page=2&tab=votes#tab-top
def split_list(the_list, chunk_size):
    result_list = []
    while the_list:
        result_list.append(the_list[:chunk_size])
        the_list = the_list[chunk_size:]
    return result_list


# Figure out how long to pause in between each submission.  Is 0 if will not hit the rate limit, the necessary pause
# if will
submissionsPerRequest = 100  # Find this value at https://dev.twitter.com/rest/reference/get/statuses/show/%3Aid.

window_minutes = 15  # The length of Twitter's rate limit window, in minutes.
requestsPer15Window = 180
delay = (
                    window_minutes * 60) / requestsPer15Window  # Calculates how many seconds per request per window.
#  This number will tell the loop how many seconds to sleep.

chunkedTweets = split_list(tweet_IDs['ID'].tolist(), submissionsPerRequest)  # List of lists, each sublist is tweet IDs
tweets = []  # Empty object that tweets will feed into

# Download tweets
for chunk in chunkedTweets:
    print('-', end='')
    temp = connection.lookup_status(id=chunk)  # Notice that this is lookup_status and not show_status
    tweets.extend([item for item in temp])
# time.sleep(delay)  # Pause execution so do not hit rate limits.  Not needed when downloading tweets for 1 user
# because Twitter allows 18,000 tweets per 15 minutes.

# Save out, all on one line.  This version is what is used for other examples written in Python.
with open('/Users/chuzhengtian/Desktop/twitter/tweets_downloadedTwython.txt', 'w') as outfile:
    json.dump(tweets, outfile)
    print("saved")
