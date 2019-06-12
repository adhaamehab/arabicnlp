import re
import numpy as np
import gensim

from gensim.models.KeyedVectors import load_word2vec_format
from scipy import spatial

from textblob_ar.tokenizer import NLTKWordPunctTokenizer
from textblob_ar.utils import clean_str


def clean_str(text):
    search = [
        "أ",
        "إ",
        "آ",
        "ة",
        "_",
        "-",
        "/",
        ".",
        "،",
        " و ",
        " يا ",
        '"',
        "ـ",
        "'",
        "ى",
        "\\",
        "\n",
        "\t",
        "&quot;",
        "?",
        "؟",
        "!",
    ]
    replace = [
        "ا",
        "ا",
        "ا",
        "ه",
        " ",
        " ",
        "",
        "",
        "",
        " و",
        " يا",
        "",
        "",
        "",
        "ي",
        "",
        " ",
        " ",
        " ",
        " ? ",
        " ؟ ",
        " ! ",
    ]

    p_tashkeel = re.compile(r"[\u0617-\u061A\u064B-\u0652]")
    text = re.sub(p_tashkeel, "", text)
    p_longation = re.compile(r"(.)\1+")
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)
    text = text.replace("وو", "و")
    text = text.replace("يي", "ي")
    text = text.replace("اا", "ا")

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])
    text = text.strip()

    return text


class TextSimilarity:
    def __init__(self):
        try:
            self.model = gensim.models.KeyedVectors.load_word2vec_format("wiki.ar.vec")
            self.index2word_set = set(self.model.wv.index2word)
        except FileNotFoundError:
            raise FileNotFoundError

    def avg_feature_vector(self, sentence, num_features=300):
        words = NLTKWordPunctTokenizer().tokenize(clean_str(sentence))
        feature_vec = np.zeros((num_features,), dtype="float32")
        n_words = 0
        for word in words:
            if word in self.index2word_set:
                n_words += 1
                feature_vec = np.add(feature_vec, self.model[word])
        if n_words > 0:
            feature_vec = np.divide(feature_vec, n_words)
        return feature_vec

    def similarity(self, sentence1, sentence2):
        vec1, vec2 = (
            self.avg_feature_vector(sentence1),
            self.avg_feature_vector(sentence2),
        )
        return self.cosine_similarity(vec1, vec2)

    def cosine_similarity(self, vec1, vec2):
        return 1 - spatial.distance.manhatten(vec1, vec2)
