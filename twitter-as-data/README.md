## Download tweets' text from twitter using tweepy
"""
import tweepy
consumer_key = 'E0FnotCZMhpbuO7YtwTkKEdGy'
consumer_secret = 'sWjudpoeluzvaBu6PBXMSsaQy3agFiVNa2DjgnYmg2TjUp5PRg'
access_token = '1273199416476708871-qItbL8Nh3FL5Tv7JniuC8BLQC5D0xg'
access_token_secret = '06CZqFiq8jM9R7hLRGMbiTC4HVwKHokGECUbGrip6R0LY'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search,q='COVID19').items(10):
    print(tweet.text)
"""
