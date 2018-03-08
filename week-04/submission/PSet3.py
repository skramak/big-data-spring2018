#import necessary packages
import jsonpickle
import tweepy
import pandas as pd
import os
os.listdir()
os.chdir('/users/Saritha/Desktop/Github/big-data-spring2018/week-04')
#add in twitter keys, authentication
from twitter_keys import api_key, api_secret

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)

#parse tweets for readability
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

#add scraper
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
  print ("Downloaded {tweet_count} tweets.")
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'tweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 2000

#call scraper function
tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

#tweets to .json file
tweets.to_json('/users/Saritha/Desktop/Github/big-data-spring2018/week-04/data/tweets.json')
#Check how many tweets
tweets.shape
tweets.head()
#import numpy and matlobplot - enable inline display
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

#read in tweets into dataframe
df=pd.read_json('/users/Saritha/Desktop/Github/big-data-spring2018/week-04/data/tweets.json')


#define variable names - clean locations
bos_list = df[df['location'].str.contains("Boston", case=False)]['location']
cambridge_list=df[df['location'].str.contains("Cambridge", case=False)]['location']
somerville_list=df[df['location'].str.contains("Somerville", case=False)]['location']
jp_list=df[df['location'].str.contains("Jamaica Plain", case=False)]['location']
dorchester_list=df[df['location'].str.contains("Dorchester", case=False)]['location']
johnston_list=df[df['location'].str.contains("johnston", case=False)]['location']
somerset_list=df[df['location'].str.contains("Somerset", case=False)]['location']
chicago_list=df[df['location'].str.contains("Chicago", case=False)]['location']
allston_list=df[df['location'].str.contains("Allston", case=False)]['location']
brighton_list=df[df['location'].str.contains("Brighton", case=False)]['location']

#replace locations
df['location'].replace(bos_list, 'Boston, MA', inplace = True)
df['location'].replace(cambridge_list, 'Cambridge, MA', inplace = True)
df['location'].replace(somerville_list, 'Somerville, MA', inplace = True)
df['location'].replace(jp_list, 'Boston, MA', inplace = True)
df['location'].replace(dorchester_list, 'Boston, MA', inplace = True)
df['location'].replace(johnston_list, 'Johnston, RI', inplace = True)
df['location'].replace(somerset_list, 'Somerset, MA', inplace = True)
df['location'].replace(chicago_list, 'Chicago, IL', inplace = True)
df['location'].replace(allston_list, 'Boston, MA', inplace = True)
df['location'].replace(brighton_list, 'Boston, MA', inplace = True)

#remove retweets/duplicates
df[df.duplicated(subset = 'content', keep = False)]
df.drop_duplicates(subset = 'content', keep = False, inplace = True)

#check unique values, total by location
df['location'].unique()
df['location'].value_counts()


#Remove missing tweet locations
has_location=df[df['location'] != ""]
has_location['location'].value_counts()

#Take only the cleaned up locations, which are all locations that have a count greater than 10
#Put value counts of locations into a new data frame
location_count_frame= has_location['location'].value_counts().to_frame()
location_count_frame.head()
#Take locations with counts over 10 and place into another variable
q2_chart = location_count_frame[location_count_frame['location']>10]
q2_chart.shape

#Plotting the pie chart
q2_chart.plot(kind='pie', y='location', fontsize=14, title='User-Named Locations', sharey=False)


#plotting scatter plot of geolocated tweets
tweets_geo = df[df['lon'].notnull() & df['lat'].notnull()]
len(tweets_geo)
len(df)
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()

#search term scraping
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


# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'tweets_search.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 2000

#call tweet scraper, search term of 'storm'
tweets_search= get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name,
  search_term = 'storm'
)

#tweets to JSON
tweets_search.to_json('/users/Saritha/Desktop/Github/big-data-spring2018/week-04/data/tweets_search.json')

#tweets to dataframe
tweets_search.shape
df_s=pd.read_json('/users/Saritha/Desktop/Github/big-data-spring2018/week-04/data/tweets_search.json')

#clean tweets for location
df_s['location'].unique()

sbos_list = df_s[df_s['location'].str.contains("Boston", case=False)]['location']
scambridge_list=df_s[df_s['location'].str.contains("Cambridge", case=False)]['location']
ssomerville_list=df_s[df_s['location'].str.contains("Somerville", case=False)]['location']
sjp_list=df_s[df_s['location'].str.contains("Jamaica Plain", case=False)]['location']
sdorchester_list=df_s[df_s['location'].str.contains("Dorchester", case=False)]['location']
sjohnston_list=df_s[df_s['location'].str.contains("johnston", case=False)]['location']
ssomerset_list=df_s[df_s['location'].str.contains("Somerset", case=False)]['location']
schicago_list=df_s[df_s['location'].str.contains("Chicago", case=False)]['location']
sallston_list=df_s[df_s['location'].str.contains("Allston", case=False)]['location']
sbrighton_list=df_s[df_s['location'].str.contains("Brighton", case=False)]['location']
sroxbury_list=df_s[df_s['location'].str.contains("Roxbury", case=False)]['location']
swaltham_list=df_s[df_s['location'].str.contains("Waltham", case=False)]['location']
scharlestown_list=df_s[df_s['location'].str.contains("Charlestown", case=False)]['location']
smedford_list=df_s[df_s['location'].str.contains("Medford", case=False)]['location']
sworcester_list=df_s[df_s['location'].str.contains("Worcester", case=False)]['location']

df_s['location'].replace(sbos_list, 'Boston, MA', inplace = True)
df_s['location'].replace(scambridge_list, 'Cambridge, MA', inplace = True)
df_s['location'].replace(ssomerville_list, 'Somerville, MA', inplace = True)
df_s['location'].replace(sjp_list, 'Boston, MA', inplace = True)
df_s['location'].replace(sdorchester_list, 'Boston, MA', inplace = True)
df_s['location'].replace(sjohnston_list, 'Johnston, RI', inplace = True)
df_s['location'].replace(ssomerset_list, 'Somerset, MA', inplace = True)
df_s['location'].replace(schicago_list, 'Chicago, IL', inplace = True)
df_s['location'].replace(sallston_list, 'Boston, MA', inplace = True)
df_s['location'].replace(sbrighton_list, 'Boston, MA', inplace = True)
df_s['location'].replace(sroxbury_list, 'Boston, MA', inplace = True)
df_s['location'].replace(swaltham_list, 'Waltham, MA', inplace = True)
df_s['location'].replace(scharlestown_list, 'Charlestown, MA', inplace = True)
df_s['location'].replace(smedford_list, 'Medford, MA', inplace = True)
df_s['location'].replace(sworcester_list, 'Worcester, MA', inplace = True)

df_s['location'].unique()

#drop duplicates
df_s[df_s.duplicated(subset = 'content', keep = False)]
df_s.drop_duplicates(subset = 'content', keep = False, inplace = True)

#scatterplot of geolocations
tweets_geo_s = df_s[df_s['lon'].notnull() & df_s['lat'].notnull()]
len(tweets_geo_s)
len(df_s)
plt.scatter(tweets_geo_s['lon'], tweets_geo_s['lat'], s = 25)
plt.show()

#export both to a .csv file
df_s.to_csv('twitter_searchterm.csv', sep=',', encoding='utf-8')
df.to_csv('twitter_nosearchterm.csv', sep=',', encoding='utf-8')
