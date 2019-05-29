import re
from .stemmer import ArabicStemmer
from .pos_tagger import tags as _tags
from .correction import spell_checker

available_models = (
    ('POST', 'LSTM')
)

stemmer = ArabicStemmer()

def tokens(text):
    r = re.compile(r'\w+|[^\w\s]+', re.UNICODE | re.MULTILINE | re.DOTALL)
    return r.findall(text)

def stems(text):
    return [stemmer.stem(token) for token in tokens(text)]


def tags(text):
    return _tags(text)
    

def correct(text, top=False):
    words = tokens(text)
    result = {w: spell_checker.correction(w, top) for w in words}
    return result


def sentiment(text):
    return False


def similarity(text1, text2):
    return False
