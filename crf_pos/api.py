import requests


def downloader(path: str, save_path: str, mode: str):
    try:
        model_bin = requests.get(path, allow_redirects=True)
        with open(save_path, mode) as resource:
            resource.write(model_bin.content)
    except Exception:
        raise Exception('not a proper webpage')