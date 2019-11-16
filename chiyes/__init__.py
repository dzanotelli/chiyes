from . import version


def get_version(short=False):
    """Returns the current drypy version.

    Optional args:
        short (bool): If True return just "major.minor"

    Returns:
        A string with the current drypy version.

    """
    if short:
        # extract the first two parts of version (eg '1.2' from '1.2.3')
        return '.'.join(version._version.split('.')[:2])
    else:
        return version._version
