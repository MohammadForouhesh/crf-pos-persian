"""
Wapiti Classifier

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module contains the implementation and encapsulation for Wapiti classifier.
"""

from typing import List, Any, Tuple
from wapiti import Model

from crf_pos.api import get_resources
from crf_pos.pos_tagger.meta_tagger import MetaTagger
from crf_pos.pos_tagger.utils import remove_after_underline


class WapitiPosTagger(MetaTagger):
    """
    Wapiti Part-of-Speech tagger encapsulation.
    """
    def __init__(self) -> None:
        super().__init__()
        model_path = get_resources(self.dir_path, resource_name='UPC_full_model_wapiti')
        self.tagger = Model(model=model_path)

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        """
        Primary function that overwrite the same method from the super class. This function is
        responsible for the logic behind the model.
        :param token_list:  A list of tokens (strings)
        :return:            A list of list of extracted part of speeches and their related tokens.
        """
        sent_line = "\n".join(token_list[0])
        postags = self.tagger.label_sequence(sent_line).decode('utf-8').strip().split('\n')
        return list(super().zip_vector(zip(token_list, [list(map(remove_after_underline, postags))])))
