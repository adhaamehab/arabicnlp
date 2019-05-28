# Adapted from the NLTK package v3.0.1:
# https://github.com/nltk/nltk/blob/3.0.1/nltk/stem/snowball.py

#
# Natural Language Toolkit: Snowball Stemmer
#
# Copyright (C) 2001-2014 NLTK Project
# Author: Peter Michael Stahl <pemistahl@gmail.com>
#         Peter Ljunglof <peter.ljunglof@heatherleaf.se> (revisions)
# Algorithms: Dr Martin Porter <martin@tartarus.org>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
Snowball stemmers

This module provides a port of the Snowball stemmers
developed by Martin Porter.

"""

import re
from .porter import PorterStemmer

def suffix_replace(original, old, new):
    """
    Replaces the old suffix of the original string by a new suffix
    """
    return original[: -len(old)] + new

 
def prefix_replace(original, old, new):
    """
    Replaces the old prefix of the original string by a new suffix
    :param original: string
    :param old: string
    :param new: string
    :return: string
    """
    return new + original[len(old) :]


class SnowballStemmer():

    """
    Snowball Stemmer

    The following languages are supported:
    Danish, Dutch, English, Finnish, French, German,
    Hungarian, Italian, Norwegian, Portuguese, Romanian, Russian,
    Spanish and Swedish.

    The algorithm for English is documented here:

        Porter, M. \"An algorithm for suffix stripping.\"
        Program 14.3 (1980): 130-137.

    The algorithms have been developed by Martin Porter.
    These stemmers are called Snowball, because Porter created
    a programming language with this name for creating
    new stemming algorithms. There is more information available
    at http://snowball.tartarus.org/

    The stemmer is invoked as shown below:

    >>> from summa.preprocessing.snowball import SnowballStemmer
    >>> print(" ".join(SnowballStemmer.languages)) # See which languages are supported
    ...
    >>> stemmer = SnowballStemmer("german") # Choose a language
    >>> stemmer.stem("Autobahnen") # Stem a word
    'autobahn'

    Invoking the stemmers that way is useful if you do not know the
    language to be stemmed at runtime. Alternatively, if you already know
    the language, then you can invoke the language specific stemmer directly:

    >>> from summa.preprocessing.snowball import GermanStemmer
    >>> stemmer = GermanStemmer()
    >>> stemmer.stem("Autobahnen")
    'autobahn'

    :param language: The language whose subclass is instantiated.
    :type language: str or unicode
    :raise ValueError: If there is no stemmer for the specified
                           language, a ValueError is raised.
    """

    languages = (
        "arabic",
        "danish",
        "dutch",
        "english",
        "finnish",
        "french",
        "german",
        "hungarian",
        "italian",
        "norwegian",
        "polish",
        "portuguese",
        "romanian",
        "russian",
        "spanish",
        "swedish",
    )

    def __init__(self, language):
        if language not in self.languages:
            raise ValueError("The language '%s' is not supported." % language)
        stemmerclass = globals()[language.capitalize() + "Stemmer"]
        self.stemmer = stemmerclass()
        self.stem = self.stemmer.stem


class _LanguageSpecificStemmer():

    """
    This helper subclass offers the possibility
    to invoke a specific stemmer directly.
    This is useful if you already know the language to be stemmed at runtime.

    Create an instance of the Snowball stemmer.
    """

    def __init__(self):
        # The language is the name of the class, minus the final "Stemmer".
        language = type(self).__name__.lower()
        if language.endswith("stemmer"):
            language = language[:-7]

    def __repr__(self):
        """
        Print out the string representation of the respective class.

        """
        return "<%s>" % type(self).__name__


class PorterStemmer(_LanguageSpecificStemmer, PorterStemmer):
    """
    A word stemmer based on the original Porter stemming algorithm.

        Porter, M. \"An algorithm for suffix stripping.\"
        Program 14.3 (1980): 130-137.

    A few minor modifications have been made to Porter's basic
    algorithm.  See the source code of the module
    nltk.stem.porter for more information.

    """
    def __init__(self):
        _LanguageSpecificStemmer.__init__(self)
        PorterStemmer.__init__(self)


class _StandardStemmer(_LanguageSpecificStemmer):

    """
    This subclass encapsulates two methods for defining the standard versions
    of the string regions R1, R2, and RV.

    """

    def _r1r2_standard(self, word, vowels):
        """
        Return the standard interpretations of the string regions R1 and R2.

        R1 is the region after the first non-vowel following a vowel,
        or is the null region at the end of the word if there is no
        such non-vowel.

        R2 is the region after the first non-vowel following a vowel
        in R1, or is the null region at the end of the word if there
        is no such non-vowel.

        :param word: The word whose regions R1 and R2 are determined.
        :type word: str or unicode
        :param vowels: The vowels of the respective language that are
                       used to determine the regions R1 and R2.
        :type vowels: unicode
        :return: (r1,r2), the regions R1 and R2 for the respective word.
        :rtype: tuple
        :note: This helper method is invoked by the respective stem method of
               the subclasses DutchStemmer, FinnishStemmer,
               FrenchStemmer, GermanStemmer, ItalianStemmer,
               PortugueseStemmer, RomanianStemmer, and SpanishStemmer.
               It is not to be invoked directly!
        :note: A detailed description of how to define R1 and R2
               can be found at http://snowball.tartarus.org/texts/r1r2.html

        """
        r1 = ""
        r2 = ""
        for i in range(1, len(word)):
            if word[i] not in vowels and word[i-1] in vowels:
                r1 = word[i+1:]
                break

        for i in range(1, len(r1)):
            if r1[i] not in vowels and r1[i-1] in vowels:
                r2 = r1[i+1:]
                break

        return (r1, r2)



    def _rv_standard(self, word, vowels):
        """
        Return the standard interpretation of the string region RV.

        If the second letter is a consonant, RV is the region after the
        next following vowel. If the first two letters are vowels, RV is
        the region after the next following consonant. Otherwise, RV is
        the region after the third letter.

        :param word: The word whose region RV is determined.
        :type word: str or unicode
        :param vowels: The vowels of the respective language that are
                       used to determine the region RV.
        :type vowels: unicode
        :return: the region RV for the respective word.
        :rtype: unicode
        :note: This helper method is invoked by the respective stem method of
               the subclasses ItalianStemmer, PortugueseStemmer,
               RomanianStemmer, and SpanishStemmer. It is not to be
               invoked directly!

        """
        rv = ""
        if len(word) >= 2:
            if word[1] not in vowels:
                for i in range(2, len(word)):
                    if word[i] in vowels:
                        rv = word[i+1:]
                        break

            elif word[:2] in vowels:
                for i in range(2, len(word)):
                    if word[i] not in vowels:
                        rv = word[i+1:]
                        break
            else:
                rv = word[3:]

        return rv


class ArabicStemmer(_StandardStemmer, _LanguageSpecificStemmer):

    # Normalize_pre stes
    __vocalization = re.compile(
        r'[\u064b-\u064c-\u064d-\u064e-\u064f-\u0650-\u0651-\u0652]'
    )

    __kasheeda = re.compile(r'[\u0640]')  # ـ tatweel/kasheeda

    __arabic_punctuation_marks = re.compile(r'[\u060C-\u061B-\u061F]')  #  ؛ ، ؟

    # Normalize_post
    __last_hamzat = ('\u0623', '\u0625', '\u0622', '\u0624', '\u0626')  # أ، إ، آ، ؤ، ئ

    # normalize other hamza's
    __initial_hamzat = re.compile(r'^[\u0622\u0623\u0625]')  #  أ، إ، آ

    __waw_hamza = re.compile(r'[\u0624]')  # ؤ

    __yeh_hamza = re.compile(r'[\u0626]')  # ئ

    __alefat = re.compile(r'[\u0623\u0622\u0625]')  #  أ، إ، آ

    # Checks
    __checks1 = (
        '\u0643\u0627\u0644',
        '\u0628\u0627\u0644',  # بال، كال
        '\u0627\u0644',
        '\u0644\u0644',  # لل، ال
    )

    __checks2 = ('\u0629', '\u0627\u062a')  # ة  #  female plural ات

    # Suffixes
    __suffix_noun_step1a = (
        '\u064a',
        '\u0643',
        '\u0647',  # ي، ك، ه
        '\u0646\u0627',
        '\u0643\u0645',
        '\u0647\u0627',
        '\u0647\u0646',
        '\u0647\u0645',  # نا، كم، ها، هن، هم
        '\u0643\u0645\u0627',
        '\u0647\u0645\u0627',  # كما، هما
    )

    __suffix_noun_step1b = '\u0646'  # ن

    __suffix_noun_step2a = ('\u0627', '\u064a', '\u0648')  # ا، ي، و

    __suffix_noun_step2b = '\u0627\u062a'  # ات

    __suffix_noun_step2c1 = '\u062a'  # ت

    __suffix_noun_step2c2 = '\u0629'  # ة

    __suffix_noun_step3 = '\u064a'  # ي

    __suffix_verb_step1 = (
        '\u0647',
        '\u0643',  # ه، ك
        '\u0646\u064a',
        '\u0646\u0627',
        '\u0647\u0627',
        '\u0647\u0645',  # ني، نا، ها، هم
        '\u0647\u0646',
        '\u0643\u0645',
        '\u0643\u0646',  # هن، كم، كن
        '\u0647\u0645\u0627',
        '\u0643\u0645\u0627',
        '\u0643\u0645\u0648',  # هما، كما، كمو
    )

    __suffix_verb_step2a = (
        '\u062a',
        '\u0627',
        '\u0646',
        '\u064a',  # ت، ا، ن، ي
        '\u0646\u0627',
        '\u062a\u0627',
        '\u062a\u0646',  # نا، تا، تن Past
        '\u0627\u0646',
        '\u0648\u0646',
        '\u064a\u0646',  # ان، هن، ين Present
        '\u062a\u0645\u0627',  # تما
    )

    __suffix_verb_step2b = ('\u0648\u0627', '\u062a\u0645')  # وا، تم

    __suffix_verb_step2c = ('\u0648', '\u062a\u0645\u0648')  # و  # تمو

    __suffix_all_alef_maqsura = '\u0649'  # ى

    # Prefixes
    __prefix_step1 = (
        '\u0623',  # أ
        '\u0623\u0623',
        '\u0623\u0622',
        '\u0623\u0624',
        '\u0623\u0627',
        '\u0623\u0625',  # أأ، أآ، أؤ، أا، أإ
    )

    __prefix_step2a = ('\u0641\u0627\u0644', '\u0648\u0627\u0644')  # فال، وال

    __prefix_step2b = ('\u0641', '\u0648')  # ف، و

    __prefix_step3a_noun = (
        '\u0627\u0644',
        '\u0644\u0644',  # لل، ال
        '\u0643\u0627\u0644',
        '\u0628\u0627\u0644',  # بال، كال
    )

    __prefix_step3b_noun = (
        '\u0628',
        '\u0643',
        '\u0644',  # ب، ك، ل
        '\u0628\u0628',
        '\u0643\u0643',  # بب، كك
    )

    __prefix_step3_verb = (
        '\u0633\u064a',
        '\u0633\u062a',
        '\u0633\u0646',
        '\u0633\u0623',
    )  # سي، ست، سن، سأ

    __prefix_step4_verb = (
        '\u064a\u0633\u062a',
        '\u0646\u0633\u062a',
        '\u062a\u0633\u062a',
    )  # يست، نست، تست

    # Suffixes added due to Conjugation Verbs
    __conjugation_suffix_verb_1 = ('\u0647', '\u0643')  # ه، ك

    __conjugation_suffix_verb_2 = (
        '\u0646\u064a',
        '\u0646\u0627',
        '\u0647\u0627',  # ني، نا، ها
        '\u0647\u0645',
        '\u0647\u0646',
        '\u0643\u0645',  # هم، هن، كم
        '\u0643\u0646',  # كن
    )
    __conjugation_suffix_verb_3 = (
        '\u0647\u0645\u0627',
        '\u0643\u0645\u0627',
        '\u0643\u0645\u0648',
    )  # هما، كما، كمو

    __conjugation_suffix_verb_4 = ('\u0627', '\u0646', '\u064a')  # ا، ن، ي

    __conjugation_suffix_verb_past = (
        '\u0646\u0627',
        '\u062a\u0627',
        '\u062a\u0646',
    )  # نا، تا، تن

    __conjugation_suffix_verb_present = (
        '\u0627\u0646',
        '\u0648\u0646',
        '\u064a\u0646',
    )  # ان، ون، ين

    # Suffixes added due to derivation Names
    __conjugation_suffix_noun_1 = ('\u064a', '\u0643', '\u0647')  # ي، ك، ه

    __conjugation_suffix_noun_2 = (
        '\u0646\u0627',
        '\u0643\u0645',  # نا، كم
        '\u0647\u0627',
        '\u0647\u0646',
        '\u0647\u0645',  # ها، هن، هم
    )

    __conjugation_suffix_noun_3 = (
        '\u0643\u0645\u0627',
        '\u0647\u0645\u0627',
    )  # كما، هما

    # Prefixes added due to derivation Names
    __prefixes1 = ('\u0648\u0627', '\u0641\u0627')  # فا، وا

    __articles_3len = ('\u0643\u0627\u0644', '\u0628\u0627\u0644')  # بال كال

    __articles_2len = ('\u0627\u0644', '\u0644\u0644')  # ال لل

    # Prepositions letters
    __prepositions1 = ('\u0643', '\u0644')  # ك، ل
    __prepositions2 = ('\u0628\u0628', '\u0643\u0643')  # بب، كك

    is_verb = True
    is_noun = True
    is_defined = False

    suffixes_verb_step1_success = False
    suffix_verb_step2a_success = False
    suffix_verb_step2b_success = False
    suffix_noun_step2c2_success = False
    suffix_noun_step1a_success = False
    suffix_noun_step2a_success = False
    suffix_noun_step2b_success = False
    suffixe_noun_step1b_success = False
    prefix_step2a_success = False
    prefix_step3a_noun_success = False
    prefix_step3b_noun_success = False

    def __normalize_pre(self, token):
        """
        :param token: string
        :return: normalized token type string
        """
        # strip diacritics
        token = self.__vocalization.sub('', token)
        # strip kasheeda
        token = self.__kasheeda.sub('', token)
        # strip punctuation marks
        token = self.__arabic_punctuation_marks.sub('', token)
        return token

    def __normalize_post(self, token):
        # normalize last hamza
        for hamza in self.__last_hamzat:
            if token.endswith(hamza):
                token = suffix_replace(token, hamza, '\u0621')
                break
        # normalize other hamzat
        token = self.__initial_hamzat.sub('\u0627', token)
        token = self.__waw_hamza.sub('\u0648', token)
        token = self.__yeh_hamza.sub('\u064a', token)
        token = self.__alefat.sub('\u0627', token)
        return token

    def __checks_1(self, token):
        for prefix in self.__checks1:
            if token.startswith(prefix):
                if prefix in self.__articles_3len and len(token) > 4:
                    self.is_noun = True
                    self.is_verb = False
                    self.is_defined = True
                    break

                if prefix in self.__articles_2len and len(token) > 3:
                    self.is_noun = True
                    self.is_verb = False
                    self.is_defined = True
                    break

    def __checks_2(self, token):
        for suffix in self.__checks2:
            if token.endswith(suffix):
                if suffix == '\u0629' and len(token) > 2:
                    self.is_noun = True
                    self.is_verb = False
                    break

                if suffix == '\u0627\u062a' and len(token) > 3:
                    self.is_noun = True
                    self.is_verb = False
                    break

    def __Suffix_Verb_Step1(self, token):
        for suffix in self.__suffix_verb_step1:
            if token.endswith(suffix):
                if suffix in self.__conjugation_suffix_verb_1 and len(token) >= 4:
                    token = token[:-1]
                    self.suffixes_verb_step1_success = True
                    break

                if suffix in self.__conjugation_suffix_verb_2 and len(token) >= 5:
                    token = token[:-2]
                    self.suffixes_verb_step1_success = True
                    break

                if suffix in self.__conjugation_suffix_verb_3 and len(token) >= 6:
                    token = token[:-3]
                    self.suffixes_verb_step1_success = True
                    break
        return token

    def __Suffix_Verb_Step2a(self, token):
        for suffix in self.__suffix_verb_step2a:
            if token.endswith(suffix) and len(token) > 3:
                if suffix == '\u062a' and len(token) >= 4:
                    token = token[:-1]
                    self.suffix_verb_step2a_success = True
                    break

                if suffix in self.__conjugation_suffix_verb_4 and len(token) >= 4:
                    token = token[:-1]
                    self.suffix_verb_step2a_success = True
                    break

                if suffix in self.__conjugation_suffix_verb_past and len(token) >= 5:
                    token = token[:-2]  # past
                    self.suffix_verb_step2a_success = True
                    break

                if suffix in self.__conjugation_suffix_verb_present and len(token) > 5:
                    token = token[:-2]  # present
                    self.suffix_verb_step2a_success = True
                    break

                if suffix == '\u062a\u0645\u0627' and len(token) >= 6:
                    token = token[:-3]
                    self.suffix_verb_step2a_success = True
                    break
        return token

    def __Suffix_Verb_Step2c(self, token):
        for suffix in self.__suffix_verb_step2c:
            if token.endswith(suffix):
                if suffix == '\u062a\u0645\u0648' and len(token) >= 6:
                    token = token[:-3]
                    break

                if suffix == '\u0648' and len(token) >= 4:
                    token = token[:-1]
                    break
        return token

    def __Suffix_Verb_Step2b(self, token):
        for suffix in self.__suffix_verb_step2b:
            if token.endswith(suffix) and len(token) >= 5:
                token = token[:-2]
                self.suffix_verb_step2b_success = True
                break
        return token

    def __Suffix_Noun_Step2c2(self, token):
        for suffix in self.__suffix_noun_step2c2:
            if token.endswith(suffix) and len(token) >= 3:
                token = token[:-1]
                self.suffix_noun_step2c2_success = True
                break
        return token

    def __Suffix_Noun_Step1a(self, token):
        for suffix in self.__suffix_noun_step1a:
            if token.endswith(suffix):
                if suffix in self.__conjugation_suffix_noun_1 and len(token) >= 4:
                    token = token[:-1]
                    self.suffix_noun_step1a_success = True
                    break

                if suffix in self.__conjugation_suffix_noun_2 and len(token) >= 5:
                    token = token[:-2]
                    self.suffix_noun_step1a_success = True
                    break

                if suffix in self.__conjugation_suffix_noun_3 and len(token) >= 6:
                    token = token[:-3]
                    self.suffix_noun_step1a_success = True
                    break
        return token

    def __Suffix_Noun_Step2a(self, token):
        for suffix in self.__suffix_noun_step2a:
            if token.endswith(suffix) and len(token) > 4:
                token = token[:-1]
                self.suffix_noun_step2a_success = True
                break
        return token

    def __Suffix_Noun_Step2b(self, token):
        for suffix in self.__suffix_noun_step2b:
            if token.endswith(suffix) and len(token) >= 5:
                token = token[:-2]
                self.suffix_noun_step2b_success = True
                break
        return token

    def __Suffix_Noun_Step2c1(self, token):
        for suffix in self.__suffix_noun_step2c1:
            if token.endswith(suffix) and len(token) >= 4:
                token = token[:-1]
                break
        return token

    def __Suffix_Noun_Step1b(self, token):
        for suffix in self.__suffix_noun_step1b:
            if token.endswith(suffix) and len(token) > 5:
                token = token[:-1]
                self.suffixe_noun_step1b_success = True
                break
        return token

    def __Suffix_Noun_Step3(self, token):
        for suffix in self.__suffix_noun_step3:
            if token.endswith(suffix) and len(token) >= 3:
                token = token[:-1]  # ya' nisbiya
                break
        return token

    def __Suffix_All_alef_maqsura(self, token):
        for suffix in self.__suffix_all_alef_maqsura:
            if token.endswith(suffix):
                token = suffix_replace(token, suffix, '\u064a')
        return token

    def __Prefix_Step1(self, token):
        for prefix in self.__prefix_step1:
            if token.startswith(prefix) and len(token) > 3:
                if prefix == '\u0623\u0623':
                    token = prefix_replace(token, prefix, '\u0623')
                    break

                elif prefix == '\u0623\u0622':
                    token = prefix_replace(token, prefix, '\u0622')
                    break

                elif prefix == '\u0623\u0624':
                    token = prefix_replace(token, prefix, '\u0624')
                    break

                elif prefix == '\u0623\u0627':
                    token = prefix_replace(token, prefix, '\u0627')
                    break

                elif prefix == '\u0623\u0625':
                    token = prefix_replace(token, prefix, '\u0625')
                    break
        return token

    def __Prefix_Step2a(self, token):
        for prefix in self.__prefix_step2a:
            if token.startswith(prefix) and len(token) > 5:
                token = token[len(prefix) :]
                self.prefix_step2a_success = True
                break
        return token

    def __Prefix_Step2b(self, token):
        for prefix in self.__prefix_step2b:
            if token.startswith(prefix) and len(token) > 3:
                if token[:2] not in self.__prefixes1:
                    token = token[len(prefix) :]
                    break
        return token

    def __Prefix_Step3a_Noun(self, token):
        for prefix in self.__prefix_step3a_noun:
            if token.startswith(prefix):
                if prefix in self.__articles_2len and len(token) > 4:
                    token = token[len(prefix) :]
                    self.prefix_step3a_noun_success = True
                    break
                if prefix in self.__articles_3len and len(token) > 5:
                    token = token[len(prefix) :]
                    break
        return token

    def __Prefix_Step3b_Noun(self, token):
        for prefix in self.__prefix_step3b_noun:
            if token.startswith(prefix):
                if len(token) > 3:
                    if prefix == '\u0628':
                        token = token[len(prefix) :]
                        self.prefix_step3b_noun_success = True
                        break

                    if prefix in self.__prepositions2:
                        token = prefix_replace(token, prefix, prefix[1])
                        self.prefix_step3b_noun_success = True
                        break

                if prefix in self.__prepositions1 and len(token) > 4:
                    token = token[len(prefix) :]  # BUG: cause confusion
                    self.prefix_step3b_noun_success = True
                    break
        return token

    def __Prefix_Step3_Verb(self, token):
        for prefix in self.__prefix_step3_verb:
            if token.startswith(prefix) and len(token) > 4:
                token = prefix_replace(token, prefix, prefix[1])
                break
        return token

    def __Prefix_Step4_Verb(self, token):
        for prefix in self.__prefix_step4_verb:
            if token.startswith(prefix) and len(token) > 4:
                token = prefix_replace(token, prefix, '\u0627\u0633\u062a')
                self.is_verb = True
                self.is_noun = False
                break
        return token

    def stem(self, word):
        """
         Stem an Arabic word and return the stemmed form.
        :param word: string
        :return: string
        """
        # set initial values
        self.is_verb = True
        self.is_noun = True
        self.is_defined = False

        self.suffix_verb_step2a_success = False
        self.suffix_verb_step2b_success = False
        self.suffix_noun_step2c2_success = False
        self.suffix_noun_step1a_success = False
        self.suffix_noun_step2a_success = False
        self.suffix_noun_step2b_success = False
        self.suffixe_noun_step1b_success = False
        self.prefix_step2a_success = False
        self.prefix_step3a_noun_success = False
        self.prefix_step3b_noun_success = False

        modified_word = word
        # guess type and properties
        # checks1
        self.__checks_1(modified_word)
        # checks2
        self.__checks_2(modified_word)
        # Pre_Normalization
        modified_word = self.__normalize_pre(modified_word)
        # Start stemming
        if self.is_verb:
            modified_word = self.__Suffix_Verb_Step1(modified_word)
            if self.suffixes_verb_step1_success:
                modified_word = self.__Suffix_Verb_Step2a(modified_word)
                if not self.suffix_verb_step2a_success:
                    modified_word = self.__Suffix_Verb_Step2c(modified_word)
                # or next TODO: How to deal with or next instruction
            else:
                modified_word = self.__Suffix_Verb_Step2b(modified_word)
                if not self.suffix_verb_step2b_success:
                    modified_word = self.__Suffix_Verb_Step2a(modified_word)
        if self.is_noun:
            modified_word = self.__Suffix_Noun_Step2c2(modified_word)
            if not self.suffix_noun_step2c2_success:
                if not self.is_defined:
                    modified_word = self.__Suffix_Noun_Step1a(modified_word)
                    # if self.suffix_noun_step1a_success:
                    modified_word = self.__Suffix_Noun_Step2a(modified_word)
                    if not self.suffix_noun_step2a_success:
                        modified_word = self.__Suffix_Noun_Step2b(modified_word)
                    if (
                        not self.suffix_noun_step2b_success
                        and not self.suffix_noun_step2a_success
                    ):
                        modified_word = self.__Suffix_Noun_Step2c1(modified_word)
                    # or next ? todo : how to deal with or next
                else:
                    modified_word = self.__Suffix_Noun_Step1b(modified_word)
                    if self.suffixe_noun_step1b_success:
                        modified_word = self.__Suffix_Noun_Step2a(modified_word)
                        if not self.suffix_noun_step2a_success:
                            modified_word = self.__Suffix_Noun_Step2b(modified_word)
                        if (
                            not self.suffix_noun_step2b_success
                            and not self.suffix_noun_step2a_success
                        ):
                            modified_word = self.__Suffix_Noun_Step2c1(modified_word)
                    else:
                        if not self.is_defined:
                            modified_word = self.__Suffix_Noun_Step2a(modified_word)
                        modified_word = self.__Suffix_Noun_Step2b(modified_word)
            modified_word = self.__Suffix_Noun_Step3(modified_word)
        if not self.is_noun and self.is_verb:
            modified_word = self.__Suffix_All_alef_maqsura(modified_word)

        # prefixes
        modified_word = self.__Prefix_Step1(modified_word)
        modified_word = self.__Prefix_Step2a(modified_word)
        if not self.prefix_step2a_success:
            modified_word = self.__Prefix_Step2b(modified_word)
        modified_word = self.__Prefix_Step3a_Noun(modified_word)
        if not self.prefix_step3a_noun_success and self.is_noun:
            modified_word = self.__Prefix_Step3b_Noun(modified_word)
        else:
            if not self.prefix_step3b_noun_success and self.is_verb:
                modified_word = self.__Prefix_Step3_Verb(modified_word)
                modified_word = self.__Prefix_Step4_Verb(modified_word)

        # post normalization stemming
        modified_word = self.__normalize_post(modified_word)
        stemmed_word = modified_word
        return stemmed_word