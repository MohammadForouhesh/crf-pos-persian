"""
Meta Class for Classifiers

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module sole purpose is abstraction, it contains a meta class for Wapiti and CRF classifier.
"""

import os
from typing import Union, List, Any, Tuple, Generator
from crf_pos.normalization.normalizer import Normalizer


class MetaTagger:
    """
    Part-of-Speech taggers meta class abstraction.
    """
    def __init__(self) -> None:
        self.dir_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)))) + "/"
        self.tagger = None
        self.norm = Normalizer(downloading=True)

    def __getitem__(self, item: Union[list, str]) -> List[Tuple[str, str]]:
        """
        Generic getitem, used across the children objects.
        :param item:    An input text/list, the preferred input type is string.
        :return:        A List of tuples including a word and its part of speech.
        """
        if isinstance(item, str):   item = self.norm.normalize(item).split()
        else:                       item = self.norm.normalize(' '.join(item)).split()
        # return MetaTagger.pos_process(self.parse([item])[0])
        return self.parse([item])[0]
        
    def parse(self, token_list: List[List[str]]) -> List[List[Tuple[Any, Any]]]:
        """
        An abstract method, to be overwritten by its descendants.
        :param token_list:  A list of tokens (strings)
        :return:            A list of list of extracted part of speeches and their related tokens.
        """
        pass

    @staticmethod
    def zip_vector(iterable: zip) -> Generator[List[zip], None, None]:
        """
        A function that combine to iterables elements together.
        :param iterable:    A zip that contains the zipped format of two iterables.
        :return:            A Generator containing a list of tuples that consist of elements of
                            each iterable.
        """
        for key, item in iterable:
            yield list(zip(key, item))

    @staticmethod
    def extract_pos_words(pos_tagged: List[Tuple[str, str]], role: str) -> Generator[str, None, None]:
        for item in pos_tagged:
            if item[1] == role: yield item[0]

    @staticmethod
    def find_pos_index(pos_tagged: List[Tuple[str, str]], role: str) -> Generator[int, None, None]:
        pos_tags = [item[1] for item in pos_tagged]
        for ind, tag in enumerate(pos_tags):
            if tag == role: yield ind

    @staticmethod
    def find_pos_word(pos_tagged: List[Tuple[str, str]], role: str, index: int) -> str:
        try:    return list(MetaTagger.extract_pos_words(pos_tagged, role))[index]
        except: return ''

    @staticmethod
    def pos_process(pos_tagged: List[Tuple[Any, Any]]):
        verbs_index: Generator[int] = MetaTagger.find_pos_index(pos_tagged, 'V')
        for ind in verbs_index:
            if pos_tagged[ind - 1][1] == 'N':   pos_tagged[ind - 1] = (pos_tagged[ind - 1][0], 'V')
            if pos_tagged[ind - 1][1] == 'ADJ': pos_tagged[ind - 1] = (pos_tagged[ind - 1][0], 'V')
        return pos_tagged
