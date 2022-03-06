import unittest
from crf_pos.crf import POSTagger
from crf_pos.api import downloader

pos_tagger = POSTagger("model/perpos-v1.model")
tokens = "ابراهیم رئیسی رئيس‌جمهور جمهوری اسلامی ایران می‌باشد"
print(pos_tagger[tokens])
print(pos_tagger['دانش‌آموز و دانش آموز متفاوت می باشند'])
print(pos_tagger['نهاد ریاست جمهوری'])


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model_path = 'https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v1/perpos.model'
        self.tagger = POSTagger("model/perpos-v1.model")
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADVe', 'RES', 'RESe', 'DET', 'DETe', 'AJ', 'AJe', 'CL', 'INT', 'CONJ',
                         'CONJe', 'POSTP', 'PRO', 'PROe', 'NUM', 'NUMe', 'PUNC', 'Ne', 'Pe')

    def test_api(self):
        self.assertRaises(Exception, downloader, path='wrong-path')

    def test_normalized_verb_tagging(self):
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertNotEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_tagger(self):
        self.assertIsInstance(self.tagger['رئيس‌جمهور'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0], tuple)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0][1], str)
        for item in self.tagger['رئيس‌جمهور جمهوری اسلامی']:
            self.assertIn(member=item[1], container=self.all_tags)

    def test_ai(self):
        self.assertIn(self.tagger['رئيس‌جمهور'][0][1], 'Ne')


if __name__ == '__main__':
    unittest.main()
