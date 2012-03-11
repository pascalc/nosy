import tornado.ioloop
import tornado.web
import simplejson
import pymongo

from nosy.lib.model import ClassificationObject

class CorpusHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            limit = int(self.get_argument('limit', 10))
        except ValueError:
            raise tornado.web.HTTPError(400)

        query = {}

        keywords = self.get_argument('keywords', None)
        if keywords:
            keywords = map(lambda k: k.lower(), keywords.split(','))
            query = { 'keywords' : { '$in' : keywords } }

        results = ClassificationObject.find(
            query=query,
            limit=limit,
            sort=[("last_modified", pymongo.DESCENDING)]
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=self._json_serializer)

        self.set_header("Content-Type", "application/json")
        self.write(json)

    #  curl -X PUT -d "id=5&tags=l,o,l" http://localhost:8888/corpus
    def put(self):
        try:
            id = int(self.get_argument('id'))
        except ValueError:
            raise tornado.web.HTTPError(400)

        tags = self.get_argument('tags')
        tags = map( lambda t: t.lower(), tags.split(','))

        # update the tags for classification object
        c = ClassificationObject.find_by_id(id)

        success = True
        message = 'Successfully updated id %d with tags %s' % (id, tags)
        if c:
            c.tags = tags
            try:
                c.save()
            except Exception, e:
                success = False
                message = 'An error occured while saving'
        else:
            success = False
            message = 'Document %d was not found' % id
            raise tornado.web.HTTPError(404)

        json = {'success': success, 'message': message}
        self.set_header('Content-Type', 'application/json')
        self.write(json)

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class TrainingHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            tags = self.get_argument('tags');
        except ValueError:
            raise tornado.web.HTTPError(400); # tags is required

        # get all tags passed as argument and convert into list
        # JCA: experience encoding issues on Ubuntu 10.04. Get [u'val1', u'val2', ... ]
        tags = map(lambda t: t.lower(), tags.split(','))

        print tags, '\n'

        # find all objects where all tag in tags is present
        query = { 'tags' : { '$in' : tags } }
        results = ClassificationObject.find(
            query = query,
            limit = 10,
            sort = [("last_modified", pymongo.DESCENDING)]
        )

        dicts = [ c.to_dict() for c in results ]
        json = simplejson.dumps(dicts, default=_json_serializer)

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

@classmethod
def _json_serializer(cls, obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

application = tornado.web.Application([
    (r"/corpus", CorpusHandler), 
    (r"/training", TrainingHandler),
    (r"/harvest/([a-zA-Z]+)", HarvestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()