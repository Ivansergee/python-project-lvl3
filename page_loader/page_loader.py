import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import re


def download(output, url):
    if not os.path.exists(output):
        return 'Directory does not exist'

    r = requests.get(url)
    basename = re.sub(r'\W', '-', re.split('//', r.url.rstrip('/'))[1])
    html_name = basename + '.html'
    assets_dir = basename + '_files'
    html_path = os.path.join(output, html_name)
    assets_path = os.path.join(output, assets_dir)

    if not os.path.exists(assets_path):
        os.mkdir(assets_path)
    soup = BeautifulSoup(r.text, 'html.parser')
    for img in soup.find_all('img'):
        img_url = urljoin(url, img.get('src'))
        img_content = requests.get(img_url).content
        img_name = re.sub(
            r'\W',
            '-',
            re.split('//', os.path.splitext(img_url.rstrip('/'))[0])[1]
        ) + '.png'
        img_path = os.path.join(assets_path, img_name)
        img['src'] = os.path.join(assets_dir, img_name)
        with open(img_path, 'wb') as f:
            f.write(img_content)

    with open(html_path, 'w') as f:
        f.write(soup.prettify())
    return html_path
