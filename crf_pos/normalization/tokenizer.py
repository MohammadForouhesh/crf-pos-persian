"""
Tokenizer

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This Module contains the tools and one-line functions used in tokenization process.
"""

import re
import string
from typing import List


tokenize_words = lambda text: [item.strip("\u200c") for item in text.strip().split()
                               if len(item.strip("\u200c")) != 0]
add_tab = lambda text: str(" " + text.group().strip(' ').strip('\n') + "\t\t")
triplets2tagged_pairs = lambda iob_sent: [((word, pos), chunk) for word, pos, chunk in iob_sent]
add_space = lambda text: str(" " + text.group().strip(' ') + " ")


def tokenize_sentences(text: str) -> List[str]:
    """
    A sentencizer function, split text into sentence.
    :param text:    A text.
    :return:        Splatted sentences in the format of list of strings.
    """
    text = pattern_matching(text)
    nums_list = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    for number in nums_list:
        pattern = 'floatingpointnumber'
        text = re.sub(pattern, number, text, 1)

    return [item for item in text.split('\t\t') if len(item) != 0]


def pattern_matching(text: str) -> str:
    """
    A regex based pattern matching function to remove the unwanted characters in the text.
    :param text:    The input text (str).
    :return:        A text without the patterns.
    """
    patterns = re.compile(pattern="["
                                  r"[-+]?\d*\.\d+|\d+"
                                  r"([!\.\?؟]+)[\n]*"
                                  r":\n"
                                  r";\n"
                                  r'؛\n'
                                  r'[\n]+'
                                  "]+", flags=re.UNICODE)
    return str(patterns.sub(r'', text))


def clean_text(text_doc: str, new_line_elimination: bool) -> str:
    """
    A preprocessing function to delete the punctuations.
    :param text_doc:    The input text.
    :param new_line_elimination: A boolean that controls the usage of half-space
    :return:            Removed punctuation text.
    """
    punctuations = r')(}{:؟!،؛»«.' + r"/<>?.,:;"
    punctuations = '[' + punctuations + string.punctuation + ']'
    punctuations = punctuations.replace("@", "")

    text_doc.strip()

    pattern = r"[-+]?\d*\.\d+|\d+"
    nums_list = re.findall(pattern, text_doc)
    new_string = re.sub(pattern, 'floatingpointnumber', text_doc)

    pattern = r'\s*' + punctuations + '+' + r'\s*'
    new_string = re.sub(pattern, add_space, new_string)

    pattern = r'[\n]+'
    if new_line_elimination:  new_string = re.sub(pattern, " ", new_string)

    pattern = r'[^' + r")(}{:؟!-،؛»«.@$&%" + r"/<>?.,:;" + r"a-zA-Z0-9" + 'آ-ی' + '‌' + '\d\s:]'
    new_string = re.sub(pattern, '', new_string)

    pattern = r'[ ]+'
    new_string = re.sub(pattern, ' ', new_string)

    for number in nums_list:
        pattern = 'floatingpointnumber'
        new_string = re.sub(pattern, number, new_string, 1)
    return new_string
