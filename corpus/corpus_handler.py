import tornado.ioloop
import tornado.web
import simplejson
import pymongo

from nosy.model import ClassificationObject
import nosy.util

class CorpusHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            limit = int(self.get_argument('limit', 10))
        except ValueError:
            raise tornado.web.HTTPError(400)

        query = {}

        # Search for keywords after stemming if supplied
        keywords = self.get_argument('keywords', None)
        if keywords:
            words = map(lambda k: k.lower(), keywords.split(','))
            words = map(lambda w: ClassificationObject.stem(w), words)
            query['stemmed_keywords'] = { '$all': words }

        # Search for tags if supplied
        tags = self.get_argument('tags', None)
        if tags:
            tags = map(lambda t: t.lower(), tags.split(','))
            query['tags'] = { '$all': tags }
        else:
            # Otherwise filter by tagged or untagged
            tagged = self.get_argument('tagged', False)
            if tagged:
                query['tags'] = { '$ne' : [] }
            else:
                query['tags'] = []

        results = ClassificationObject.find(
            query=query,
            limit=limit,
            sort=[("last_modified", pymongo.DESCENDING)]
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=nosy.util.json_serializer)

        self.set_header("Content-Type", "application/json")
        self.write(json)

    #  curl -X PUT -d "tags=funny" http://localhost:8888/corpus/<id>
    def put(self, doc_id):
        try:
            doc_id = int(doc_id)
        except ValueError:
            raise tornado.web.HTTPError(400)

        tags = self.get_argument('tags', None)
        if tags:
            tags = map( lambda t: t.lower(), tags.split(','))

        # update the tags for classification object
        c = ClassificationObject.find_by_id(doc_id)
        if c:
            c.tags = tags
            c.save()
        else:
            raise tornado.web.HTTPError(404)

        json = simplejson.dumps({'success': True})
        self.set_header('Content-Type', 'application/json')
        self.write(json)

    def delete(self, doc_id):
        try:
            doc_id = int(doc_id)
        except ValueError:
            raise tornado.web.HTTPError(400)

        ClassificationObject.remove({'_id' : doc_id})

        json = simplejson.dumps({'success': True})
        self.set_header('Content-Type', 'application/json')
        self.write(json)                

class TagsHandler(tornado.web.RequestHandler):
    def get(self):
        tags = ClassificationObject.tags()
        
        json = simplejson.dumps({'tags' : tags})
        self.set_header("Content-Type", "application/json")
        self.write(json)

application = tornado.web.Application([
    (r'/corpus', CorpusHandler), 
    (r'/corpus/([0-9]+)', CorpusHandler),
    (r'/corpus/tags', TagsHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()