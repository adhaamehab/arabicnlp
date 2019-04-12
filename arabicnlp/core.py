import re
from .preprocessing import ArabicStemmer


available_models = (
    ('POST', 'LSTM'),
    ('POST', 'NGRAM')
)

stemmer = ArabicStemmer()

def tokens(text):
    r = re.compile(r'\w+|[^\w\s]+', re.UNICODE | re.MULTILINE | re.DOTALL)
    return r.findall(text)

def stem(text):
    return [stemmer.stem(token) for token in tokens(text)]


def tags(text, model='LSTM'):
    

def correct(text):
    return False


def sentiment(text):
    return False


def similarity(text1, text2):
    return False

def download(name):
    pass
