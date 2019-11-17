"""
.. module:: version
   :platform: Unix
   :synopsis: Define the client and auth methods

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""


import logging
import requests

from validators.url import url as validate_url

from .exceptions import ConfigError, BadHTTPMethod


logger = logging.getLogger(__name__)


class ChinoClient:
    _official_urls = {
        'prod': 'https://api.chino.io',
        'test': 'https://api.test.chino.io',
    }
    _api_versions = ['v1']

    def __init__(self, label='test', url=None, port=None, force_https=True,
                 api_version='v1', session=True):
        """
        Init the base HTTP client

        :param label: if url not given, load the rel. labeled url
        :param url: format <protocol>://<host>[:<port>]
        :param port: used if not specified in url, default: 80
        :param force_https: forces https, and set port default to 443
        :param api_version: string to be appended to base_url,
                            default: 'v1'
        :param session: if True inited requests with `Session`

        """

        # url or valid label must be given
        url = url or self._official_urls.get(label, None)
        if not url:
            err = f"Bad label given: '{label}'. "
            err += f"Supported labels: {self._official_urls.keys()}"
            raise ConfigError(err)

        # http or https
        if force_https and 'https' not in url:
            url = url.replace('http', 'https')

        # port
        port_default = 443 if force_https else 80
        port = port or port_default

        # add port only if a single colon is found: else url is malformed
        if len(url.split(':')) == 2:
            url = f"{url}:{port}"

        # validate url
        if validate_url(url) is not True:
            raise ConfigError(f"Bad url: {url}")

        self._base_url = url

        # api version
        if api_version not in self._api_versions:
            err = f"Unsupported api version: '{api_version}'. "
            err += f"Supported versions: {self._api_versions}"
            raise ConfigError(err)

        self._api_version = api_version

        # ok setup the client
        self._client = requests if not session else requests.Session()

    def _build_url(self, resource):
        url = '/'.join([self._base_url, self._api_version, resource])
        logger.debug(f"Built url: {url}")
        return url

    def _call(self, method, url, **kwargs):
        # if given method is a valid requests method, run it
        client_method = getattr(self._client, method.lower(), None)
        if callable(client_method):
            return client_method(url, **kwargs)

        # method was not valid indeed
        raise BadHTTPMethod(f"Invalid HTTP method: '{method}'")

    def call(self, method, resource, **kwargs):
        """
        Perform an HTTP call to the chino server

        :param method: the HTTP method
        :param resource: the resource to append to base_url
        :param kwargs: all the supported args by requests for method
        :return: a requests.Response object

        """
        # build the full url
        url = self._build_url(resource)

        # delegate the rest to the private method
        return self._call(method, url, **kwargs)

    def get(self, resource, params=None):
        """
        Perform a GET request

        :param resource: the resource to append to base_url
        :param params: url params
        :return: a requests.Response object

        """
        return self.call('get', resource, params=params)

    def post(self, resource, data=None, params=None, form=None):
        """
        Performa POST request

        :param resource: the resource to append to base_url
        :param data: the payload
        :param params: url params
        :param form: form data
        :return: a requests.Response object

        """
        return self.call('post', resource, data=data, params=params, form=form)

    def put(self, resource, data=None):
        """

        :param resource: the resource to append to base_url
        :param data: the payload
        :return: a requests.Response object

        """
        return self.call('put', resource, data=data)

    def patch(self, resource, data=None):
        """

        :param resource: the resource to append to base_url
        :param data: the payload
        :return: a requests.Response object

        """
        return self.call('patch', resource, data=data)

    def delete(self, resource, params=None):
        """

        :param resource: the resource to append to base_url
        :param params: url params
        :return: a requests.Response object

        """
        return self.call('delete', resource, params=params)

    def check_connection(self):
        """
        Hit the chino server and check for an HTTP 200

        :return: bool

        """
        response = self._call('get', self._base_url)
        return response.status_code == 200

    @property
    def auth(self):
        return self._client.auth

    @auth.setter
    def auth(self, value):
        self._client.auth = value