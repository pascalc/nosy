import pymongo
import multiprocessing
import Queue

from classification_object import ClassificationObject

class HarvestingComplete(Exception):
    pass

class Harvester(object):
    # Job queue
    queue = multiprocessing.Queue()

    def __init__(self, workers):
        for i in range(workers):
            worker = Worker(self)
            worker.start()

    @classmethod
    def to_classification_object(cls, data):
        return ClassificationObject(data)

class Worker(multiprocessing.Process):
    def __init__(self, harvester):
        super(Worker, self).__init__()
        self.harvester = harvester

    def run(self):
        while(True):            
            data = self.harvester.queue.get(True)
            
            try:
                c = self.harvester.to_classification_object(data)
            except KeyError:
                continue
            
            c.extract_keywords()
            c.save()