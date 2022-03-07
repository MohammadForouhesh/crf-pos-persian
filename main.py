import unittest
import os
from crf_pos.pos_tagger.crf import CrfPosTagger
from crf_pos.api import downloader
from crf_pos.pos_tagger.wapiti import WapitiPosTagger
from crf_pos.normalization.normalizer import Normalizer


class NormalizerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        load_dir = 'https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer'
        save_dir = 'model/normalizer/'
        os.makedirs(save_dir, exist_ok=True)
        for ind in range(1, 4):
            downloader(path=load_dir + f'/Dic{ind}_new.txt', save_path=save_dir + f'Dic{ind}_new.txt', mode='wb')
        self.normalizer = Normalizer()

    def test_normalize(self) -> None:
        self.assertEqual(self.normalizer.normalize('می باشد'), self.normalizer.normalize('می‌باشد'))


class CrfTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model_path = 'https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v1/perpos.model'
        self.tagger = CrfPosTagger("model/perpos-v1.model")
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADVe', 'RES', 'RESe', 'DET', 'DETe', 'AJ', 'AJe', 'CL', 'INT', 'CONJ',
                         'CONJe', 'POSTP', 'PRO', 'PROe', 'NUM', 'NUMe', 'PUNC', 'Ne', 'Pe')

    def test_crf_api(self) -> None:
        self.assertRaises(Exception, downloader, path='wrong-path')

    def test_crf_normalized_verb_tagging(self) -> None:
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertNotEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_crf_tagger(self) -> None:
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
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADJ', 'PRO', 'CON')

    def test_wapiti_normalizer(self) -> None:
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertNotEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_wapiti_tagger(self) -> None:
        self.assertIsInstance(self.tagger['رئيس جمهور'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0], tuple)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0][1], str)
        for item in self.tagger['او وقتی رئيس‌جمهور جمهوری اسلامی ایران میباشد مملکت معمولا ویران است']:
            self.assertIn(member=item[1], container=self.all_tags)

    def test_wapiti_ai(self) -> None:
        self.assertIn(self.tagger['رئيس‌جمهور'][0][1], 'Ne')


if __name__ == '__main__':
    unittest.main()
