import tornado.ioloop
import tornado.web
import simplejson
import pymongo

from classification_object import ClassificationObject

class ClassifyHandler(tornado.web.RequestHandler):
    # Example http://localhost:8888/classify?limit=10&skip=true leaves threshold as default
    def get(self):
        try:
            threshold = int(self.get_argument('threshold', 0.5))
        except ValueError:
            raise 'Digits allowed'

        try:
            limit = int(self.get_argument('limit', 10))
        except ValueError:
            raise 'Intgers allowed'

        try:
            skip = self.get_argument('skip', 'false')
        except ValueError:
            raise 'Valid values: {true, false}'

        # JSON list of matching classification objects
        self.write('Threshold %f, limit %d, skip %s' % (threshold, limit, skip))

    def post(self):
        try:
            c_obj = self.get_argument('classification_object')
        except TypeError:
            raise 'Classification objected allowed'

        # perform classification on the given object

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class StreamHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            source_url = self.get_argument('source_url')
        except TypeError:
            raise 'Could not find source url'

        try:
            threshold = self.get_argument('thresholds')
        except TypeError:
            raise ''

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
    def get(self, algorithm_id):


        self.write('Settings for algorithm %s is {} \n' % algorithm_id)

    # Test with $curl -X PUT http://localhost:8888/algorithm/:id
    def put(self, algorithm_id):

        self.write('Updated settings for algorithm %s \n' % algorithm_id)


application = tornado.web.Application([
    (r"/classify", ClassifyHandler),
    (r"/classify/stream", StreamHandler),
    (r"/train", TrainHandler),
    (r"/test", TestHandler),
    (r"/algorithm/([0-9]+)", AlgorithmHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()