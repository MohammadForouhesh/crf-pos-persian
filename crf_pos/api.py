import requests


def downloader(path: str):
    try:
        r = requests.get(path, allow_redirects=True)
        open('model/perpos-v1.model', 'wb').write(r.content)
    except:
        raise Exception('not a proper webpage')