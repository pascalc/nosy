import pymongo
import random

from datetime import datetime, timedelta

class AlgorithmObject(object):
    # MongoDB
    COUNTER_ID = 'algorithm_objects'
    connection = pymongo.Connection('nosy.pspace.se', 27017)
    db = connection[''] # TODO
    coll = db['']       # TODO

    @classmethod
    def _generate_id(cls):
        query = { '_id' : cls.COUNTER_ID }
        action = { '$inc' : { 'next' : 1 } }
        response = cls.db.counters.find_and_modify(
            query, action, new=True, upsert=True
        )
        return response['next']

    @classmethod
    def find_by_id(cls, id):
        data = cls.coll.find_one( { '_id' : long(id) } )
        if not data:
            return data
        return AlgorithmObject(data)

    @classmethod
    def find(cls, query=None, skip=0, limit=25, **kwargs):
        if not query: query = {}
        docs = cls.coll.find(query, skip=skip, limit=limit, **kwargs)
        return [ AlgorithmObject(data) for data in docs ]

    @classmethod
    def ensure_indexes(cls):
        cls.coll.ensure_index('parameters')

    def __init__(self, data=None, **kwargs):
        if data and '_id' in data: 
            self.new = False
            self.__dict__.update(data)
        else:
            self.new = True
            self._id = self._generate_id()

        # Merge with kwargs if supplied
        self.__dict__.update(kwargs)

    def __setattr__(self, name, value):
        # if name.startswith('_'):
        #     super(AlgorithmObject, self).__setattr__(name, value)
        self.__dict__[name] = value

    def __delattr__(self, name):
        del self.__dict__[name]

    def save(self):
        self.last_modified = datetime.utcnow()
        
        new = self.new
        del self.new
        
        if new:
            self.coll.insert(self.__dict__)
        else:
            query, action = self._update_command()
            self.coll.update(query, action)

    def _update_command(self):
        query = { '_id' : self._id }
        
        action = { '$set' : {} }
        for attribute, value in self.__dict__.iteritems():
            action['$set'][attribute] = value
        del action['$set']['_id']

        return query, action

    def to_dict(self):
        return self.__dict__