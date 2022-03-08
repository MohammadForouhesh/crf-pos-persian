"""
Normalizer

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This Module contains the implementation and encapsulation for Text Normalizer, this functionality
helps with detecting
half-spaces.
"""

from re import sub
import os
from typing import Dict

from crf_pos.api import downloader
from crf_pos.normalization.tokenizer import clean_text


class Normalizer:
    """
    A native persian text normalizer to help detecting half-spaces.
    """
    def __init__(self, downloading: bool = False) -> None:
        self.dir_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)))) + "/"
        if downloading: self.get_resources()
        self.dic1 = self.load_dictionary(self.dir_path + 'model/normalizer/Dic1_new.txt')
        self.dic2 = self.load_dictionary(self.dir_path + 'model/normalizer/Dic2_new.txt')
        self.dic3 = self.load_dictionary(self.dir_path + 'model/normalizer/Dic3_new.txt')

    def get_resources(self) -> None:
        """
        A tool to download required resources over internet.
        :return:    None.
        """
        load_dir = 'https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer'
        save_dir = self.dir_path + '/model/normalizer/'
        os.makedirs(save_dir, exist_ok=True)
        for ind in range(1, 4):
            downloader(path=load_dir + f'/Dic{ind}_new.txt', save_path=save_dir + f'Dic{ind}_new.txt', mode='wb')

    @staticmethod
    def load_dictionary(file_path: str) -> Dict[str, str]:
        """
        A static method that read a file and return a keyed dictionary of the contents of the file.
        :param file_path:   The path (str) to the resource file.
        :return:            A dictionary of the contents of the file.
        """
        dictionary = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for words in lines:
                word = words.split(' ')
                dictionary[word[0].strip()] = sub('\n', '', word[1].strip())
        return dictionary

    @staticmethod
    def space_correction(text: str) -> str:
        """
        A tool to help with rule-based half space correction
        :param text:        The input text (str).
        :return:            The half-spaced corrected text (str).
        """
        text = sub(r'^(بی|می|نمی)( )', r'\1‌', text)
        text = sub(r'( )(می|نمی|بی)( )', r'\1\2‌', text)
        pattern = r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین' \
                  r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )' \
                  r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
                  r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
                  r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        text = sub(pattern, r'‌\2\3', text)
        return sub(r'( )(شده|نشده)( )', r'‌\2‌', text)

    def uni_window_correction(self, text: str) -> str:
        """
        A tool to help with rule-based half space correction using external resources.
        :param text:        The input text (str).
        :return:            The half-spaced corrected text (str).
        """
        ## refrence_dictionary
        for word in text.split(' '):
            if word in self.dic1:
                yield self.dic1[word]
            else:
                yield word

    def bi_window_correction(self, text: str) -> str:
        """
        A tool to help with rule-based half space correction using external resources.
        :param text:        The input text (str).
        :return:            The half-spaced corrected text (str).
        """
        out_sentences = ''
        words = text.split(' ')
        if len(words) < 2:
            return text
        cnt = 1
        for i in range(0, len(words) - 1):
            combination = words[i] + words[i + 1]
            if combination in self.dic2:
                out_sentences += ' ' + self.dic2[combination]
                cnt = 0
            else:
                if cnt == 1:    out_sentences += ' ' + words[i]
                cnt = 1
        if cnt == 1:            out_sentences += ' ' + words[-1]
        return out_sentences

    def tri_window_correction(self, text: str) -> str:
        """
        A tool to help with rule-based half space correction using external resources.
        :param text:        The input text (str).
        :return:            The half-spaced corrected text (str).
        """
        out_sentences = ''
        words = text.split(' ')
        if len(words) < 3:   return text
        cnt = 1
        cnt2 = 0
        for i in range(0, len(words) - 2):
            combination = words[i] + words[i + 1] + words[i + 2]
            try:
                out_sentences = out_sentences + ' ' + self.dic3[combination]
                cnt = 0
                cnt2 = 2
            except KeyError:
                if cnt == 1 and cnt2 == 0:  out_sentences += ' ' + words[i]
                else:                       cnt2 -= 1
                cnt = 1
        if cnt == 1 and cnt2 == 0:          out_sentences += ' ' + words[-2] + ' ' + words[-1]
        elif cnt == 1 and cnt2 == 1:        out_sentences += ' ' + words[-1]
        return out_sentences

    def normalize(self, text: str, new_line_elimination: bool = False) -> str:
        """
        Normalizer function, it is the main function in this class.
        :param text:        The input text.
        :param new_line_elimination: A boolean, controls whether to use another character for
                                     half-space.
        :return:            A normalized text.
        """
        cleansed_string = clean_text(text, new_line_elimination).strip()
        return self.space_correction(
            ' '.join(self.uni_window_correction(
                self.bi_window_correction(
                    self.tri_window_correction(cleansed_string))))).strip()
