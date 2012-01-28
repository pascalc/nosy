import tornado.ioloop
import tornado.web
import pymongo
import simplejson

class TweetHandler(tornado.web.RequestHandler):
    db = pymongo.Connection()['nosy']

    def get(self):
        count = int(self.get_argument('count', 10))

        results = self.db.tweets.find({}, limit=count)
        tweets = []
        for doc in results:
            try:
                del doc["_id"]
                if doc['user']['lang'] == 'en':
                    tweets.append(
                        { 'text' : doc['text'] }
                    )
            except KeyError:
                continue

        json = simplejson.dumps(tweets)
        self.set_header("Content-Type", "application/json")
        self.write(json)

application = tornado.web.Application([
    (r"/tweets", TweetHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()