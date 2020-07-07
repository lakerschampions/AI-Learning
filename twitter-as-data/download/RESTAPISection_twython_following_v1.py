'''
The purpose of this script is to demonstrate how to use the twython package to connect to Twitter\'s  REST API to download the accounts an account followers (the account's friends, in Twitter terminology).

The script has been tested on Mac OS X 10.11.3 (El Capitan) and Python 3.5.

NB: The get_friends function uses the screen_name of the account in which you are interested.  Best practice is to use the ID number of the account whose friends you want, as it will not change if the screen name changes.  If you use the ID number, replace screen_name=<user screen name> with user_id= <user ID number>.  This script provides two lines of code which will find the ID number of the screen name of interest.
'''
import twython as twy
import os
import time
import json

# Set working directory
os.chdir(
    '/Users/chuzhengtian/Desktop/twitter/')  # I set my parent directory to a folder containing subfolders for data, figures, and scripts

# Get OAuth credentials.  Need to copy the access token and access token secret as well.  Run this code each time you are using twitteR.
APP_KEY = 'E0FnotCZMhpbuO7YtwTkKEdGy'
APP_SECRET = 'sWjudpoeluzvaBu6PBXMSsaQy3agFiVNa2DjgnYmg2TjUp5PRg'
OAUTH_TOKEN = '1273199416476708871-qItbL8Nh3FL5Tv7JniuC8BLQC5D0xg'
OAUTH_TOKEN_SECRET = '06CZqFiq8jM9R7hLRGMbiTC4HVwKHokGECUbGrip6R0LY'

# Connect
connection = twy.Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


# Function to get followers
def get_friends(user, cursor, i=1, total_friends=None):
    try:
        print('Getting friends for %s' % user)
        while cursor != '0':  # Cursor is a key returned by Twitter when there are more than 5,000 followers
            print('Cursoring through friends.  On cursor %s' % cursor)

            temp = connection.get_friends_ids(screen_name=user, count=5000,
                                              cursor=cursor)  # Returns dictionary of cursors and IDs, with IDs as a list of integers

            for entry in temp['ids']:  # Write each ID to file.  I have chosen to write as an edgelist.
                with open('/Users/chuzhengtian/Desktop/twitter/FriendsOf_' + user + '.txt', 'a') as f:
                    f.write(user + ',')
                    f.write(str(entry) + '\n')
                    # Each ID is an integer, I make a string in order to write the newline string on the same line of code.

            cursor = temp['next_cursor_str']

    except twy.TwythonRateLimitError:

        downloaded = 15 * 5000 * i  # Will be used to help monitor progress
        i += 1

        wait = 60 * 15 + 2  # how many seconds to wait

        print('Stopped by Twitter rate limits.  Sleeping for %s minutes' % (wait / 60.0))

        if total_friends is not None:  # If the user provides total number of followers, print the below
            print('Have downloaded %s of %s friends' % (downloaded, total_friends))

        print('It is now %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))  # So you know when to come back

        time.sleep(wait)  # Pause execution for wait seconds

        get_friends(user=user, cursor=cursor, total_friends=total_friends)  # Recursive, starts execution again

    except twy.TwythonError as e:
        print(e)

        get_friends(user=user, cursor=cursor, total_friends=total_friends)  # Recursive, starts execution again

        i += 1


def openIDs(user):  # Read list of follower IDs
    id_file = '/Users/chuzhengtian/Desktop/twitter/FriendsOf_' + user + '.txt'
    ids = []
    with open(id_file) as f:
        temp = f.read().splitlines()

    for item in temp:
        ids.append(item.split(',')[1])  # First entry is screen name of user, 2nd entry is ID of follower

    return ids


def hydrateFriends(user, IDs, start,
                   end):  # Function to take saved user IDs and get their hydrated objects (user profile)
    try:
        temp = connection.lookup_user(user_id=IDs[start:end])
        for entry in temp:
            # followers_hydrated[entry['id_str']] = entry
            my_dict = {entry['id_str']: entry}
            with open('/Users/chuzhengtian/Desktop/twitter/Friends_Dictionary_Hydrated_' + user + '.txt', 'a') as f:
                json.dump(my_dict, f)
                f.write('\n')

    except twy.TwythonRateLimitError:
        wait = 60 * 12  # 180 requests per 15 minutes, 12 per minute.
        display = wait / 60.0

        print('Stopped by Twitter Rate Limits. Sleeping for %s' % display)
        time.sleep(wait)
        hydrateFriends(user=user, IDs=IDs, start=start, end=end)

    except twy.TwythonError as e:
        print(e)
        # dict2 = {entry['id_str']:e}
        # with open(output+'PassedFriends_HyradteFriends.txt','a') as f:
        # 	json.dump(dict2,f)
        # 	f.write('\n')
        hydrateFriends(user=user, IDs=IDs, start=start, end=end)


# Below finds the user ID number of the screen_name of interest Get followers of account without very many followers
account = connection.lookup_user(screen_name=['ZacharyST'])
account_id = account[0]['id']  # The ID number for the user in the account object

# Get followers for an account without many followers
get_friends(user='ZacharyST',
            cursor=-1)
# No object saved to because the function writes to file instead.  cursor needs to be any number not equal to 0.

# Get followers for a very popular account
account = connection.lookup_user(screen_name=['BarackObama'])
account_friends = account[0]['followers_count']

get_friends(user='BarackObama', cursor=-1, total_friends=account_friends)

# Hydrate friends list.  Below function just get list of Twitter IDs.
ids = openIDs(user='BarackObama')

total = len(ids)
i = 0
while i < total:
    print("On friend %d" % i)
    j = i + 100
    hydrateFriends(user='BarackObama', IDs=ids, start=i, end=j)
    i += 100
    pct_done = (j / total) * 100
    print("Finished %f10 percent" % pct_done)
