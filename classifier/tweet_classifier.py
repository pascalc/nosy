import multiprocessing
import simplejson
import redis
import random
import sys

from nosy.stream_handler import TwitterHandler
from nosy.model import ClassifiedObject
from nosy.algorithm.lang import LanguageClassifier
from nosy.algorithm.random_classifier import RandomClassifier
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
            data = self.harvester.queue.get(True, timeout=120)
            
            try:
                c = self.harvester.to_classification_object(data)
            except KeyError:
                continue
            
            c.process()
            RandomClassifier.classify(c)
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
        c.author = json['user']['screen_name']
        c.location = json['geo'] or \
            { 
                'longitude' : 18 + random.random(),
                'latitude' : 59 + random.random()
            }

        return c

    #Only harvest if not already harvesting
    def harvest(self, limit=1000):
        _redis = ClassifierWorker._redis
        running = _redis.get('nosy:classifying') == 'true'
        if running:
            print "Already running!"
            for w in self.workers:
                w.terminate()
            sys.exit(1)
        else:
            _redis.set('nosy:classifying', 'true')
            super(TweetClassifier, self).harvest(limit=limit)
            _redis.delete('nosy:classifying')    

if __name__ == "__main__":
    TweetClassifier.run()