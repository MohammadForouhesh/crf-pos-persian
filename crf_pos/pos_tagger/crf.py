from typing import List, Tuple, Any
from crf_pos.pos_tagger.meta_tagger import MetaTagger
from crf_pos.pos_tagger.utils import token2features
import pickle


class CrfPosTagger(MetaTagger):
    def __init__(self, model_path) -> None:
        super().__init__()
        with open(model_path, 'rb') as resource:
            self.tagger = pickle.load(resource)

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        y_pred = self.tagger.predict([token2features(token) for token in token_list])
        return list(super().zip_vector(zip(token_list, y_pred)))
