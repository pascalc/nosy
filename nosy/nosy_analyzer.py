import nltk

from nltk.tokenize import WhitespaceTokenizer

from classification_object import ClassificationObject
#from algorithm_object import AlgorithmObject

# NATK
class NosyAnalyzerToolkit():
	TOKENIZER = WhitespaceTokenizer()

	'''
	Performs the action defined by tokenzier on the classification objects data

	@param text
		A string to seperate
	@param tokenizer
		Tokenizer to use on the data
	'''
	def seperate_words(self, text):
		words = map( lambda w: w.lower(), self.TOKENIZER.tokenize(text))
		return words

	'''
	Based on a dictionary with the 100 most common 'lang' words and 
	25 most common 'lang' nouns/verbs/adjectives do simple classification of the language.
	Counts the number of occurrences of each word and based on the score determines if it
	belongs to 'lang'

	@param co
		Classification object
	@param lang
		Language dictionary to use
	'''
	def simple_language_detector(self, co, lang='en'):
		counter = {
			"words" : 0,
			"nouns" : 0,
			"verbs" : 0,
			"adjectives" : 0
		}
		# dict = connect_to_dict['dict'][lang]
		# for word in co.data
		# 	for key in counter
		# 		word in dict[key] do ++counter[key]

		# if counter.value gt threshold then co.category = lang else co.category = 'undefined'

	'''
	http://code.google.com/p/nltk/source/browse/trunk/nltk_contrib/nltk_contrib/misc/langid.py

	Finds the word that does NOT EXIST in the english vocabulary. If a word does not exists,
	the language is simply not english 
	'''
	def nltk_language_detector_en(self, text):
		text = self.seperate_words(text)
		english_vocab = set(w.lower() for w in nltk.corpus.words.words())
		text_vocab = set(w.lower() for w in text if w.lower().isalpha())
		output = text_vocab.difference(english_vocab)
		lang = 'en' 
		if len(output) == 0:
			lang = 'undefined'

		res = {
			"language": lang,
			"output": output
		}
		return res

	def _prep_string(self, s):
		return map( lambda w: w.lower(), s.split(' '))
		

nalt = NosyAnalyzerToolkit()
s = "I am an evil monkey with an urge to take over the WORLD from the humans"
print nalt.nltk_language_detector_en(s)
print nalt.seperate_words(s)