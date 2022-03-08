"""
API

....................................................................................................
MIT License

Copyright (c) 2021-2023 AUT Iran, Mohammad H Forouhesh
Copyright (c) 2021-2022 MetoData.ai, Mohammad H Forouhesh
....................................................................................................
This module contains tools to download resources over http connections.
supported http links are:
    - https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v2.0.0.alpha/UPC_full_model_wapiti
    - https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v2.0.0.alpha/perpos.model
    - https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer/model/normalizer/Dic1_new.txt
    - https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer/model/normalizer/Dic2_new.txt
    - https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer/model/normalizer/Dic3_new.txt
"""

import os
from typing import Union

import requests


def downloader(path: str, save_path: str, mode: str) -> Union[int, None]:
    """
    A tool to download and save files over https.
    supported http links are:
    - https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v2.0.0.alpha/UPC_full_model_wapiti
    - https://github.com/MohammadForouhesh/crf-pos-persian/releases/download/v2.0.0.alpha/perpos.model
    - https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer/model/normalizer/Dic1_new.txt
    - https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer/model/normalizer/Dic2_new.txt
    - https://raw.githubusercontent.com/MohammadForouhesh/Parsivar/master/parsivar/resource/normalizer/model/normalizer/Dic3_new.txt

    :param path:        The path to the desired file.
    :param save_path:   The intended storage path.
    :param mode:        The mode that it should be stored.
    :return:            If the file exists, it returns 0 (int), otherwise nothing would be returned.
    """
    if os.path.isfile(save_path): return 0
    try:
        model_bin = requests.get(path, allow_redirects=True)
        with open(save_path, mode) as resource:
            resource.write(model_bin.content)
    except Exception:
        raise Exception('not a proper webpage')
