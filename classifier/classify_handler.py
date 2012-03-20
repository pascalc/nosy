import tornado.ioloop
import tornado.web
import simplejson
import pymongo
import os
import redis

from nosy.model import ClassifiedObject
import nosy.util
from tweet_classifier import TweetClassifier

class StreamHandler(tornado.web.RequestHandler):
    # curl -i -X POST -d @_stream.json -H 'Content-type:application/json' -v http://localhost:7777/classify/stream
    def post(self):
        _redis = redis.Redis()
        try:
            tags = simplejson.loads(self.request.body) #tornado.escape.json_decode(self.request.body)
        except ValueError:
            raise tornado.httpserver._BadRequestException("Invalid JSON structure.")

        _redis.set('nosy:classifying:thresholds', simplejson.dumps(tags))
        # for tag, val in tags.iteritems():
        #     self.write('%s => %0.3f\n' % (tag, val))
        #     pass

        os.system('python tweet_classifier.py -processes 1 -tweets 1000 YAP_nosy yetanotherproject &')
        json = simplejson.dumps({'success': True})

        self.set_header('Content-Type', 'application/json')
        self.write(json)

# class ClassifyHandler(tornado.web.RequestHandler):
    # # Example http://localhost:8888/classify?limit=10&skip=true leaves threshold as default
    # def get(self):
    #     '''
    #     @parameter thresholds   Threshold [0,1]
    #     @parameter limit        Maximum amount of classification objects
    #     @parameter skip         Skip is per default True. If sent, regardless of value, then False
    #     '''
    #     try:
    #         threshold = float(self.get_argument('threshold', 0.5))
    #         _valid_threshold(threshold)
    #     except ValueError:
    #         raise tornado.web.HTTPError(500, 'Digits allowed')
    #     except InvalidThreshold, e:
    #         raise tornado.web.HTTPError(500, '%s' % e)
        
    #     try:
    #         limit = int(self.get_argument('limit', 10))
    #     except ValueError:
    #         raise tornado.web.HTTPError(500, 'Integers allowed')

    #     skip = self.get_argument('skip', True)
    #     if skip != True:
    #         skip = False

    #     # JSON list of matching classification objects
    #     self.set_status(200)
    #     self.write('Threshold %f, limit %d, skip %s' % (threshold, limit, skip))

    # def post(self):
    #     try:
    #         c_obj = self.get_argument('classification_object')
    #     except TypeError:
    #         raise tornado.web.HTTPError(500, 'Classification objected allowed')

    #     # perform classification on the given object

    # def put(self):
    #     '''
    #     Returns 200 on success, 4xx on failure
    #     '''

    #     self.set_status(200)

    # @classmethod
    # def _json_serializer(cls, obj):
    #     if hasattr(obj, 'isoformat'):
    #         return obj.isoformat()
    #     else:
    #         raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

# class TrainHandler(tornado.web.RequestHandler):
#     def post(self):
#         try:
#             source_url = self.get_argument('source_url')
#         except TypeError:
#             raise 'Could not find source url'

# class TestHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write('Test handler')

# class AlgorithmHandler(tornado.web.RequestHandler):
#     @classmethod
#     def _find_algorithm_by_id(self, id):
#         algorithm = AlgorithmObject.find_by_id(id)
#         return algorithm

#     def get(self, algorithm_id):
#         #a = self._find_algorithm_by_id(algorithm_id)
#         algorithm = {"_id": algorithm_id, "data": {"alpha":0.2, "beta":0.7}}
#         json = simplejson.dumps(algorithm)
#         self.write(json)

#     # Test with $curl -d @_algorithm_settings_json.txt -X PUT -H 'Content-type:application/json' -v http://localhost:8888/algorithm/5
#     def put(self, algorithm_id):
#         settings = tornado.escape.json_decode(self.request.body)
#         id = settings['_id']
#         name = settings['name']
#         parameters = settings['parameters']

#         #a = self._find_algorithm_by_id(algorithm_id)
#         for param, value in parameters.items():
#             #try:
#                 #a.settings[param] = value
#             self.write('%s -> %f\n' % (param, value))

#         # try:
#         #     a.save()
#         # except Exception, e:
#         #     raise tornado.web.HTTPError(500)

#         self.set_status(200)
#         self.set_header('Content-Type', 'application/json')
#         json_parameters = simplejson.dumps(parameters)
#         self.write('Updated algorithm %d with settings %s\n' % (id, json_parameters))

# class AlgorithmsHandler(tornado.web.RequestHandler):
#     def get(self):
#         '''
#         Return a list of algorithms
#         '''
#         algorithms = [
#             {"_id" : 1, "name":"Bayseian clasiifier", "parameters": {} },
#             {"_id": 2, "name":"Maximum entropy", "parameters": {} }
#         ]
#         json = simplejson.dumps(algorithms)

#         self.set_status(200)
#         self.set_header('Content-Type', 'application/json')
#         self.write(json)

# #@globalmethod
# def _valid_threshold(threshold):
#     if threshold > 1.0 or threshold < 0:
#         raise InvalidThreshold('Threshold valid range is [0,1]')

# class InvalidThreshold(Exception):
#     pass

application = tornado.web.Application([
    # (r"/classify", ClassifyHandler),
    (r"/classify/stream", StreamHandler),
    # (r"/train", TrainHandler),
    # (r"/test", TestHandler),
    # (r"/algorithm/([0-9]+)", AlgorithmHandler),
    # (r"/algorithms", AlgorithmsHandler),
])

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()