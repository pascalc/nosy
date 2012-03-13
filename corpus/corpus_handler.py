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

class TagsHandler(tornado.web.RequestHandler):
    def get(self):
        tags = ClassificationObject.tags()
        
        json = simplejson.dumps({'tags' : tags})
        self.set_header("Content-Type", "application/json")
        self.write(json)

# class TrainingHandler(tornado.web.RequestHandler):
#     def get(self):
#         try:
#             tags = self.get_argument('tags');
#         except ValueError:
#             raise tornado.web.HTTPError(400); # tags is required

#         # get all tags passed as argument and convert into list
#         # JCA: experience encoding issues on Ubuntu 10.04. Get [u'val1', u'val2', ... ]
#         tags = map(lambda t: t.lower(), tags.split(','))

#         print tags, '\n'

#         # find all objects where all tag in tags is present
#         query = { 'tags' : { '$in' : tags } }
#         results = ClassificationObject.find(
#             query = query,
#             limit = 10,
#             sort = [("last_modified", pymongo.DESCENDING)]
#         )

#         dicts = [ c.to_dict() for c in results ]
#         json = simplejson.dumps(dicts, default=_json_serializer)

#         self.set_header("Content-Type", "application/json")
#         self.write(json)

# # curl -X POST -d "amount=10&username=joakim&password=secret" http://localhost:8888/harvest/twitter
# class HarvestHandler(tornado.web.RequestHandler):
#     '''
#     Preferrably: Call file 'source'_harvester.py
#     '''    
#     def get(self, source):
#         self.write('Source for data mining is %s' % source)

#     # tweet harvester
#     def post(self, source): # why not just get if only amount
#         try:
#             amount = int(self.get_argument('amount', 10))
#         except ValueError:
#             raise e

#         try:
#             username = self.get_argument('username', 'username')
#         except TypeError:
#             raise ''

#         try:
#             password = self.get_argument('password', 'password') 
#         except TypeError:
#             raise ''

#         #t = TweetHarvester(username, password, 10)
#         #t.harvest(amount)
#         self.write('Amount %d. Credentials for %s = Username: %s and password: %s \n' % (amount, source, username, password))

application = tornado.web.Application([
    (r'/corpus', CorpusHandler), 
    (r'/corpus/([0-9]+)', CorpusHandler),
    (r'/corpus/tags', TagsHandler),
#    (r"/training", TrainingHandler),
#    (r"/harvest/([a-zA-Z]+)", HarvestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()