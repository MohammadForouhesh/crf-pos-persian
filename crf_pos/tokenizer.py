import re
from typing import List


tokenize_words = lambda text: [item.strip("\u200c") for item in text.strip().split() if len(item.strip("\u200c")) != 0]
add_tab = lambda text: str(" " + text.group().strip(' ').strip('\n') + "\t\t")


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
