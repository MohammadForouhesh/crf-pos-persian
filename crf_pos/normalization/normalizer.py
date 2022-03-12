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

import os
from re import sub
from typing import Dict, List, Generator
from crf_pos.api import get_resources
from crf_pos.normalization.tokenizer import clean_text


class Normalizer:
    """
    A native persian text normalizer to help detecting half-spaces.
    """
    def __init__(self, downloading: bool = True) -> None:
        dir_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)))) + "/"
        if downloading: get_resources(dir_path, resource_name='corrections.txt')
        self.corrections = self.load_dictionary(dir_path + 'resources/corrections.txt')

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
        """
        Sample a sentence by moving a window of length `window_length` over it. e.g.
        >>> list(Normalizer.window_sampling(tokens=['Hi', 'Hello', 'Hallo'], window_length=2))
        ['Hi Hello', 'Hello Hallo']

        :param tokens:          A list of tokens i.e. words
        :param window_length:   An integer, the length of the sampling.
        :return:                A list of concatenated tokens.
        """

        if len(tokens) < window_length: yield ' '.join(tokens)
        while True:
            try:                yield ' '.join([tokens.pop(0)] + [tokens[_] for _ in range(window_length - 1)])
            except IndexError:  break

    def vector_mavericks(self, text: str, window_length: int) -> Generator[str, None, None]:
        """
        A generative recursive function that substitute a concatenated string of length `window_length` with its
        half-space correction.
        :param text:            The input text (str).
        :param window_length:   The order (scope) of correction, considers the n-grams for correcting.
        :return:                A list of tokens that are half-space corrected upto order `window_length`
        """
        iter_sample = iter(self.window_sampling(text.replace('\u200c', ' ').split(), window_length))
        for word in iter_sample:
            try:
                yield self.corrections[word.replace(' ', '')]
                for ind in range(0, window_length - 1):   next(iter_sample, None)
            except:
                try:    yield self.corrections[word.split()[0]]
                except: yield word.split()[0]

    def moving_mavericks(self, text: str, scope: int = 4) -> Generator[str, None, None]:
        """
        Cascading the generation of half-space correction for a variety of different scopes (n-grams).
        :param text:    An input text.
        :param scope:   The maximum length of which we are interested to study.
        :return:        A generator of generators
        """
        yield self.vector_mavericks(text, scope)
        if scope > 1: yield from self.moving_mavericks(text, scope - 1)

    def collapse_mavericks(self, text: str) -> str:
        """
        Choosing the best output among all of the corrections.
        :param text:    Input text (str)
        :return:        half-space corrected text. (str)
        """
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
