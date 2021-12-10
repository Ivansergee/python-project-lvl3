import tempfile

from page_loader import download


def test_download(requests_mock):
    requests_mock.get('https://ru.hexlet.io/courses', text='data')
    with tempfile.TemporaryDirectory() as tmpdir:
        path = download(tmpdir, 'https://ru.hexlet.io/courses')
        with open(path) as f:
            assert f.read() == 'data'
