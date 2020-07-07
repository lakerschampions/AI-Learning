'''
The purpose of this script is to demonstrate how to use the twython package to connect to Twitter\'s  REST API to download tweets from a specific user.

The script has been tested on Mac OS X 10.11.3 (El Capitan) and Python 3.5.
'''

import twython as twy
import os
# import time  # NB: This script is designed to work with one user per request.  If the function is then used for
# multiple users at once, uncomment this line and the lines with time.sleep(3) below.  Twitter allows 300 requests
# per 15 minutes, or 1 per 3 seconds.  Uncommenting avoids tripping the rate limits.
import json


######################
#
# FUNCTION TO USE
#
######################

# Below function will get tweets based on screen_name or ID of user.  If both are given, will use ID.
def getUserTweets(screen_name=None, id_number=None):
    tweets = []

    try:  # This try-except will catch exceptions for protected users
        if screen_name is not None:
            maxID = connection.get_user_timeline(screen_name=[screen_name], count=1)[0][
                'id']  # Current max ID is ID of newest tweet
            try:  # try-catch to avoid error message when all tweets are complete
                for i in range(0, 16):  # Cannot return more than 3200 tweets; 200 at a time equals 16 cycles
                    temp = connection.get_user_timeline(screen_name=[screen_name], count=200,
                                                        max_id=maxID - 1)  # Subtract 1 so that you do not loop through the last tweet, constantly downloading it until i equals 15.
                    maxID = temp[len(temp) - 1]['id']
                    tweets.extend(temp)
                # time.sleep(3)
            except:
                print('Done!')

        if id_number is not None:
            maxID = connection.get_user_timeline(user_id=[id_number], count=1)[0][
                'id']  # Current max ID is ID of newest tweet
            try:  # try-catch to avoid error message when all tweets are complete
                for i in range(0, 16):  # Cannot return more than 3200 tweets; 200 at a time equals 16 cycles
                    temp = connection.get_user_timeline(user_id=[id_number], count=200,
                                                        max_id=maxID - 1)  # Subtract 1 so that you do not loop through the last tweet, constantly downloading it until i equals 15.
                    maxID = temp[len(temp) - 1]['id']
                    tweets.extend(temp)
                    print('On turn', i)
                # time.sleep(3)
            except:
                print('Done!')

    except (twy.TwythonError, twy.TwythonAuthError, twy.TwythonRateLimitError) as e:
        print(e)

    except:
        print('User', id_number, 'is no longer on Twitter')
        pass

    return tweets


# Saves tweets to file
def saveTweets(tweet_object, filename):
    for item in tweet_object:
        with open(filename, 'a') as f:
            json.dump(item, f)
            f.write('\n')


# Saves users and their tweets to file
def saveUsersTweets(tweet_object, filename):
    with open(filename, 'a') as f:
        json.dump(tweet_object, f)
        f.write('\n')


######################
#
# WORK
#
######################
# Set working directory
os.chdir(
    '/Users/chuzhengtian/Desktop/twitter/')  # I set my parent directory to a folder containing subfolders for data, figures,
# and scripts

# Get OAuth credentials.  Need to copy the access token and access token secret as well.  Run this code each time you
# are using twitteR.
APP_KEY = 'E0FnotCZMhpbuO7YtwTkKEdGy'
APP_SECRET = 'sWjudpoeluzvaBu6PBXMSsaQy3agFiVNa2DjgnYmg2TjUp5PRg'
OAUTH_TOKEN = '1273199416476708871-qItbL8Nh3FL5Tv7JniuC8BLQC5D0xg'
OAUTH_TOKEN_SECRET = '06CZqFiq8jM9R7hLRGMbiTC4HVwKHokGECUbGrip6R0LY'

# Connect
connection = twy.Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Download tweets using screen name
tweets = getUserTweets(screen_name='ZacharyST')

# Download tweets using user ID
tweets = getUserTweets(id_number=17367248)

# Download tweets for user with more than 3,200 tweets
tweets_BO = getUserTweets(screen_name='BarackObama')

# Download tweets when have multiple IDs
users = []  # A list of user IDs
# tweets = {}  # Dictionary, each key will be the user.  Uncomment if want to have one large dictionary in memory
for user in users:
    tweets = {}  # Comment out if want to have one large dictionary in memory
    print('On user', user)
    tweets[str(user)] = getUserTweets(id_number=user)
    saveUsersTweets(tweets, filename='/Users/chuzhengtian/Desktop/twitter/Gabon_TweetsOfUsers_v1.txt')

# Write to file when object is list of tweets
saveTweets(tweets, filename='ZST')
saveTweets(tweets_BO, filename='Obama')
