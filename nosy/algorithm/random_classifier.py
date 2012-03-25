import random

class RandomClassifier():
    _TAGS = [
        'riot',
        'earthquake',
        'apocalypse',
        'zombies',
        'aliens',
        'urgent',
        'wtf'
    ]

    @classmethod
    def classify(cls, c):
        num_tags = random.randint(0,len(cls._TAGS))
        for i in range(num_tags):
            c.tags[random.choice(cls._TAGS)] = random.random()