from tweepy.streaming import StreamListener
import time
import json
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client['tweets']
tweets = db.tweets

class listener(StreamListener):
    
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            tweet = json.loads(data)
            hashtags = []
        
            country = tweet['place']['country'] if tweet['place'] is not None else ""
            country_code = tweet['place']['country_code'] if tweet['place'] is not None else ""
        
            doc = {
                "screen_name": tweet['user']['screen_name'],
                "user_name": tweet['user']['name'],
                "location": tweet['user']['location'],
                "source_device": tweet['source'],
                "is_retweeted": tweet['retweeted'],
                "retweet_count": tweet['retweet_count'],
                "country": country,
                "country_code": country_code,
                "reply_count": tweet['reply_count'],
                "favorite_count": tweet['favorite_count'],    # likes
                "tweet_text": tweet['text'],
                "created_at": tweet['created_at'],
                "timestamp_ms": tweet['timestamp_ms'],
                "lang": tweet['lang'],
                "hashtags": hashtags,
                "quote_count":tweet['quote_count'],
            }
            tweet_text = tweets.insert_one(doc).inserted_id
            print(tweet_text)
            return True
        else:
            print("Stream Stopped")
            return False

    def on_error(self, status):
        print(status)