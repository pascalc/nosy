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

        os.system('python tweet_classifier.py -processes 1 -tweets 1000 YAP_nosy yetanotherproject &')
        json = simplejson.dumps({'success': True})

        self.set_header('Content-Type', 'application/json')
        self.write(json)

class ClassifyHandler(tornado.web.RequestHandler):
    @classmethod
    def parse_json(self, data):
        json = simplejson.loads(data)
        if not json:
            raise ValueError
        return json

    @classmethod
    def parse_txt(self, data):
        DELIMITER = '\n'
        return self.convert(data, DELIMITER)

    @classmethod
    def parse_csv(self, data):
        DELIMITER = ','
        return self.convert(data, DELIMITER)

    @classmethod
    def convert(self, data, delimiter):
        print data
        return [{'text': line} for line in map( lambda x: x.lower(), data.split(delimiter)) if line]


    def post(self, format):
        encoding = {
            'json': self.parse_json,
            'txt': self.parse_txt,
            'csv': self.parse_csv
        }

        try:
            fn = encoding[format]
            print fn.__name__
        except KeyError:
            raise tornado.web.HTTPError(404, "Format %s not supported" % format)
        
        try:
            data = fn(self.request.body)
            print data
        except ValueError:
            raise tornado.httpserver._BadRequestException("Invalid JSON structure.")
        
        # _redis = redis.Redis()

        # get the features and map to the id
        # features = [ (c_id, feature_extractor(text)) for c_id, text in data['data'] ]
        
        # classify the text and store the result under each id
        # classifier = _redis.get('nosy:classifier:naivebayes')
        # result = [(c_id, type_classifier.classify(feature)) for c_id, feature in features]

        # self.set_header('Content-Type', 'application/json')
        # self.write(simplejson.dumps(result))

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
    (r"/classify/(json|csv|txt)", ClassifyHandler),
    (r"/classify/stream", StreamHandler),
    # (r"/train", TrainHandler),
    # (r"/test", TestHandler),
    # (r"/algorithm/([0-9]+)", AlgorithmHandler),
    # (r"/algorithms", AlgorithmsHandler),
])

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()