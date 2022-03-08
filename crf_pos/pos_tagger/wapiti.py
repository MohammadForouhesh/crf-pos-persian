"""
Wapiti Classifier

..................................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
..................................................................................................................
This module contains the implementation and encapsulation for Wapiti classifier.
"""

from typing import List, Any, Tuple
from wapiti import Model
from crf_pos.pos_tagger.meta_tagger import MetaTagger
from crf_pos.pos_tagger.utils import remove_after_underline


class WapitiPosTagger(MetaTagger):
    def __init__(self, model_path: str = 'model/UPC_full_model_wapiti') -> None:
        super().__init__()
        self.tagger = Model(model=model_path)

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        sent_line = "\n".join(token_list[0])
        postags = self.tagger.label_sequence(sent_line).decode('utf-8').strip().split('\n')
        return list(super().zip_vector(zip(token_list, [list(map(remove_after_underline, postags))])))
