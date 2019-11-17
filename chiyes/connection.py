import logging

from .auth import get_supported_methods
from .exceptions import MissingAuthConf
from .client import ChinoClient


logger = logging.getLogger(__name__)


def connect(**kwargs):
    """
    Connect to the remote chino server

    :param kwargs:
    :return:

    """
    logger.info("Setting up connection to remote chino server ...")

    # FIXME: define args to pass
    client = ChinoClient(**kwargs)
    if not client.check_connection():
        msg = "Error while checking connection with remote chino server"
        logger.warning(msg)

    # FIXME: define args to pass
    auth(client, **kwargs)


def auth(client, **kwargs):
    """
    Setup the authentication method

    :param client: a ChinoClient object
    :return: bool
    """
    logger.info("Setting authentication method ...")

    for method_cls in get_supported_methods():
        try:
            return method_cls(client).authenticate(**kwargs)
        except MissingAuthConf:
            logger.debug(f"{method_cls} failed, skip to next")
            continue

    raise MissingAuthConf("None auth method set")
