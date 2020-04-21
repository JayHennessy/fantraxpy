import logging
import getpass
import platform
import netrc
from datetime import datetime

from urllib.parse import urlparse
import requests

__version__ = '0.0.1'

def query_netrc(server, netrc_file=None, logger=None):
    remoteHost = urlparse(server)
    if not netrc_file:
        netrc = netrc.netrc()
    else:
        netrc = netrc.netrc(netrc_file)
    
    authTokens = netrc.authenticators(remoteHost)
    user = authTokens[0]
    password = authTokens[2]
    if logger:
        logger.info('Got password for {} from netrc file'.format(user))
    return user, password

def connect(server, user=None, password=None, netrc_file=None, logger=None, debug=None, loglevel=None):
    
    # Setup the logger for this connection
    if logger is None:
        logger = logging.getLogger('fantrax-{}'.format(datetime.now()))
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        # create formatter
        if debug:
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(module)s:%(lineno)d >> %(message)s')
        else:
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        if loglevel is not None:
            logger.setLevel(loglevel)
        elif debug:
            logger.setLevel('DEBUG')
        else:
            logger.setLevel('WARNING')

    # Get the login inf0
    if user is None and password is None:
        user, password = query_netrc(server, netrc_file, logger)

    if user is not None and password is None:
        password = getpass.getpass(prompt=str("Please enter the password for user '{}':".format(user)))

    requests_session = requests.Session()
    user_agent = "xnatpy/{version} ({platform}/{release}; python/{python}; requests/{requests})".format(
        version=__version__,
        platform=platform.system(),
        release=platform.release(),
        python=platform.python_version(),
        requests=requests.__version__
    )

    requests_session.headers.update({'User-Agent': user_agent})

    if user is not None:
        requests_session.auth = (user, password)
    
    fantrax_session = requests_session

    return fantrax_session
