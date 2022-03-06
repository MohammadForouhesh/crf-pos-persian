from typing import Union
import parsivar
from crf_pos.utils import token2features
import pickle

norm = parsivar.Normalizer(statistical_space_correction=True, date_normalizing_needed=True)
tokenizer = parsivar.Tokenizer()


class CrfPosTagger:
    def __init__(self, model_path):
        self.model_path = model_path
        with open(model_path, 'rb') as resource:
            self.crf = pickle.load(resource)

    def __getitem__(self, item: Union[list, str]):
        if isinstance(item, str):   item = tokenizer.tokenize_words(norm.normalize(item))
        return self.parse_sentences([item])[0]

    def parse_sentences(self, token_stream: list):
        y_pred = self.crf.predict([token2features(token) for token in token_stream])
        out = []
        for x_sent, y_pred in zip(token_stream, y_pred):
            out.append(list(zip(x_sent, y_pred)))
        return out