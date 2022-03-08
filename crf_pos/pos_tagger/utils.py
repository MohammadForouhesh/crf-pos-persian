"""
Utils

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module contains various tools and one-line functions for Part-of-Speech tagging.
"""
from typing import Generator, Dict, Any

import string
import re

token2features = lambda item: [word2features(item, ind) for ind in range(len(item))]
sent2labels = lambda item: [postag for token, postag in item]
sent2tokens = lambda item: [token for token, postag in item]
template = lambda word: "".join([(lambda item: "x" if not item in "آایو" else "a")(char)
                                 for char in word])
isdigit = lambda word: all(map(lambda char: char in "۱۲۳۴۵۶۷۸۹۰1234567890.", word))
is_all_latin = lambda item: bool(len(re.sub('[a-zA-Z]*', '', item)) == 0)
remove_after_underline = lambda item: item[:item.find('_')] if '_' in item else item


def ngram(text: str, length: int = 2) -> Generator[str, None, None]:
    """
    function for detecting n-grams.
    :param text:    Input text, it is in the form of a sentence and it is a string.
    :param length:  The length at which we want to extract n-grams.
    :return:        A Generator, it yields words pattern.
    """
    for i in range(len(text) - 1):
        yield 'word[' + str(i) + ":" + str(i + length) + "]", text[i:i + length]


def word2features(text: str, index: int) -> Dict[str, Any]:
    """
    A feature extraction tool that helps with extraction of different useful information
    within the given text.
    :param text:    The input text. A string.
    :param index:   The place of the word at which we want to move the window back and forth.
    :return:        A dictionary containing extracted features.
    """
    word = text[index]
    features = {
        'B': 1.0,
        'W': word,
        'P': word in string.punctuation,
        'T': template(word),
        'D(W)': isdigit(word),
    }
    for length in range(max(4 + 1, len(word)) + 1):
        for k, v in ngram(word, length=length):
            features[k] = v
    if index > 0:
        word = text[index - 1][0]
        features.update({
            '-1W[-3': word[-3:],
            '-1W[-2': word[-2:],
            '-1W[-1': word[-1:],
            '-1W': word,
            '-1W0W': word + text[index],
            '-1P': word in string.punctuation,
            '-1T': template(word)
        })
    else:
        features['BOS'] = True
    if index > 1:
        word = text[index - 2][0]
        features.update({
            '-2W[-3': word[-3:],
            '-2W[-2': word[-2:],
            '-2W[-1': word[-1:],
            '-2P': word in string.punctuation,
            '-2T': template(word)
        })

    if index < len(text) - 2:
        word = text[index + 2][0]
        features.update({
            '+2W[-1': word[-1:],
            '+2W[-2': word[-2:],
            '+2W': word,
            '+2P': word in string.punctuation,
            '+2T': template(word)
        })
    if index < len(text) - 1:
        word = text[index + 1][0]
        features.update({
            '+1W[-1': word[-1:],
            '+1W': word,
            '+1W0W': word + text[index],
            '+1W[-2': word[-2:],
            '+1:P': word in string.punctuation,
            '+1:T': template(word)
        })
    else:
        features['EOS'] = True
    if 0 < index < len(text) - 1:   features['-1W/+1W'] = text[index + 1][0] + "/" + text[index - 1][0]
    return features
