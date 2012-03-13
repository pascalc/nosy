from nltk.corpus import wordnet

class LanguageClassifier():
    @classmethod
    def _is_english(cls, word):
        return len(wordnet.synsets(word)) > 0

    @classmethod
    def _english_score(cls, words):
        if len(words) > 0:
            return float(sum([cls._is_english(w) for w in words]))/len(words)
        else:
            return 0

    @classmethod
    def classify(cls, c):
        c.tags['english'] = cls._english_score(c.keywords)