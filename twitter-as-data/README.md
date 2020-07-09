## Download tweets' text from twitter 
By using <em>tweepy</em>, you can easily catch the text of tweets with specific <strong>hashtags</strong>.
```
import tweepy

consumer_key = 'xxxxxx'
consumer_secret = 'xxxxxxx'
access_token = 'xxxxxxx'
access_token_secret = 'xxxxxxx'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)

CovidList = []
for tweet in tweepy.Cursor(api.search,q='COVID19').items(10):
    CovidList.append(tweet.text)
```
Texts are stored in the <em>CovidList</em>.
