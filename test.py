import unittest
import arabicnlp


class IntegrationTest(unittest.TestCase):
    """Integration test for package interface"""

    testtext = ""


    def test_tokens(self):
        self.assertTrue(arabicnlp.tokens(self.testtext))

    def test_lemmas(self):
        dictionary = {
            "فليكن عندك الشجاعة لتفعل بدلاً من أن تقوم برد فعل " : "فلك عند شجع فعل بدل من ان تقم برد فعل",
            "محمود و مهاب اصحاب منذ الطفولة" : "حمد و هاب صحب منذ طفل",
            "المَدّ و الجَزْر يحدثان في البحر" : "الم د و الج ز ر حدث في بحر",
            "لا يتوقف الناس عن اللعب لأنهم كبروا، بل يكبرون لأنهم توقفوا عن اللعب" : "لا وقف لنس عن لعب أنهم كبرو ، بل كبر أنهم وقف عن لعب",
            "فهرس مقالات عربية رائعة" : "هرس قال عرب رئع",
            "سينتقل من خلالها من روضة أنيقة إلى روضة ثانية" : "نقل من خلل من روض جمل الى روض ثني",
            "كما أن بعض تلك المقالات قد خرجت في طباعة رديئة" : "كما ان بعض تلك قال قد خرج في طبع ردئ",
            "تختصر عليه كثيراً من الوقت والجهد" : "خصر عليه كثر من الق جهد",
            "بسم الله الرحمن الرحيم" : "بسم الل رحم رحم",
            " تشتمل على أبواب متفرقة" : "شمل على بوب تفرق",
            
        }

        for x,y in dictionary.items():
            self.lemmas_checker(x,y)
        self.assertTrue(arabicnlp.stem(self.testtext))

    def lemmas_checker(self,test_str,correct_string):
        """"
        Checking if the Algorithm's output matches the correctly initialzied values
        """
        result_string = arabicnlp.stem(test_str)
        self.assertEqual(correct_string,result_string)


    def test_tags(self):
        self.assertTrue(arabicnlp.tags(self.testtext))

    def test_spelling(self):
        self.assertTrue(arabicnlp.correct(self.testtext))

    def test_sentiment(self):
        self.assertTrue(arabicnlp.sentiment(self.testtext))

    def test_similarity(self):
        self.assertTrue(arabicnlp.similarity(self.testtext, self.testtext))


class UnitTest(unittest.TestCase):
    """Unit test here"""
    pass


if __name__ == '__main__':
    unittest.main()