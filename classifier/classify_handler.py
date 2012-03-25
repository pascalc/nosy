import tornado.ioloop
import tornado.web
import simplejson
import pymongo
from datetime import datetime

from nosy.model import ClassifiedObject
import nosy.util

class ClassifyHandler(tornado.web.RequestHandler):

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

# class StreamHandler(tornado.web.RequestHandler):
#     def post(self):
#         os.system('python tweet_classifier.py -processes 1 -tweets 1000 YAP_nosy yetanotherproject &')
#         json = simplejson.dumps({'success': True})

#         self.set_header('Content-Type', 'application/json')
#         self.write(json)

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
    (r"/classify", ClassifyHandler),
    # (r"/classify/stream", StreamHandler),
    # (r"/train", TrainHandler),
    # (r"/test", TestHandler),
    # (r"/algorithm/([0-9]+)", AlgorithmHandler),
    # (r"/algorithms", AlgorithmsHandler),
])

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()