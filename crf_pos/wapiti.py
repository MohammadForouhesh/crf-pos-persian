from typing import Union, List, Any, Tuple, Generator
from wapiti import Model
import parsivar


norm = parsivar.Normalizer()
tokenizer = parsivar.Tokenizer()


class WapitiPosTagger():
    def __init__(self, model_path: str = 'model/UPC_full_model_wapiti') -> None:
        self.model_path = model_path
        self.wapiti = Model(model=self.model_path)

    def __getitem__(self, item: Union[list, str]) -> List[Tuple[str, str]]:
        if isinstance(item, str):   item = tokenizer.tokenize_words(norm.normalize(item))
        return self.parse([item])[0]

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        sent_line = "\n".join(token_list[0])
        postags = self.wapiti.label_sequence(sent_line).decode('utf-8').strip().split('\n')
        return list(WapitiPosTagger.zip_vector(zip(token_list, [list(map(lambda item: item, postags))])))

    @staticmethod
    def zip_vector(iterable: zip) -> Generator[List[Tuple[str, str]]]:
        for key, item in iterable:
            yield list(zip(key, item))
