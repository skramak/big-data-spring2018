import jsonpickle
import tweepy
import pandas as pd

import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret
auth = tweepy.AppAuthHandler(api_key, api_secret)

api = tweepy.API(auth, wait_on_rate_limit= True, wait_on_rate_limit_notify=True)

def auth(key, secret):
    auth = tweepy.AppAuthHandler(key, secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #print error if there is an authentication problem

    if(not api):
        print ('Cannot authenticate')
        sys.exist(-1)
    else:
        return api

api = auth(api_key, api_secret)

def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        if write == True:
            with open(out_file, 'w') as f:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '1mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 200

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

def parse_tweet(tweet):
  p = pd.Series()
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)
