"""
Wapiti Classifier

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
        return self.parse([item])[0]

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
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
