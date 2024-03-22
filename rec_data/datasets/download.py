import requests
from tqdm import tqdm


def download_url(url, filepath) -> None:
    """
    Download a file from the given URL and save it
    :param url: url to download
    :param filepath: path to save
    :return:
    """
    r = requests.get(url)
    r.raise_for_status()
    with open(filepath, 'wb') as file:
        with tqdm(unit='byte', unit_scale=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
                progress_bar.update(len(chunk))
