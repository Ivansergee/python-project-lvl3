import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import os
import re


def download(output, url):
    if not os.path.exists(output):
        return 'Directory does not exist'

    html = requests.get(url).text
    host = urlparse(url).netloc
    basename = convert_url(url)
    html_name = basename + '.html'
    html_path = os.path.join(output, html_name)

    assets_dir = basename + '_files'
    assets_path = os.path.join(output, assets_dir)
    if not os.path.exists(assets_path):
        os.mkdir(assets_path)

    soup = BeautifulSoup(html, 'html.parser')
    for asset in soup.find_all(['img', 'link', 'script']):
        if 'src' in asset.attrs:
            attr = 'src'
        else:
            attr = 'href'
        asset_url = urljoin(url, asset.get(attr))
        if urlparse(asset_url).netloc == host:
            asset_name = convert_url(asset_url)
            asset_path = os.path.join(assets_path, asset_name)
            data = requests.get(asset_url).content
            save_file(asset_path, data)
            asset[attr] = os.path.join(assets_dir, asset_name)

    with open(html_path, 'w') as f:
        f.write(soup.prettify())

    return html_path


def convert_url(url):
    no_scheme = url.replace(urlparse(url).scheme + '://', '')
    root, ext = os.path.splitext(no_scheme)
    if ext and not ext.startswith('.htm'):
        return re.sub(r'\W', '-', root) + ext
    return re.sub(r'\W', '-', root)


def parse_html(html, tag, attr):
    pass


def save_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)
