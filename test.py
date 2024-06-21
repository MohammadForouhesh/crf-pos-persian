"""
Test Suite

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module serves as unit testing for various functionalities in the code.
"""

import unittest
import requests
import json
from crf_pos.pos_tagger.crf import CrfPosTagger
from crf_pos.api import downloader
from crf_pos.pos_tagger.wapiti import WapitiPosTagger
from crf_pos.normalization.normalizer import Normalizer


class NormalizerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.normalizer = Normalizer(downloading=True)

    def test_normalize(self) -> None:
        self.assertEqual(self.normalizer.normalize('می باشد'), self.normalizer.normalize('می‌باشد'))
        self.assertEqual(self.normalizer.normalize('می باشد'), self.normalizer.normalize('میباشد'))
        self.assertEqual(self.normalizer.normalize('تامینکنندگان'), self.normalizer.normalize('تامین کنندگان'))

    def test_moving_mavericks(self) -> None:
        self.assertEqual(self.normalizer.collapse_mavericks('رئيس جمهور ایران میباشد'),
                         self.normalizer.collapse_mavericks('رئيس‌جمهور ایران می باشد'))
        self.assertEqual(self.normalizer.collapse_mavericks('بی طرفانه'),
                         self.normalizer.collapse_mavericks('بیطرفانه'))


class CrfTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tagger = CrfPosTagger()
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADVe', 'RES', 'RESe', 'DET', 'DETe', 'AJ', 'AJe',
                         'CL', 'INT', 'CONJ', 'CONJe', 'POSTP', 'PRO', 'PROe', 'NUM', 'NUMe',
                         'PUNC', 'Ne', 'Pe')

    def test_crf_api(self) -> None:
        self.assertRaises(Exception, downloader, path='wrong-path')

    def test_crf_normalized_verb_tagging(self) -> None:
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_crf_tagger(self) -> None:
        self.assertIsInstance(self.tagger['رئيس‌جمهور'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0], tuple)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0][1], str)
        for item in self.tagger['ابراهیم رئیسی رئيس جمهور جمهوری اسلامی ایران میباشد']:
            self.assertIn(member=item[1], container=self.all_tags)

    def test_crf_ai(self) -> None:
        self.assertIn(self.tagger['رئيس‌جمهور'][0][1], 'Ne')
       
    def test_crf_soundness(self) -> None:
        text = 'ابراهیم رئیسی رئيس جمهور جمهوری اسلامی ایران میباشد'
        self.assertEqual(self.tagger[text], self.tagger[text.split()])


class WapitiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tagger = WapitiPosTagger()
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADJ', 'PRO', 'CON')

    def test_wapiti_normalizer(self) -> None:
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertEqual(self.tagger['می گویم'], self.tagger['می‌گویم'])
        self.assertEqual(self.tagger['می باشد'], self.tagger['می‌باشد'])
        self.assertEqual(self.tagger['نهاد ریاست جمهوری'], self.tagger['نهاد ریاست‌جمهوری'])

    def test_wapiti_tagger(self) -> None:
        self.assertIsInstance(self.tagger['رئيس جمهور'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'], list)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0], tuple)
        self.assertIsInstance(self.tagger['رئيس‌جمهور جمهوری اسلامی'][0][1], str)
        for item in self.tagger['او وقتی رئيس جمهور جمهوری اسلامی ایران میباشد مملکت معمولا ویران است']:
            self.assertIn(member=item[1], container=self.all_tags)

    def test_wapiti_ai(self) -> None:
        self.assertIn(self.tagger['رئيس‌جمهور'][0][1], 'Ne')
       
    def test_wapiti_soundness(self) -> None:
        text = 'ابراهیم رئیسی رئيس جمهور جمهوری اسلامی ایران میباشد'
        self.assertEqual(self.tagger[text], self.tagger[text.split()])


class FlaskTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "localhost:5000/infering"
        self.headers = {'Content-Type': 'application/json'}
        self.all_tags = ('N', 'P', 'V', 'ADV', 'ADJ', 'PRO', 'CON')

    def test_flask_api(self) -> None:
        payload = json.dumps({
            "stdin": "ابراهیم رئیسی رئيس جمهور جمهوری اسلامی ایران میباشد"
            })
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        for item in response.text:
            self.assertIn(member=item[1], container=self.all_tags)


if __name__ == '__main__':
    unittest.main()
