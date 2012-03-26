from train import TrainClassifier
from nltk import NaiveBayesClassifier, MaxentClassifier

class TagsClassifier():
	@classmethod
	def __init__(self):
		self.algorithm = NaiveBayesClassifier
		self.trainer = TrainClassifier()
		self.classifier = None

	def classify(self, text):
		# if not previously trained then train else classifier = redis().get('nosy:tagsClassifier')
		self.train()
		features = self.trainer.feature_extractor(text.split())
		result = self.classifier.classify(features)
		#print self.classifier.show_most_informative_features()
		return result

	@classmethod
	def train(cls):
		training_set = cls.trainer.train() #TrainClassifier().train()
		cls.classifier = cls.algorithm.train(training_set) #NaiveBayesClassifier.train(training_set)
		
messages = [
	"there is an earthquake now",
	"i love mcdonalds more than anything",
	"riot"
	]
for msg in messages:
 	print dict([('text', msg), ('label', TagsClassifier().classify(msg))])