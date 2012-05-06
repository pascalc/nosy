import random
from nltk.classify import NaiveBayesClassifier as NltkNaiveBayes
from nltk.classify.util import accuracy

from nosy.algorithm.persistent_classifier import PersistentClassifier
from nosy.model import ClassificationObject

class NaiveBayesClassifier(PersistentClassifier):
    TRAIN_RATIO = 0.75
    TEST_RATIO = 0.25

    TAGS = ClassificationObject.tags()

    TRAIN_SETS = {}
    TEST_SETS = {}

    # num(negatve_features) = NEG_FEATURE_MULTIPLIER*num(positive_features)
    NEG_FEATURE_MULTIPLIER = 10

    # UTILITIES

    @classmethod
    def _to_feature(cls, classification_object):
        bag_of_words = {}
        for w in classification_object.keywords: bag_of_words[w]= True
        return bag_of_words

    # FEATURES

    def load_features(self):
        self.features = {}
        for tag in self.TAGS: 
            self.features[tag] = []
            
            # Positive features
            tagged = ClassificationObject.find( { 'tags' : tag } )
            for c in tagged:
                bag_of_words = self._to_feature(c)
                positive_feature = (bag_of_words, tag)
                self.features[tag].append(positive_feature)

            # Negative features - we limit these to the same number as positive features
            untagged_limit = self.NEG_FEATURE_MULTIPLIER*len(self.features[tag])
            untagged = ClassificationObject.find( { 'tags' : { '$ne' : tag } }, 
                limit=untagged_limit)
            for c in untagged:
                bag_of_words = {}
                for k in c.keywords: bag_of_words[k] = True

                negative_feature = (bag_of_words, "!" + tag)
                self.features[tag].append(negative_feature)

    def _split_features(self):
        if not hasattr(self, 'features'): self.load_features()

        self.train_sets = {}
        self.test_sets = {}

        for tag, features in self.features.iteritems():
            random.shuffle(features)
            split_index = int(self.TRAIN_RATIO*len(features))

            self.train_sets[tag] = features[:split_index]
            self.test_sets[tag] = features[split_index:]

    # TRAINING

    def train(self):
        if not hasattr(self, 'train_sets'): self._split_features()

        self.classifiers = {}
        for tag, features in self.train_sets.iteritems():
            self.classifiers[tag] = NltkNaiveBayes.train(features)

    # TESTING

    def test(self):
        if not hasattr(self, 'test_sets'): self._split_features()
        if not hasattr(self, 'classifiers'): self.train()

        result = {}
        for tag, classifier in self.classifiers.iteritems():
            result[tag] = accuracy(classifier, self.test_sets[tag])
        return result

    def show_high_information_words(self, tag, n=10):
        if not hasattr(self, 'classifiers'): self.train()
        self.classifiers[tag].show_most_informative_features(n)

    # CLASSIFYING

    def classify(self, text):
        if not hasattr(self, 'classifiers'): self.train()

        # Extract keywords like we do when learning
        c = ClassificationObject()
        c.text = text
        c.process()
        feat = self._to_feature(c)
        
        result = {}
        for tag, classifier in self.classifiers.iteritems():
            result[tag] = classifier.prob_classify(feat).prob(tag)
        return result