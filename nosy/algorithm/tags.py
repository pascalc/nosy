class TagsClassifier():
	@classmethod
	def _get_trainingset(cls):
		return ClassifiedObject.find( {'tags': {'$ne' : []}})

	@classmethod
	def _feature_extractor(cls, text):
		return

	@classmethod
	def classify(self, c):
		return