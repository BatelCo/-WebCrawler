import urllib

import requests
from lxml import html

page = requests.get("https://en.wikipedia.org/wiki/Andy_Ram")
doc = html.fromstring(page.content)
for url in doc.xpath("//a/@href"):
    print(url)
