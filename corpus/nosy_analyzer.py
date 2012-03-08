from classification_object import ClassificationObject
from algorithm_object import AlgorithmObject
from nltk.tokenizer import WhitespaceTokenizer

# NATK
class NosyAnalyzerToolkit():
	'''
	Performs the action defined by tokenzier on the classification objects data

	@param co
		Classification object
	@param tokenizer
		Tokenizer to use on the data
	'''
	def extract_keywords(co, tokenizer):
		co.keywords = map( lambda w: w.lower, tokenizer(co.data))

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
	def simple_language_determiner(co, lang='en'):
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