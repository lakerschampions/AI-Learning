'''
The purpose of this script is to add location information on top of what Twitter provides.  While Twitter provides location names, it has some weird issues based on the place.type field.  If the place.type is city, use Twitter; if it is admin, neighborhood, or poi, use reverse geocoder.

Designed to work on Python 3.5.

Note that I have written this script to read tweets one at a time.  The reverse_geocoder works much more quickly on a list of tweets than it does on tweets individually.  Computation would therefore be quicker if you can load your tweets into memory and modify the code to read all of the (latitude, longitude) pairs at the same time.
'''

import os
import json
import reverse_geocoder as rg
# To assign city to all GPS points.  Necessary because Twitter does not precisely assign city names.


# Set working directory
os.chdir('/Users/chuzhengtian/Desktop/twitter/')
# I set my parent directory to a folder containing subfolders for data, figures, and scripts.

readin = ['/Users/chuzhengtian/Desktop/twitter/Tweets_2016_10_28_08.txt']  # Files to analyze


for item in readin:
	with open(item, 'r') as f:
		for line in f:
				try:
					# Make string a JSON object
					tweet = line.replace('\n', '')
					tweet = json.loads(tweet)

					if(tweet['place']['place_type'] == 'city'):
						tweet['city'] = tweet['place']['name']

					# NB: Each line in the below if statement is a list enumeration for a one-element list, which is overkill.  But if you change your code to read many tweets at once, you do not have to modify this line.
					if(tweet['place']['place_type'] != 'city'):  # If the place_type is admin, neighborhood, or poi
						tweet['place.bounding_box.SWcorner'] = [item[0] for item in tweet['place']['bounding_box']['coordinates']]  # Use this entry for coordinates.  Twitter adds a polygon when it does not use a specific point, so will take one point of the polygon.
						tweet['place.bounding_box.SWcorner_rg'] = [(item[1], item[0]) for item in tweet['place.bounding_box.SWcorner']]  # reverse_geocoder requires latitude, longitude, so switch from long/lat that Twitter gives.
						tweet['reversegeocode_results'] = rg.search(tweet['place.bounding_box.SWcorner_rg'])  # Perform reverse geocode

						tweet['city'] = [item['name'] for item in tweet['reversegeocode_results']]
						tweet['state'] = [item['admin1'] for item in tweet['reversegeocode_results']]
						tweet['county'] = [item['admin2'] for item in tweet['reversegeocode_results']]

					outpath = item.replace('.txt', '_CorrectLocation.txt')  # File to write out
					with open(outpath, 'a') as outfile:
						json.dump(tweet, outfile)
						outfile.write('\n')
				except:
					pass



