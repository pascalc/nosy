from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
import re

from mongo_open_struct import MongoOpenStruct

class Base(MongoOpenStruct):
    ID_TYPE = long

    def __init__(self, data=None, **kwargs):
        super(Base, self).__init__(data, **kwargs)

    # Expand contractions: can't -> cannot
    EXPANSIONS = [
        (r'won\'t', 'will not'),
        (r'can\'t', 'cannot'),
        (r'\brly\b', 'really'),
        (r'\btho\b', 'though'),
        (r'\bforeva\b', 'forever'),
        (r'2nite', 'tonight'),
        (r'\bdis\b', 'this'),
        (r'\bdat\b', 'that'),
        (r'\b4get\b', 'forget'),
        (r'gonna', 'going to'),
        (r'\bimma\b', 'i am going to'),
        (r'i\'m', 'i am'),
        (r'ain\'t', 'is not'),
        (r'(\w+)\'ll', '\g<1> will'),
        (r'(\w+)n\'t', '\g<1> not'),
        (r'(\w+)\'ve', '\g<1> have'),
        (r'(\w+)\'s', '\g<1> is'),
        (r'(\w+)\'re', '\g<1> are'),
        (r'(\w+)\'d', '\g<1> would')
    ]
    EXPAND_PATTERNS = [(re.compile(regex, flags=re.I), repl) for (regex, repl) in EXPANSIONS]
    @classmethod
    def _expand_contractions(cls, text):
        s = text
        for (pattern, repl) in cls.EXPAND_PATTERNS:
            (s,count) = re.subn(pattern, repl, s)
        return s

    # Tokenize words and punctuation into separate tokens
    TOKENIZER = WordPunctTokenizer()
    @classmethod
    def _tokenize(cls, text):
        return cls.TOKENIZER.tokenize(text)

    # Contract repeated letters: loooove -> love
    REPEAT_REGEXP = re.compile(r'(\w*)(\w)\2(\w*)')
    REPEAT_REPL = r'\1\2\3'
    # Recursive helper
    @classmethod
    def _contract_repetitions_helper(cls, word):
        if wordnet.synsets(word):
            return word
        repl_word = cls.REPEAT_REGEXP.sub(cls.REPEAT_REPL, word)
        if repl_word != word:
            return cls._contract_repetitions_helper(repl_word)
        else:
            return repl_word
    # Actual function
    @classmethod
    def _contract_repetitions(cls, words):
        return [cls._contract_repetitions_helper(w) for w in words]

    # Filter common English words
    STOPS = set(stopwords.words('english'))
    STOPS.add(',')
    STOPS.add('.')
    @classmethod
    def _filter_stopwords(cls, words):
        return [w for w in words if w not in cls.STOPS]

    # ['HELLO','THERE'] -> ['hello','there']
    @classmethod
    def _downcase(cls, words):
        return map(lambda w: w.lower(), words)

    # 'cookery' -> 'cookeri'
    STEMMER = PorterStemmer()    
    @classmethod
    def stem(cls, word):
        return cls.STEMMER.stem(word)

    # Save stemmed keywords for search index
    def stem_keywords(self):
        self.stemmed_keywords = [self.stem(w) for w in self.keywords]

    # Expand contractions -> tokenize -> downcase -> contract repetitions -> filter
    def process(self):
        expanded_text = self._expand_contractions(self.text)
        words = self._tokenize(expanded_text)
        downcased_words = self._downcase(words)
        contracted_words = self._contract_repetitions(downcased_words)
        filtered_words = self._filter_stopwords(contracted_words)

        self.keywords = filtered_words
        self.stem_keywords()