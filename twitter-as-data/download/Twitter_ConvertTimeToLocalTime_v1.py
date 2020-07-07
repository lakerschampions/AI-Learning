'''
The purpose of this script is to convert a tweet's timestamp to local time, as Twitter gives the UTC time of a stamp.

Designed to work on Python 3.5.
'''

import json
from timezonefinder import TimezoneFinder
import pytz
import datetime as dt
import os

# Set working directory
os.chdir('/Users/chuzhengtian/Desktop/twitter/')
# I set my parent directory to a folder containing subfolders for data, figures, and scripts.

# Files to read in
readin = ['/Users/chuzhengtian/Desktop/twitter/Tweets_2020_07_07_15.txt']

# If tweets contain GPS coordinates
for item in readin:
	with open(item, 'r') as f:
		for line in f:
				try:
					# Make string a JSON object
					tweet = line.replace('\n', '')
					tweet = json.loads(tweet)

					# Get GPS pair, SW corner of bounding box from Twitter
					longitude = tweet['place']['bounding_box']['coordinates'][0][0][0]
					latitude = tweet['place']['bounding_box']['coordinates'][0][0][1]

					# Get timezones
					tf = TimezoneFinder()
					zone = tf.timezone_at(lng=longitude, lat=latitude)  # Gives string of name of timezone
					timezone = pytz.timezone(zone)  # Convert string to pytz format

					# Make local time
					utc_time = dt.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)  # Convert tweet timestamp to datetime object
					local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)  # Get local time as datetime object

					tweet['local_time_twitterStyle'] = local_time.strftime(format='%a %b %d %H:%M:%S +0000 %Y')
					tweet['local_time_nice'] = local_time.strftime('%Y-%m-%d %H:%M:%S')

					outpath = item.replace('.txt', '_CorrectLocalTime.txt')  # File to write out
					with open(outpath, 'a') as outfile:
						json.dump(tweet, outfile)
						outfile.write('\n')
				except:
					pass


# If tweets do not contain GPS coordinates:
for item in readin:
	with open(item, 'r') as f:
		for line in f:
				try:
					# Make string a JSON object
					tweet = line.replace('\n', '')
					tweet = json.loads(tweet)

					# Correct for user timezone
					utc_time = dt.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
					local_time = utc_time + dt.timedelta(seconds=tweet['user']['utc_offset'])
					# Subtract hours based on timezone from profile

					tweet['local_time_twitterStyle'] = local_time.strftime(format='%a %b %d %H:%M:%S +0000 %Y')
					tweet['local_time_nice'] = local_time.strftime('%Y-%m-%d %H:%M:%S')

					outpath = item.replace('.txt', '_ProfileLocalTime.txt')  # File to write out
					with open(outpath, 'a') as outfile:
						json.dump(tweet, outfile)
						outfile.write('\n')
				except:
					pass

