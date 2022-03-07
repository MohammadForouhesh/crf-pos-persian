import os
import requests


def downloader(path: str, save_path: str, mode: str):
    if os.path.isfile(save_path): return 0
    try:
        model_bin = requests.get(path, allow_redirects=True)
        with open(save_path, mode) as resource:
            resource.write(model_bin.content)
    except Exception:
        raise Exception('not a proper webpage')
