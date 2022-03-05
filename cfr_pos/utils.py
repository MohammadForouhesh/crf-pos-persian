from nltk import tree2conlltags
import string


token2features = lambda item: [word2features(item, ind) for ind in range(len(item))]
sent2labels = lambda item: [postag for token, postag in item]
sent2tokens = lambda item: [token for token, postag in item]
template = lambda word: "".join([(lambda item: "x" if not item in "آایو" else "a")(char) for char in word])
isdigit = lambda word: all(map(lambda char: char in "۱۲۳۴۵۶۷۸۹۰1234567890.", word))


def ngram(word, length=2):
    for i in range(len(word) - 1):
        yield 'word[' + str(i) + ":" + str(i + length) + "]", word[i:i + length]


def read_conll(path, col=2):
    with open(path, "r", encoding="utf-8") as conll:
        out = []
        for sent in conll.readlines():
            split = sent.strip("\r\n").split()
            if len(split) > 1:
                none_token_count = col - 1
                new_elem = split[-1:]
                new_elem = split[:none_token_count] + new_elem
                out.append(new_elem)

            else:
                yield out
                out = []


def tree2brackets(tree):
    str, tag = '', ''
    for item in tree2conlltags(tree):
        if item[2][0] in {'B', 'O'} and tag:
            str += tag + '] '
            tag = ''

        if item[2][0] == 'B':
            tag = item[2].split('-')[1]
            str += '['
        str += item[0] + ' '

    if tag:
        str += tag + '] '

    return str.strip()


def word2features(sent, i):
    W = sent[i]
    features = {
        'B': 1.0,
        'W': W,
        'P': W in string.punctuation,
        'T': template(W),
        'D(W)': isdigit(W),
    }
    for length in range(max(4 + 1, len(W)) + 1):
        for k, v in ngram(W, length=length):
            features[k] = v
    if i > 0:
        W = sent[i - 1][0]
        features.update({
            '-1W[-3': W[-3:],
            '-1W[-2': W[-2:],
            '-1W[-1': W[-1:],
            '-1W': W,
            '-1W0W': W + sent[i],
            '-1P': W in string.punctuation,
            '-1T': template(W)
        })
    else:
        features['BOS'] = True
    if i > 1:
        W = sent[i - 2][0]
        features.update({
            '-2W[-3': W[-3:],
            '-2W[-2': W[-2:],
            '-2W[-1': W[-1:],
            '-2P': W in string.punctuation,
            '-2T': template(W)
        })

    if i < len(sent) - 2:
        W = sent[i + 2][0]
        features.update({
            '+2W[-1': W[-1:],
            '+2W[-2': W[-2:],
            '+2W': W,
            '+2P': W in string.punctuation,
            '+2T': template(W)
        })
    if i < len(sent) - 1:
        W = sent[i + 1][0]
        features.update({
            '+1W[-1': W[-1:],
            '+1W': W,
            '+1W0W': W + sent[i],
            '+1W[-2': W[-2:],
            '+1:P': W in string.punctuation,
            '+1:T': template(W)
        })
    else:
        features['EOS'] = True
    if 0 < i < len(sent) - 1:   features['-1W/+1W'] = sent[i + 1][0] + "/" + sent[i - 1][0]
    return features
