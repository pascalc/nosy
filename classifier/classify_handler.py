import tornado.ioloop
import tornado.web
import simplejson
import pymongo
import redis
from datetime import datetime

import nosy.util
from nosy.model import ClassifiedObject
from nosy.algorithm.naive_bayes import NaiveBayesClassifier

class ClassifyHandler(tornado.web.RequestHandler):
    #CLASSIFIER = NaiveBayesClassifier.load()

    # Get ClassifiedObjects
    def get(self):
        try:
            limit = int(self.get_argument('limit', 10))
        except ValueError:
            raise tornado.web.HTTPError(400)

        query = {}

        # Search for classified objects exceeding thresholds if supplied
        thresholds = self.get_argument('thresholds', None)
        if thresholds:
            thresholds = simplejson.loads(thresholds)
            for tag, threshold in thresholds.iteritems():
                query['tags.' + tag] = { '$gte' : threshold }

        # Limit to a daterange if supplied
        start_time = self.get_argument('start_time', None)
        if start_time:
            start_time = datetime.fromtimestamp(long(start_time))
            query['last_modified'] = {}
            query['last_modified']['$gte'] = start_time

        end_time = self.get_argument('end_time', None)
        if end_time:
            end_time = datetime.fromtimestamp(long(end_time))
            if 'last_modified' not in query:
                query['last_modified'] = {}
            query['last_modified']['$lte'] = end_time

        results = ClassifiedObject.find(
            query=query,
            limit=limit,
            sort=[("last_modified", pymongo.DESCENDING)]
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=nosy.util.json_serializer)

        self.set_header("Content-Type", "application/json")
        self.write(json)

    # Classify an object
    # def post(self):
    #     text = self.get_argument('text')
    #     if not text:
    #         raise tornado.web.HTTPError(400, 'Parameter \'text\' is required')

    #     result = self.CLASSIFIER.classify_text(text)
    #     json = simplejson.dumps(result, default=nosy.util.json_serializer)

    #     self.set_header("Content-Type", "application/json")
    #     self.write(json)

class ThresholdsHandler(tornado.web.RequestHandler):
    _redis = redis.Redis()
    THRESHOLDS_KEY = 'nosy:classify:thresholds'

    # Get current thresholds
    def get(self):
        thresholds = self._redis.hgetall(self.THRESHOLDS_KEY)
        thresholds = { k: float(v) for k, v in thresholds.iteritems() }
        self.write(simplejson.dumps(thresholds, default=nosy.util.json_serializer))

    # Edit streaming thresholds
    def put(self):
        try:
            body = simplejson.loads(self.request.body)
            thresholds = body['thresholds']
            assert isinstance(thresholds, dict)
        except:
            raise tornado.web.HTTPError(400, 'Parameter \'thresholds\' needs to be valid JSON')

        self._redis.hmset(self.THRESHOLDS_KEY, thresholds)
        
        self.set_header("Content-Type", "application/json")
        self.write(simplejson.dumps({'success' : True}))

application = tornado.web.Application([
    (r"/classify", ClassifyHandler),
    (r"/classify/thresholds", ThresholdsHandler),
])

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()