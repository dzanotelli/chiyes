"""
.. module:: version
   :platform: Unix
   :synopsis: Define the client and auth methods

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""


import requests

from validators.url import url as validate_url

from .exceptions import ConfigError


class Client:
    official_urls = {
        'prod': 'https://api.chino.io',
        'test': 'https://api.test.chino.io',
    }

    api_versions = ['v1']

    def __init__(self, label='test', url=None, port=80, force_https=True,
                 api_version='v1'):
        # url or valid label must be given
        url = url or self.official_urls.get(label, None)
        if not url:
            err = f"Bad label given: '{label}'. "
            err += f"Supported labels: {self.official_urls.keys()}"
            raise ConfigError(err)

        # add port only if a single colon is found: else url is malformed
        if len(url.split(':')) == 2:
            url.append(f":{port}")

        if force_https:
            url = url.replace('http', 'https')

        # validate url
        if validate_url(url) is not True:
            raise ConfigError(f"Bad url: {url}")

        # api version
        if api_version not in self.api_versions:
            err = f"Unsupported api version: '{api_version}'. "
            err += f"Supported versions: {self.api_versions}"
            raise ConfigError(err)

        # build the final url
        self._url = '/'.join(url, api_version)
        self._client = self._init_client(url)

    def _init_client(self, url):
        pass
