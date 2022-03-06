from typing import Union

from wapiti import Model
import parsivar
from crf_pos.utils import is_all_latin

norm = parsivar.Normalizer(statistical_space_correction=True, date_normalizing_needed=True)
tokenizer = parsivar.Tokenizer()


class WapitiPosTagger():
    def __init__(self, model_path: str = 'model/') -> None:
        self.model_path = model_path
        self.wapiti = Model(model=self.model_path)

    def __getitem__(self, item: Union[list, str]):
        if isinstance(item, str):   item = tokenizer.tokenize_words(norm.normalize(item))
        return self.parse([item])[0]

    def parse(self, token_list):
        tagged_tuples = []

        sent_line = "\n".join(x for x in token_list)
        postags = self.wapiti.label_sequence(sent_line).decode('utf-8')
        postags = postags.strip().split('\n')
        for i, el in enumerate(token_list):
            if is_all_latin(el):
                tagged_tuples.append((el, u"FW"))
            else:
                tagged_tuples.append((el, postags[i]))
        return tagged_tuples