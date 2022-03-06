from typing import Union
import parsivar
from crf_pos.utils import token2features
import pickle

norm = parsivar.Normalizer() #statistical_space_correction=True, date_normalizing_needed=True)
tokenizer = parsivar.Tokenizer()


class CrfPosTagger:
    def __init__(self, model_path) -> None:
        self.model_path = model_path
        with open(model_path, 'rb') as resource:
            self.crf = pickle.load(resource)

    def __getitem__(self, item: Union[list[str], str]):
        if isinstance(item, str):   item = tokenizer.tokenize_words(norm.normalize(item))
        return self.parse([item])[0]

    def parse(self, token_stream: list):
        y_pred = self.crf.predict([token2features(token) for token in token_stream])
        return list(CrfPosTagger.zip_vector(zip(token_stream, y_pred)))

    @staticmethod
    def zip_vector(iterable: zip):
        for key, item in iterable:
            yield list(zip(key, item))
