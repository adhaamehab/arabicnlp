import re
from collections import Counter
import pickle
from os import path


class TextCorrection:
    def __init__(self):
        this_dir, _ = path.split(__file__)
        WORDINDEX_PATH = path.join(this_dir, "data", "word2index.bin")
        with open(WORDINDEX_PATH, "rb") as f:
            word2index = pickle.load(f)
        self.WORDS = Counter(word2index.keys())

    def words(self, text):
        return re.findall(r"\w+", text.lower())

    def P(self, word):
        "Probability of `word`."
        N = sum(self.WORDS.values())
        return self.WORDS[word] / N

    def correction(self, word, top=False):
        "Most probable spelling correction for word."
        if top:
            return max(self.candidates(word), key=self.P)
        return self.candidates(word)

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return (
            self.known([word])
            or self.known(self.edits1(word))
            or self.known(self.edits2(word))
            or [word]
        )

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters = "غظضذخثتشرقصفعسنملكيطحزوهدجبأ"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


spell_checker = TextCorrection()
