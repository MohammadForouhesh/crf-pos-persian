import re
from typing import List, Tuple
import nltk
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import ChunkParserI, ClassifierBasedTagger


tokenize_words = lambda text: [item.strip("\u200c") for item in text.strip().split() if len(item.strip("\u200c")) != 0]
add_tab = lambda text: str(" " + text.group().strip(' ').strip('\n') + "\t\t")
triplets2tagged_pairs = lambda iob_sent: [((word, pos), chunk) for word, pos, chunk in iob_sent]


def tokenize_sentences(text: str) -> List[str]:
    text = pattern_matching(text)

    nums_list = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    for number in nums_list:
        pattern = 'floatingpointnumber'
        text = re.sub(pattern, number, text, 1)

    return [item for item in text.split('\t\t') if len(item) != 0]


def pattern_matching(text: str) -> str:
    patterns = re.compile(pattern="["
                                  r"[-+]?\d*\.\d+|\d+"
                                  r"([!\.\?؟]+)[\n]*"
                                  r":\n"
                                  r";\n"
                                  r'؛\n'
                                  r'[\n]+'
                                  "]+", flags=re.UNICODE)
    return str(patterns.sub(r'', text))


class ClassifierChunkParser(ChunkParserI):
    def __init__(self):
        self.tagger = None
        pass

    def parse(self, tagged_sent):
        chunks = self.tagger.tag(tagged_sent)
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]
        return conlltags2tree(iob_triplets)

    def train_merger(self, train_file_path):
        print("Loading Data...")
        file = open(train_file_path, "r", encoding='utf-8')
        file_content = file.read()
        file_content = file_content.split("\n\n")

        data_list = []
        for line in file_content:
            line = nltk.chunk.util.conllstr2tree(line, chunk_types=('NP',), root_label='S')
            if (len(line) > 0):
                data_list.append(line)

        train_sents = data_list
        test_sents = []

        print("Training the model ...")
        chunked_sents = [tree2conlltags(sent) for sent in train_sents]

        chunked_sents = [triplets2tagged_pairs(sent) for sent in chunked_sents]

        self.feature_detector = self.features
        self.tagger = ClassifierBasedTagger(
            train=chunked_sents,
            feature_detector=self.features)

        token_merger_model = self.tagger

        if len(test_sents) > 0:
            print("evaluating...")
            print(token_merger_model.evaluate(test_sents))

        return token_merger_model

    def nestedtree_to_list(self, tree, separator_char, d=0):
        s = ''
        for item in tree:
            if isinstance(item, tuple):
                s += item[0] + separator_char
            elif d >= 1:
                news = self.nestedtree_to_list(item, separator_char, d + 1)
                s += news + separator_char
            else:
                news = self.nestedtree_to_list(item, separator_char, d + 1) + '\t'
                s += news + separator_char
        return s.strip(separator_char)

    def merg_tokens(self, token_list, token_merger_model, separator_char):
        # gets a string line as input and returns a list of tokens
        tmp_list = []
        for word in token_list:
            tmp_list.append((word, 'N'))

        self.tagger = token_merger_model

        res = self.parse(tmp_list)
        res = self.nestedtree_to_list(res, separator_char=separator_char)
        res = res.strip('\t').split('\t')
        res = [x.strip(separator_char).strip() for x in res]
        return res

    def features(self, tokens: List[Tuple[str, str]], index: int, history):
        tokens = [('__START2__', '__START2__'), ('__START1__', '__START1__')] + list(tokens) + [
            ('__END1__', '__END1__'),
            ('__END2__', '__END2__')]
        history = ['__START3__', '__START2__', '__START1__'] + list(history)

        index += 2

        word, pos = tokens[index]
        prevword, prevpos = tokens[index - 1]
        nextword, nextpos = tokens[index + 1]
        previob = history[index - 1].split("-")[0]

        return {
            'word': word,

            'prev-iob': previob,

            'next-word': nextword,

            'prev-word': prevword,
        }