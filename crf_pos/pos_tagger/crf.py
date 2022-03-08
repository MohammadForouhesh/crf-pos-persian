"""
CRF Classifier

..................................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
..................................................................................................................
This Module contains the implementation and encapsulation for Conditional Random Field classifier.
"""

from typing import List, Tuple, Any
from crf_pos.pos_tagger.meta_tagger import MetaTagger
from crf_pos.pos_tagger.utils import token2features
import pickle


class CrfPosTagger(MetaTagger):
    """
    Wapiti Part-of-Speech tagger encapsulation.
    """
    def __init__(self, model_path) -> None:
        super().__init__()
        with open(model_path, 'rb') as resource:
            self.tagger = pickle.load(resource)

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        """
        Primary function that override the same method from the super class. This function is responsible for the logic
        behind the model.
        :param token_list:  A list of tokens (strings)
        :return:            A list of extracted part of speeches and their related tokens.
        """
        y_pred = self.tagger.predict([token2features(token) for token in token_list])
        return list(super().zip_vector(zip(token_list, y_pred)))
