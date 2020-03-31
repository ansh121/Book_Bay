from isbnlib import meta,cover
from isbnlib.config import add_apikey

import os

try:
    proxy = 'http://172.16.2.30:8080'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1/*,127.0.0.1'
except:
    print("proxy error")


SERVICE = 'isbndb'
APIKEY = 'temp475675837'  # <-- replace with YOUR key
# register your key
add_apikey(SERVICE, APIKEY)

isbn='9780141199610'
book=meta(isbn)
print(book)
print(cover(isbn))