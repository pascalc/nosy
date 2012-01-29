import pymongo
import multiprocessing

from classification_object import ClassificationObject

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