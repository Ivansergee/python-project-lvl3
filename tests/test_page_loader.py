import tempfile
import requests
import os
from bs4 import BeautifulSoup

from page_loader import download


def test_download(requests_mock):
    requests_mock.get('https://test.ru', text='data')
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download(tmpdir, 'https://test.ru')
        with open(path) as f:
            assert f.read() == 'data\n'


def test_download_img(requests_mock):
    with open('tests/fixtures/test.html') as t, open('tests/fixtures/test_result.html') as r:
        data = t.read()
        result = r.read()
    requests_mock.get('https://test.ru', text=data)
    requests_mock.get('https://test.ru/test.png', text='test.png')
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download(tmpdir, 'https://test.ru')
        assert os.path.exists(path.rstrip('.html') + '_files')
        assert os.listdir(path.rstrip('.html') + '_files')
        with open(path) as res:
            soup = BeautifulSoup(res.read(), 'html.parser')
            res_soup = BeautifulSoup(result, 'html.parser')
            img, img_res = soup.find('img'), res_soup.find('img')
            assert img['src'] == img_res['src']
