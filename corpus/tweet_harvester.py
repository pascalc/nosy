from tornado.httpclient import HTTPClient, HTTPRequest, HTTPError
import simplejson
import pymongo

class TweetHarvester:
    # Twitter info
    STREAM_URL = "https://stream.twitter.com/1/statuses/sample.json"
    TWITTER_USERNAME = "YAP_nosy"
    TWITTER_PASSWORD = "yetanotherproject"
    tweet_count = 0

    # PyMongo
    db = pymongo.Connection()['nosy']

    @classmethod
    def harvest(cls):
        req = HTTPRequest(
            cls.STREAM_URL, 
            method="GET",
            auth_username=cls.TWITTER_USERNAME,
            auth_password=cls.TWITTER_PASSWORD, 
            streaming_callback=cls.handle_tweet_stream)

        client = HTTPClient()
        client.fetch(req)

    @classmethod
    def handle_tweet_stream(cls, response):
        try:
            json = simplejson.loads(response)
        except ValueError:
            return

        cls.insert_into_db(json)

    @classmethod
    def insert_into_db(cls, json):
        cls.db.tweets.insert(json)
        cls.tweet_count += 1
        print cls.tweet_count

if __name__ == "__main__":
    try:
        TweetHarvester.harvest()
    except HTTPError:
        print "Done!"
        