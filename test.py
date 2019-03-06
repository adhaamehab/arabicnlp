import unittest
import arabicnlp


class IntegrationTest(unittest.TestCase):
    """Integration test for package interface"""

    testtext = ""


    def test_tokens(self):
        """tests for the tokenizer"""     
        test =  "وقد تتكون النجوم في أزواج تدور حول بعضها البعض، مثال على ذلك نجده في نجم الشعرى اليمانية."
       
        correct = ["و","قد","تتكون","النجوم","في","أزواج","تدور","حول","بعضها","البعض","،","مثال"
        ,"على","ذلك","نجده","في","نجم","الشعرى","اليمانية","."]
        
        res = arabicnlp.tokens(test)
        self.assertEqual(len(correct),len(res))

        for i in range(len(correct)):
             self.assertEqual(correct[i],res[i])

        test = "آخر رسالة لمسبار أبورتيونيتي كانت مناظرة ل'my battery is low and it is getting dark.', كما ذكر مراسل KPCC جاكوب موراليس."
        
        correct = ["آخر","رسالة","لمسبار","أبورتيونيتي","كانت","مناظرة"
        ,"ل","'","my","battery","is","low","and","it","is","getting","dark"
        ,".","'",",","كما","ذكر","مراسل","KPCC","جاكوب","موراليس","."]

        res = arabicnlp.tokens(test)
        self.assertEqual(len(correct),len(res))

        for i in range(len(correct)):
             self.assertEqual(correct[i],res[i])


        test = "يبلغ عمر كوكب الأرض حوالي 4.54 مليار سنة (4.54 × 109 سنة ± 1%)."
        
        correct = ["عمر","الأرض","حوالي","4.54","مليار","سنة","(","4.54"
        ,"×","109","سنة","±","1","%",")","."]

        res = arabicnlp.tokens(test)
        self.assertEqual(len(correct),len(res))

        for i in range(len(correct)):
             self.assertEqual(correct[i],res[i])
        


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