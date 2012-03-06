import tornado.ioloop
import tornado.web
import simplejson
import pymongo

from classification_object import ClassificationObject

class CorpusHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            count = int(self.get_argument('count', 10))
        except ValueError:
            raise tornado.web.HTTPError(400)

        query = {}

        keywords = self.get_argument('keywords', None)
        if keywords:
            keywords = map(lambda k: k.lower(), keywords.split(','))
            query = { 'keywords' : { '$in' : keywords } }

        results = ClassificationObject.find(
            query=query,
            limit=count,
            sort=[("last_modified", pymongo.DESCENDING)]
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=self._json_serializer)

        self.set_header("Content-Type", "application/json")
        self.write(json)

    def put(self):
        try:
            id = int(self.get_argument('id'))
        except ValueError:
            raise ''

        try:
            tags = self.get_argument('tags')
        except ValueError:
            raise ''
        
        tags = map( lambda t: t.lower(), tags.split(','))

        # update the tags for classification object
        c = ClassificationObject.find_by_id(id)
        c.tags = tags
        success = true
        try:
            c.save()
        except TypeError:
            raise ''
            success = false

        if success:
            self.write('Successfully updated id %d with tags %s' % id, tags)
        else:
            self.write('Could not update tags %s for id %d' % id, tags)

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class TrainingHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            tags = self.get_arguments('tags');
        except ValueError:
            raise tornado.web.HTTPError(400); # tags is required

        # get all tags passed
        tags = map(lambda t: t.lower(), tags.split(','))
        
        # find all objects where all tag in tags is present and output
        query = { 'tags' : { '$in' : tags } }
        results = ClassificationObject.find(
            query = query,
            limit = None,
            sort = [("last_modified", pymongo.DESCENDING)]
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=self._json_serializer)

        self.set_header("Content-Type", "application/json")
        self.write(json)

# curl -X POST -d "amount=10&username=joakim&password=secret" http://localhost:8888/harvest/twitter
class HarvestHandler(tornado.web.RequestHandler):
    '''
    Preferrably: Call file 'source'_harvester.py
    '''    
    def get(self, source):
        self.write('Source for data mining is %s' % source)

    # tweet harvester
    def post(self, source): # why not just get if only amount
        try:
            amount = int(self.get_argument('amount', 10))
        except ValueError:
            raise e

        try:
            username = self.get_argument('username', 'username')
        except TypeError:
            raise ''

        try:
            password = self.get_argument('password', 'password') 
        except TypeError:
            raise ''

        #t = TweetHarvester(username, password, 10)
        #t.harvest(amount)
        self.write('Amount %d. Credentials for %s = Username: %s and password: %s \n' % (amount, source, username, password))

application = tornado.web.Application([
    (r"/corpus", CorpusHandler), 
    (r"/training", TrainingHandler),
    (r"/harvest/([a-zA-Z]+)", HarvestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()