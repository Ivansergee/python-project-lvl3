import requests
import os
import re


def download(output, url):
    r = requests.get(url)
    data = r.text
    filename = re.sub(r'\W', '-', re.split('//', r.url.rstrip('/'))[1]) + '.html'
    if os.path.exists(output):
        abspath = os.path.join(output, filename)
        with open(abspath, 'w') as f:
            f.write(data)
        return abspath
    else:
        return 'Directory does not exist'
