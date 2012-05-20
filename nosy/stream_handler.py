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

    def __init__(self, username, password, workers=2, timeout=30):
        super(TwitterHandler, self).__init__(workers)
        self.username = username
        self.password = password
        self.tweet_count = 0
        self.timeout = timeout

    def harvest(self):
        req = HTTPRequest(
            self.STREAM_URL, 
            method="GET",
            auth_username=self.username,
            auth_password=self.password,
            request_timeout=self.timeout,
            streaming_callback=self.handle_stream)

        client = HTTPClient()
        try:
            client.fetch(req)
        except HTTPError as e:
            print "HTTP Error: %s" % e.message

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

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(
            description='Twitter stream handling script for Nosy'
        )
        parser.add_argument('username', help='Your Twitter username')
        parser.add_argument('password', help='Your Twitter password')
        parser.add_argument('-processes', dest='workers', type=int, default=1, help='Number of worker processes')
        parser.add_argument('-timeout', dest='timeout', type=int, default=30, help='Seconds to keep connection to Twitter open')
        
        return parser.parse_args()

    @classmethod
    def run(cls):
        args = cls.parse_args()
        t = cls(args.username, args.password, workers=args.workers, timeout=args.timeout)
        t.harvest()