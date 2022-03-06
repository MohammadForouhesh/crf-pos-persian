import unittest
from crf_pos.crf import CrfPosTagger
from crf_pos.api import downloader
from crf_pos.wapiti import WapitiPosTagger


class CrfTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model_path = 'https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v1/perpos.model'
        self.tagger = CrfPosTagger("model/perpos-v1.model")
        self.wapiti = WapitiPosTagger(model_path="model/UPC_full_model_wapiti")
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADVe', 'RES', 'RESe', 'DET', 'DETe', 'AJ', 'AJe', 'CL', 'INT', 'CONJ',
                         'CONJe', 'POSTP', 'PRO', 'PROe', 'NUM', 'NUMe', 'PUNC', 'Ne', 'Pe')

    def test_crf_api(self):
        self.assertRaises(Exception, downloader, path='wrong-path')

    def test_crf_normalized_verb_tagging(self):
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertNotEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_crf_tagger(self):
        self.assertIsInstance(self.tagger['رئيس‌جمهور'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0], tuple)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0][1], str)
        for item in self.tagger['ابراهیم رئیسی رئيس‌جمهور جمهوری اسلامی ایران میباشد']:
            self.assertIn(member=item[1], container=self.all_tags)

    def test_crf_ai(self):
        self.assertIn(self.tagger['رئيس‌جمهور'][0][1], 'Ne')


class WapitiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tagger = WapitiPosTagger(model_path="model/UPC_full_model_wapiti")
        self.all_tags = ('N', 'P', 'V', 'A', 'R', 'FW', 'C')

    def test_wapiti_normalizer(self):
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertNotEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_wapiti_tagger(self):
        self.assertIsInstance(self.tagger['رئيس جمهور'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0], tuple)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0][1], str)
        for item in self.tagger['ابراهیم رئیسی وقتی رئيس‌جمهور جمهوری اسلامی ایران میباشد مملکت ویران است']:
            print(item)
            # self.assertIn(member=item[1], container=self.all_tags)

    def test_wapiti_ai(self):
        self.assertIn(self.tagger['رئيس‌جمهور'][0][1], 'Ne')


if __name__ == '__main__':
    unittest.main()
