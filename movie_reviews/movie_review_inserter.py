import os

from nosy.model import ClassificationObject

# Clear all tagged with 'movie'
ClassificationObject.remove({'tags': {'$ne': [] } })

POS_DIR = 'txt_sentoken/pos'
NEG_DIR = 'txt_sentoken/neg'

def line_iterator(directory):
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            for line in f:
                yield(line)

def save_classification_object(line, tags):
    c = ClassificationObject()
    c.text = line
    c.process()
    c.tags = tags
    c.save()

# Positive reviews
for line in line_iterator(POS_DIR):
    save_classification_object(line, ['movie'])

# Negative reviews
for line in line_iterator(NEG_DIR):
    save_classification_object(line, ['movie'])