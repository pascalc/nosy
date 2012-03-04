import tornado.ioloop
import tornado.web
import simplejson
import pymongo

from classification_object import ClassificationObject

class ClassifyHandler(tornado.web.RequestHandler):
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
            skip = self.get_argument('skip', false)
        except ValueError:
            raise 'Valid values: {true, false}'

        # JSON list of matching classification objects
        self.write()

    def post(self):
        try:
            c_obj = self.get_argument('classification_object')
        except TypeError:
            raise ''

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

application = tornado.web.Application([
    (r"/classify/(stream)?", ClassifyHandler),
])

train = tornado.web.Application([
    (r"/train", TrainHandler),
])

test = tornado.web.Application([
    (r"/test", TestHandler),
])

application = tornado.web.Application([
    (r"/algorithm/([0-9]+)", AlgorithmHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()