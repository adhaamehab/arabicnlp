import unittest
import arabicnlp


class IntegrationTest(unittest.TestCase):
    """Integration test for package interface"""

    testtext = "يتحدث اللغه العربيه حوالي مليار شخص حول العالم"

    def test_tokenization(self):
        self.assertTrue(arabicnlp.tokens(self.testtext))

    def test_stemming(self):
        self.assertTrue(arabicnlp.stems(self.testtext))

    def test_tags(self):
        self.assertTrue(arabicnlp.tags(self.testtext))

    def test_spelling(self):
        self.assertTrue(arabicnlp.correct(self.testtext, top=True))

    def test_sentiment(self):
        self.assertTrue(arabicnlp.sentiment(self.testtext))

    def test_similarity(self):
        self.assertTrue(arabicnlp.similarity(self.testtext, self.testtext))


if __name__ == "__main__":
    unittest.main()
