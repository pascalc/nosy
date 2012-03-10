import multiprocessing
import redis
import simplejson

from nosy.classification_object import ClassificationObject
from nosy.algorithm.lang import LanguageClassifier

class HarvestingComplete(Exception):
    pass

class Harvester(object):
    # Job queue
    queue = multiprocessing.Queue()

    def __init__(self, processes):
        self.workers = []
        for i in range(processes):
            worker = Worker(self)
            worker.start()
            self.workers.append(worker)

    @classmethod
    def to_classification_object(cls, data):
        return ClassificationObject(data)

class Worker(multiprocessing.Process):
    _redis = redis.Redis()

    def __init__(self, harvester):
        super(Worker, self).__init__()
        self.harvester = harvester

    @classmethod
    def publish(cls, class_obj):
        message = { 'channels' : ['nosy'], 'data' : class_obj.to_dict() }
        json = simplejson.dumps(message, default=cls._json_serializer)
        cls._redis.publish('juggernaut', json)

    @classmethod
    def _json_serializer(cls, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

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
