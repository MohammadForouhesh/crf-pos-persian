from typing import Union, List, Any, Tuple
import parsivar

norm = parsivar.Normalizer()
tokenizer = parsivar.Tokenizer()


class MetaTagger:
    def __init__(self) -> None:
        self.tagger = None

    def __getitem__(self, item: Union[list, str]) -> List[Tuple[str, str]]:
        if isinstance(item, str):   item = tokenizer.tokenize_words(norm.normalize(item))
        return self.parse([item])[0]

    def parse(self, token_list: List[str]) -> List[List[Tuple[Any, Any]]]:
        pass

    @staticmethod
    def zip_vector(iterable: zip):
        for key, item in iterable:
            yield list(zip(key, item))