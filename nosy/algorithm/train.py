from nltk.classify.util import apply_features
from nltk.probability import FreqDist
from nosy.model import ClassificationObject

class TrainClassifier():
	@classmethod
	def __init__(cls):
		cls.word_features = []

	@classmethod
	def _get_data(cls, source):
		if source == 'db':
			data = cls._get_from_db()
		return data

	@classmethod
	def _get_from_db(cls):
		objects = ClassificationObject.find( {'tags': {'$ne' : []}})
		data = []
		for c in objects:
			keywords = c.keywords
			tags = c.tags
			keywords = [w for w in keywords] 
			for tag in tags:
				data.append((keywords, tag))
		return data

	@classmethod
	def _get_word_freq(cls, data):
		all_words = []
		for words, label in data:
			all_words.extend(words)
		freq = FreqDist(all_words)
		cls.word_features = freq.keys()

	@classmethod
	def _feature_extractor(cls, document):
		document = set(document)
		features = {}
		for word in cls.word_features:
			features['contains(%s)' % word] = word in document
		return features

	@classmethod
	def _get_trainingset(cls, source = 'db'):
		data = cls._get_data(source)
		cls._get_word_freq(data)
		return apply_features(cls._feature_extractor, data)

	def train(self):
		training_set = self._get_trainingset()
		# classifier = naivebayesclassifier.train

		
TrainClassifier().train()