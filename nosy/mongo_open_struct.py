import pymongo
from datetime import datetime, timedelta

from open_struct import OpenStruct

class MongoOpenStruct(OpenStruct):
    def __init__(self, data=None, **kwargs):
        super(MongoOpenStruct, self).__init__(data, **kwargs)

    def _on_created(self, data, **kwargs):
        if data and '_id' in data: 
            self.new = False
            self.__dict__.update(data)
        else:
            self.new = True

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
        data = cls.coll.find_one( { '_id' : cls.ID_TYPE(id) } )
        if not data:
            return data #raise Exception('No document found')
        return cls(data)

    @classmethod
    def find(cls, query=None, **kwargs):
        if not query: query = {}
        docs = cls.coll.find(query, **kwargs)
        for d in docs: 
            yield(cls(d))

    def save(self):
        self.last_modified = datetime.utcnow()
        
        new = self.new
        del self.new
        
        if new:
            self._id = self._generate_id()
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

    @classmethod
    def remove(cls, query):
        cls.coll.remove(query)