import pymongo

from base import Base

class ClassificationObject(Base):
    COUNTER_ID = 'corpus'
    connection = pymongo.Connection('localhost', 27017)
    db = connection['nosy']
    coll = db['corpus']

    def __init__(self, data=None, **kwargs):
        super(ClassificationObject, self).__init__(data, **kwargs)
        self.tags = []

    @classmethod
    def ensure_indexes(cls):
        cls.coll.ensure_index('tags')
        cls.coll.ensure_index('last_modified')
        cls.coll.ensure_index('stemmed_keywords')

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

    @classmethod
    def ensure_indexes(cls):
        cls.coll.ensure_index('tags')
        cls.coll.ensure_index('last_modified')