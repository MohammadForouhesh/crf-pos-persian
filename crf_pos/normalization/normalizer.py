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
import itertools
from re import sub
import os
from typing import Dict, List, Generator

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
        self.corrections = self.load_dictionary(self.dir_path + 'model/normalizer/corrections.txt')

    def get_resources(self) -> None:
        """
        A tool to download required resources over internet.
        :return:    None.
        """
        load_dir = 'https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v2.0.0.alpha/corrections.txt'
        save_dir = self.dir_path + '/model/normalizer/'
        os.makedirs(save_dir, exist_ok=True)
        downloader(path=load_dir, save_path=save_dir + 'corrections.txt', mode='wb')

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
                word = words.replace('\ufeff', '').split(' ')
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

    @staticmethod
    def window_sampling(tokens: List[str], window_length: int) -> Generator[str, None, None]:
        if len(tokens) < window_length: yield ' '.join(tokens)
        while True:
            try:                yield ' '.join([tokens.pop(0)] + [tokens[_] for _ in range(window_length - 1)])
            except IndexError:  break

    def vector_mavericks(self, text: str, window_length: int) -> Generator[str, None, None]:
        iter_sample = iter(self.window_sampling(text.replace('\u200c', ' ').split(), window_length))
        for word in iter_sample:
            try:
                yield self.corrections[word.replace(' ', '')]
                for ind in range(0, window_length - 1):   next(iter_sample, None)
            except:
                try:    yield self.corrections[word.split()[0]]
                except: yield word.split()[0]

    def moving_mavericks(self, text: str, scope: int = 4) -> Generator[str, None, None]:
        yield self.vector_mavericks(text, scope)
        if scope > 1: yield from self.moving_mavericks(text, scope - 1)

    def collapse_mavericks(self, text: str) -> str:
        mavericks_cascades = list(map(lambda item: ' '.join(item), self.moving_mavericks(text)))
        return sorted(mavericks_cascades, key=lambda item: item.count('\u200c'))[-1]

    def normalize(self, text: str, new_line_elimination: bool = False) -> str:
        """
        Normalizer function, it is the main function in this class.
        :param text:        The input text.
        :param new_line_elimination: A boolean, controls whether to use another character for
                                     half-space.
        :return:            A normalized text.
        """
        cleansed_string = clean_text(text, new_line_elimination).strip()
        return self.space_correction(self.collapse_mavericks(cleansed_string)).strip()
