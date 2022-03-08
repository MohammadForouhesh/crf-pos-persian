from typing import Union, List, Any, Tuple, Generator
from crf_pos.normalization.normalizer import Normalizer
"""
Wapiti Classifier

..................................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
..................................................................................................................
This module sole purpose is abstraction, it contains a meta class for Wapiti and CRF classifier.
"""

from crf_pos.normalization.tokenizer import tokenize_words


class MetaTagger:
    def __init__(self) -> None:
        self.tagger = None
        self.norm = Normalizer(downloading=True)

    def __getitem__(self, item: Union[list, str]) -> List[Tuple[str, str]]:
        if isinstance(item, str):   item = tokenize_words(self.norm.normalize(item))
        return self.parse([item])[0]

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        pass

    @staticmethod
    def zip_vector(iterable: zip) -> Generator[List[zip], None, None]:
        for key, item in iterable:
            yield list(zip(key, item))