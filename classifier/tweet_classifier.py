import multiprocessing
import simplejson
import redis

from nosy.stream_handler import TwitterHandler
from nosy.model import ClassifiedObject
from nosy.algorithm.lang import LanguageClassifier
import nosy.util

class ClassifierWorker(multiprocessing.Process):
    _redis = redis.Redis()

    def __init__(self, harvester):
        super(ClassifierWorker, self).__init__()
        self.harvester = harvester

    @classmethod
    def publish(cls, class_obj):
        message = { 'channels' : ['nosy'], 'data' : class_obj.to_dict() }
        json = simplejson.dumps(message, default=nosy.util.json_serializer)
        cls._redis.publish('juggernaut', json)

    def run(self):
        while(True):            
            data = self.harvester.queue.get(True)
            
            try:
                c = self.harvester.to_classification_object(data)
            except KeyError:
                continue
            
            c.extract_keywords()
            
            LanguageClassifier.classify(c)
            if (c.tags['english'] > 0.8):
                self.publish(c)
                c.save()

class TweetClassifier(TwitterHandler):
    Worker = ClassifierWorker

    @classmethod
    def to_classification_object(cls, json):
        c = ClassifiedObject()
        
        c.source = 'twitter'
        c.text = json['text']
        c.created_at = json['created_at']

        return c

if __name__ == "__main__":    
    TweetClassifier.run()