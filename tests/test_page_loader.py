import tempfile
import os
import requests
from bs4 import BeautifulSoup

from page_loader import download


def test_download(requests_mock):
    requests_mock.get('https://test.ru', text='data')
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download(tmpdir, 'https://test.ru')
        with open(path) as f:
            assert f.read() == 'data\n'


def test_download_assets(requests_mock):

    with open('tests/fixtures/test.html') as t:
        data = t.read()
    with open('tests/fixtures/res/style.css') as t:
        style = t.read()
    with open('tests/fixtures/res/main.js') as t:
        js = t.read()
    with open('tests/fixtures/test.png', 'rb') as t:
        pic = t.read()

    requests_mock.get('https://test.ru', text=data)
    requests_mock.get('https://test.ru/res/style.css', text=style)
    requests_mock.get('https://test.ru/res/main.js', text=js)
    requests_mock.get('https://test.ru/test.png', content=pic)
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download(tmpdir, 'https://test.ru')
        asset_dir = path.rstrip('.html') + '_files'
        assert os.path.exists(asset_dir)
        with open(path) as res:
            res_soup = BeautifulSoup(res.read(), 'html.parser')
            img_res = os.path.split(res_soup.find('img')['src'])[1]
            js_res = os.path.split(res_soup.find('script')['src'])[1]
            css_res = os.path.split(res_soup.find('link')['href'])[1]
            with open(os.path.join(asset_dir, img_res), 'rb') as r:
                assert r.read() == pic
            with open(os.path.join(asset_dir, js_res)) as r:
                assert r.read() == js
            with open(os.path.join(asset_dir, css_res)) as r:
                assert r.read() == style
