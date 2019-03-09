import unittest
import arabicnlp


class IntegrationTest(unittest.TestCase):
    """Integration test for package interface"""

    testtext = ""


    def test_tokens(self):
        """Tests for the tokenizer"""     
        cases = {
         
            "وقد تتكون النجوم في أزواج تدور حول بعضها البعض، مثال على ذلك نجده في نجم الشعرى اليمانية.":
            ["و","قد","تتكون","النجوم","في","أزواج","تدور","حول","بعضها","البعض","،","مثال"
        ,"على","ذلك","نجده","في","نجم","الشعرى","اليمانية","."],

        "يبلغ عمر كوكب الأرض حوالي 4.54 مليار سنة (4.54 × 109 سنة ± 1%).":
        ["عمر","الأرض","حوالي","4.54","مليار","سنة","(","4.54"
        ,"×","109","سنة","±","1","%",")","."]
        }

        for case, correct in cases.items():
            res = arabicnlp.tokens(case)
            self.assertEqual(len(correct),len(res))

            for i in range(len(correct)):
                self.assertEqual(correct[i],res[i])


    def test_stemming(self):
        self.assertTrue(arabicnlp.stem(self.testtext))


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
    def test_correction(self):
        
        result = []
        cases= {'توصية' : 'تتتتتتتتوصية' , 'الهام' : 'الهم', 'املائية' : 'املاءية' }
        for _, val in cases.items():
            result.append(arabicnlp.correct(val))
              
        self.assertEqual(cases.keys(),result)

    def test_stemming(self):
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

        result_list = []

        for key, value in dictionary.items():
            result_list.append(self.__lemmas_checker(key, value))
        return self.assertTrue(all(result_list), True)
            
    def __lemmas_checker(self, test_str, correct_string):
        """"
        Checking if the Algorithm's output matches the correctly initialzied values
        """
        result_string = arabicnlp.stem(test_str)
        if result_string == correct_string:
            return True
        return False


if __name__ == '__main__':
    unittest.main()