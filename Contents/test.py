import urllib2
import ssl
import logging


SEARCH_URL = 'https://www.javbus.com/search/%s'
keyword = "SSIS-088"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


request = urllib2.Request(SEARCH_URL % keyword,headers=headers)
response = urllib2.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
data = response.read()
