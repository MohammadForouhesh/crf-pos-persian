from pos.utils import token2features
import pickle


class POSTagger:
    def __init__(self, model_path):
        self.model_path = model_path
        self.crf = pickle.load(open(model_path, "rb"))

    def __getitem__(self, item):
        return self.parse_sentences([item])[0]

    def parse_sentences(self, token_stream: list):
        y_pred = self.crf.predict([token2features(token) for token in token_stream])
        out = []
        for x_sent, y_pred in zip(token_stream, y_pred):
            out.append(list(zip(x_sent, y_pred)))
        return out