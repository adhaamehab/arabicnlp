import unittest
import arabicnlp


class IntegrationTest(unittest.TestCase):
    """Integration test for package interface"""

    testtext = ""


    def test_tokens(self):
        """Tests for the tokenizer"""     
        test =  "وقد تتكون النجوم في أزواج تدور حول بعضها البعض، مثال على ذلك نجده في نجم الشعرى اليمانية."
       
        correct = ["و","قد","تتكون","النجوم","في","أزواج","تدور","حول","بعضها","البعض","،","مثال"
        ,"على","ذلك","نجده","في","نجم","الشعرى","اليمانية","."]
        
        self.__tokens_checker(test,correct)

        test = "يبلغ عمر كوكب الأرض حوالي 4.54 مليار سنة (4.54 × 109 سنة ± 1%)."
        
        correct = ["عمر","الأرض","حوالي","4.54","مليار","سنة","(","4.54"
        ,"×","109","سنة","±","1","%",")","."]
        
        self.__tokens_checker(test,correct)

    def __tokens_checker(self,test_str,correct_tokens):
        """
        A helper method Checking if a string is tokenized correctly
        
        :pram test_str: The string to be checked.
        :pram correct_tokens: A list of tokens that should be matched
        with the result of tokenizing test_str
        """
        res = arabicnlp.tokens(test_str)
        self.assertEqual(len(correct_tokens),len(res))

        for i in range(len(correct_tokens)):
             self.assertEqual(correct_tokens[i],res[i])


    def test_lemmas(self):
        self.assertTrue(arabicnlp.lemmas(self.testtext))

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