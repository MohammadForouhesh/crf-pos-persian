import requests


def downloader(path: str, save_path: str = 'model/perpos-v1.model', mode: str = 'wb'):
    try:
        model_bin = requests.get(path, allow_redirects=True)
        with open(save_path, mode) as resource:
            resource.write(model_bin.content)
    except Exception as e:
        raise Exception('not a proper webpage')