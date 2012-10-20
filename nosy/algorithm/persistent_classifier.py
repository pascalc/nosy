import redis
import cPickle

class PersistentClassifier(object):
    _REDIS = redis.Redis()
    BASE_KEY = 'nosy:algorithms:'

    def save(self):
        key = self.BASE_KEY + self.__class__.__name__
        value = cPickle.dumps(self.classifiers)
        self._REDIS.set(key, value)

    @classmethod
    def load(cls):
        instance = cls()

        key = cls.BASE_KEY + cls.__name__
        value = cls._REDIS.get(key)
        instance.classifiers = cPickle.loads(value)

        return instance