import tornado.ioloop
import tornado.web
import simplejson

from classification_object import ClassificationObject

class CorpusHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            count = int(self.get_argument('count', 10))
        except ValueError:
            raise tornado.web.HTTPError(400)

        query = {}

        keyword = self.get_argument('keyword', None)
        if keyword:
            query = { 'keywords' : keyword }

        results = ClassificationObject.find(
            query=query,
            limit=count
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=self._json_serializer)

        self.set_header("Content-Type", "application/json")
        self.write(json)

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

application = tornado.web.Application([
    (r"/corpus", CorpusHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()