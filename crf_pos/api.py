import requests


def downloader(path: str):
    try:
        model_bin = requests.get(path, allow_redirects=True)
        with open('model/perpos-v1.model', 'wb') as resource:
            resource.write(model_bin.content)
    except:
        raise Exception('not a proper webpage')