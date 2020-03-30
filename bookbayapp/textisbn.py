import os

proxy = 'http://172.16.2.30:8080'

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


from isbnlib import meta
from isbnlib.config import add_apikey
from isbnlib.registry import bibformatters

SERVICE = 'isbndb'
APIKEY = 'temp475675837'  # <-- replace with YOUR key

# register your key
add_apikey(SERVICE, APIKEY)

# now you can use the service
isbn = '9780262033848'
bibtex = bibformatters['bibtex']
print(meta(isbn))