from nltk.tokenize import WordPunctTokenizer
import pymongo

from mongo_open_struct import MongoOpenStruct

class Base(MongoOpenStruct):
    # NLTK
    TOKENIZER = WordPunctTokenizer()

    def __init__(self, data=None, **kwargs):
        super(Base, self).__init__(data, **kwargs)

    def extract_keywords(self):
        self.keywords = map(lambda word: word.lower(), self.TOKENIZER.tokenize(self.text))

class ClassificationObject(Base):
    COUNTER_ID = 'corpus'
    connection = pymongo.Connection('localhost', 27017)
    db = connection['nosy']
    coll = db['corpus']

    def __init__(self, data=None, **kwargs):
        super(ClassificationObject, self).__init__(data, **kwargs)
        self.tags = []

class ClassifiedObject(Base):
    COUNTER_ID = 'classified'
    connection = pymongo.Connection('localhost', 27017)
    
    db = connection['nosy']
    if 'classified' in db.collection_names():
        coll = db['classified']
    else:
        coll = db.create_collection('classified',
            size = 1024*1024*500, # 500 MB
            capped = True
        )

    def __init__(self, data=None, **kwargs):
        super(ClassifiedObject, self).__init__(data, **kwargs)
        self.tags = {}