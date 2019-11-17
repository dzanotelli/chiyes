import logging
import os

from requests.auth import HTTPBasicAuth

from .exceptions import MissingAuthConf


logger = logging.getLogger(__name__)


def register_auth_method(cls):
    if not hasattr(register_auth_method, 'supported_methods'):
        register_auth_method.supported_methods = []

    register_auth_method.supported_methods.append(cls)


def get_supported_methods():
    return getattr(register_auth_method, 'supported_methods', [])


class Authentication:
    auth_vars = []

    def __init__(self, client):
        self.environment = {}
        self.client = client

    def authenticate(self, **kwargs):
        self._read_environment()

        data = {}
        for item in self.auth_vars:
            data[item] = kwargs.get(item) or self.environment.get(item)

        # if all the values are not None
        if len([i for i in data.values() if i is None]) == 0:
            logger.info(f"{self.__class__.__name__}: authenticate")
            return self._authenticate(data)

        msg = f"Missing conf values for Auth method: {self.__class__.__name__}"
        raise MissingAuthConf(msg)

    def _authenticate(self, data):
        raise NotImplementedError()

    def _read_environment(self):
        for var in self.auth_vars:
            self.environment[var] = os.environ.get(var, None)


@register_auth_method
class CustomerKeyAuthentication(Authentication):
    auth_vars = ['chino_customer_id', 'chino_customer_key']

    def _authenticate(self, data):
        user = data['chino_customer_id']
        pwd = data['chino_customer_key']
        self.client.auth = HTTPBasicAuth(user, pwd)
