from nltk.corpus import wordnet

class LanguageClassifier():
    @classmethod
    def _is_english(cls, word):
        return len(wordnet.synsets(word)) > 0

    @classmethod
    def classify(cls, c):
        score = float(sum([cls._is_english(w) for w in c.keywords]))/len(c.keywords)
        c.tags['english'] = score