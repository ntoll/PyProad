"""
A simple module for making requests to Amazon's Product Advertising API.
Especially useful for obtaining product information.
"""
import urllib
import hashlib
import hmac
import base64
import httplib2
import datetime
from xml.dom.minidom import parseString, Document

# To hold a valid access key
ACCESS_KEY = ''
# To hold a valid secret key
SECRET_KEY = ''
# The service name of the Product Advertising API
SERVICE = 'AWSECommerceService'
# The version of the Product Advertising API this module targets
VERSION = '2010-11-01'
# Maps the supported locales with the appropriate amazon controlled domain
SUPPORTED_LOCALES = {
    "us": "ecs.amazonaws.com",
    "uk": "ecs.amazonaws.co.uk",
    "de": "ecs.amazonaws.de",
    "jp": "ecs.amazonaws.co.jp",
    "fr": "ecs.amazonaws.fr",
    "ca": "ecs.amazonaws.ca"}


def buildUrl(locale, timestamp, **kwargs):
    """
    Builds the correctly signed URL for a request. The ACCESS_KEY and
    SECRET_KEY values must be set to the appropriate values.

    :param locale: the API locale ['us', 'uk', 'de', 'jp', 'fr', 'ca']
    :param timestamp: current UTC timestamp (e.g. "2011-01-06T16:57:32.000")
    :param kwargs: other name-value pairs used to build the request

    For example, to build a URL for searching books with the term "harry
    potter" do the following::

        >>> timestamp = '%sZ' % datetime.datetime.utcnow().isoformat()
        >>> buildUrl('GET', 'us', timestamp, Operation='ItemSearch',
        ... SearchIndex='Books', Keywords='harry potter')
    """
    # 1) Create the name-value pairs
    namedValuePairs = dict(kwargs)
    namedValuePairs['Service'] = SERVICE
    namedValuePairs['Timestamp'] = timestamp
    namedValuePairs['AWSAccessKeyId'] = ACCESS_KEY
    namedValuePairs['Version'] = VERSION
    # 2) Sort the name-value pairs
    sortedPairs = ['%s=%s' % (n, urllib.quote(v))
        for n, v in namedValuePairs.iteritems()]
    sortedPairs.sort()
    pathArgs = '&'.join(sortedPairs)
    # 3) Get the signature
    domain = SUPPORTED_LOCALES[locale]
    stringToSign = "GET\n%s\n/onca/xml\n%s" % (domain, pathArgs)
    hashValue = hmac.new(SECRET_KEY, stringToSign, hashlib.sha256).digest()
    signature = base64.encodestring(hashValue).strip()
    # 4) Build the signed URL
    return "http://%s/onca/xml?%s&Signature=%s" % (domain, pathArgs,
        urllib.quote(signature, safe=''))


class AWSException(Exception):
    """
    Represents an error returned from the Product Advertising API
    """
    pass


class Request(object):
    """
    Represents a request to the Product Advertising API
    """

    def __init__(self, locale='us', **kwargs):
        """
        :param locale: the API locale ['us', 'uk', 'de', 'jp', 'fr', 'ca']
        :param kwargs: other name-value pairs used to build the request
        """
        self.locale = locale
        self.NameValuePairs = kwargs

    def callApi(self, page=0):
        """
        Makes a RESTful call to the Product Advertising API and returns the
        resulting XML for further processing.

        :param page: the page of results to return (defaults to first page)
        """
        timestamp = datetime.datetime.utcnow().isoformat()
        url = buildUrl(self.locale, timestamp, **self.NameValuePairs)
        http = httplib2.Http()
        headers, content = http.request(url, 'GET')
        return parseString(content)
