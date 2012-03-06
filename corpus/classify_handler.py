import tornado.ioloop
import tornado.web
import simplejson
import pymongo

from classification_object import ClassificationObject

class ClassifyHandler(tornado.web.RequestHandler):
    # Example http://localhost:8888/classify?limit=10&skip=true leaves threshold as default
    def get(self):
        '''
        @parameter thresholds   Threshold [0,1]
        @parameter limit        Maximum amount of classification objects
        @parameter skip         Skip is per default True. If sent, regardless of its value, then False
        '''
        try:
            threshold = float(self.get_argument('threshold', 0.5))
        except ValueError:
            raise 'Digits allowed'
        
        if not _valid_threshold(threshold):
            self.write('Threshold valid range is [0,1]')
        
        try:
            limit = int(self.get_argument('limit', 10))
        except ValueError:
            raise 'Integers allowed'

        skip = self.get_argument('skip', True)
        if skip != True:
            skip = False

        # JSON list of matching classification objects
        self.set_status(200)
        self.write('Threshold %f, limit %d, skip %s' % (threshold, limit, skip))

    def post(self):
        try:
            c_obj = self.get_argument('classification_object')
        except TypeError:
            raise 'Classification objected allowed'

        # perform classification on the given object

    def put(self):
        '''
        Returns 200 on success, 4xx on failure
        '''

        self.set_status(200)

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class StreamHandler(tornado.web.RequestHandler):
    def get(self):
        source_url = self.get_argument('source_url')
        
        try:
            threshold = float(self.get_argument('thresholds'))
        except ValueError:
            raise 'Digits allowed'

        if not _valid_threshold(threshold):
            self.write('Threshold valid range is [0,1]')

class TrainHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            source_url = self.get_argument('source_url')
        except TypeError:
            raise 'Could not find source url'

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Test handler')

class AlgorithmHandler(tornado.web.RequestHandler):
    @classmethod
    def _find_algorithm_by_id(self, id):
        algorithm = ClassificationObject.find_by_id(id)
        # if not c:
        #     raise tornado.web.HTTPError(404)
        return algorithm

    def get(self, algorithm_id):
        a = self._find_algorithm_by_id(algorithm_id)
        algorithm = {"_id": algorithm_id, "data": {"alpha":0.2, "beta":0.7}}
        json = simplejson.dumps(algorithm)
        self.write(json)

    # Test with $curl -d algorithm_settings_json.txt -X PUT -H 'Content-type:application/json' -v http://localhost:8888/algorithm/5
    def put(self, algorithm_id):
        settings = tornado.escape.json_decode(self.request.body)
        self.write(simplejson.dumps(settings))
        id = settings['_id']
        name = settings['name']

        # for setting, value in data:
        #     print '%s -> %d\n' % (setting, value)

        # a = self._find_algorithm_by_id(algorithm_id)
        # a.settings = settings
        # try:
        #     a.save()
        # except Exception, e:
        #     raise tornado.web.HTTPError(500)

        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        self.write('Id %d, name %s' % (id, name))

class AlgorithmsHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        Return a list of algorithms
        '''
        algorithms = [{"_id" : 1, "data": {}}, {"_id": 2, "data": {}}]
        json = simplejson.dumps(algorithms)

        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        self.write(json)

#@globalmethod
def _valid_threshold(threshold):
    if threshold > 1 or threshold < 0:
        return False
    return True

application = tornado.web.Application([
    (r"/classify", ClassifyHandler),
    (r"/classify/stream", StreamHandler),
    (r"/train", TrainHandler),
    (r"/test", TestHandler),
    (r"/algorithm/([0-9]+)", AlgorithmHandler),
    (r"/algorithms", AlgorithmsHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()