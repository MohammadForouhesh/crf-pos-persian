"""
Run the Application

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module serves as unit testing for various functionalities in the code.
"""

from crf_pos.pos_tagger.meta_tagger import MetaTagger
from crf_pos.pos_tagger.wapiti import WapitiPosTagger


def main():
    tagger: MetaTagger = WapitiPosTagger()
    stdin: str = input('A sentence to tag its parts-of-speech: [Press Q to exit]\n>>>')
    if stdin.lower() == 'q':
        raise Exception('Quit')
    return tagger[stdin]


if __name__ == '__main__':
    while True:
        try:    print(main())
        except: break
