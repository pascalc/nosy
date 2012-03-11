import multiprocessing
from tornado.httpclient import HTTPClient, HTTPRequest, HTTPError
import simplejson
import argparse

class StreamHandler(object):
    # Job queue
    queue = multiprocessing.Queue()

    def __init__(self, processes):
        self.workers = []
        for i in range(processes):
            worker = self.Worker(self)
            worker.start()
            self.workers.append(worker)

    @classmethod
    def to_classification_object(cls, data):
        pass

class HarvestingComplete(Exception):
    pass

class TwitterHandler(StreamHandler):
    # Twitter sample stream
    STREAM_URL = "https://stream.twitter.com/1/statuses/sample.json"

    def __init__(self, username, password, workers=2):
        super(TwitterHandler, self).__init__(workers)
        self.username = username
        self.password = password
        self.tweet_count = 0

    def harvest(self, limit=1000):
        req = HTTPRequest(
            self.STREAM_URL, 
            method="GET",
            auth_username=self.username,
            auth_password=self.password,
            request_timeout=999999999999,
            streaming_callback=self.handle_stream)

        self.limit = limit
        client = HTTPClient()
        try:
            client.fetch(req)
        except HTTPError as e:
            print "HTTP Error: %s" % e.message
        except HarvestingComplete:
            for w in self.workers:
                w.terminate()
            print "Completed!"

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
    def parse_args(cls):
        parser = argparse.ArgumentParser(
            description='Twitter stream handling script for Nosy'
        )
        parser.add_argument('username', help='Your Twitter username')
        parser.add_argument('password', help='Your Twitter password')
        parser.add_argument('-processes', dest='workers', type=int, default=2, help='Number of worker processes')
        parser.add_argument('-tweets', dest='tweets', type=int, default=500, help='Number of tweets to harvest')
        
        return parser.parse_args()

    @classmethod
    def run(cls):
        args = cls.parse_args()
        t = cls(args.username, args.password, workers=args.workers)
        t.harvest(limit=args.tweets)