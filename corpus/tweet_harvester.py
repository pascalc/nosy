from tornado.httpclient import HTTPClient, HTTPRequest, HTTPError
import simplejson

from harvester import Harvester, HarvestingComplete
from classification_object import ClassificationObject

class TweetHarvester(Harvester):
    # Twitter info
    STREAM_URL = "https://stream.twitter.com/1/statuses/sample.json"
    TWITTER_USERNAME = "YAP_nosy"
    TWITTER_PASSWORD = "yetanotherproject"

    def __init__(self, workers=4):
        super(TweetHarvester, self).__init__(workers)
        self.tweet_count = 0

    def harvest(self, limit=500):
        req = HTTPRequest(
            self.STREAM_URL, 
            method="GET",
            auth_username=self.TWITTER_USERNAME,
            auth_password=self.TWITTER_PASSWORD, 
            streaming_callback=self.handle_stream)

        self.limit = limit
        client = HTTPClient()
        client.fetch(req)

    def handle_stream(self, response):
        try:
            json = simplejson.loads(response)
        except ValueError:
            return
        self.queue.put(json)

        self.tweet_count += 1
        print "Received Tweet %d" % self.tweet_count
        
        if self.tweet_count == self.limit:
            self.tweet_count = 0
            raise HarvestingComplete()

    @classmethod
    def to_classification_object(cls, json):
        c = ClassificationObject()
        
        c.source = 'twitter'
        c.text = json['text']
        c.created_at = json['created_at']

        return c

if __name__ == "__main__":
    t = TweetHarvester()
    try:
        t.harvest()
    except HTTPError:
        print "Done!"
        