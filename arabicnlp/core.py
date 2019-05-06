import re
from .preprocessing import ArabicStemmer
from .models import tags as _tags

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
    

def correct(text):
    return False


def sentiment(text):
    return False


def similarity(text1, text2):
    return False
