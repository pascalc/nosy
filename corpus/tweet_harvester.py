import multiprocessing

from nosy.stream_handler import TwitterHandler
from nosy.model import ClassificationObject
from nosy.algorithm.lang import LanguageClassifier

class CorpusWorker(multiprocessing.Process):
    def __init__(self, harvester):
        super(CorpusWorker, self).__init__()
        self.harvester = harvester

    def run(self):
        while(True):            
            data = self.harvester.queue.get(True)
            
            try:
                c = self.harvester.to_classification_object(data)
            except KeyError:
                continue
            
            c.process()
            if LanguageClassifier._english_score(c.text.split()) > 0.8:
                c.save()

class TweetHarvester(TwitterHandler):
    Worker = CorpusWorker

    @classmethod
    def to_classification_object(cls, json):
        c = ClassificationObject()
        
        c.source = 'twitter'
        c.text = json['text']
        c.created_at = json['created_at']

        return c

if __name__ == "__main__":
    TweetHarvester.run()
