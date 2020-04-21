import logging
import requests
import platform
from datetime import datetime
from pprint import pprint


import fantraxpy.fantraxUtils as util
from .user import FantraxUser
from .exceptions import *
from .league import League
from .roster import Roster
from .constants import URL, VERSION, FANTRAX_TOKEN, __version__

class Fantrax():

    def __init__(self, username=None, password=None, server=URL, token=None):
        
        self.logger = self._set_logger()
        self.league = None
        self.roster = None
        self.user = None
        self.password = None
        self.token = None
        self.server = server
        self.session = self.login(self.server,
                                    username=username,
                                    password=password,
                                    token=token)

    
    def login(self, server, username=None, password=None, token=None):
        if not token:
            token = FANTRAX_TOKEN

        try:
            requests_session = requests.Session()
        except Exception:
            self.log.error('Failed to connect to fantrax.com')
            raise FantraxConnectionError()
            
        user_agent = "fantrax/{version} ({platform}/{release}; python/{python}; requests/{requests})".format(
            version=__version__,
            platform=platform.system(),
            release=platform.release(),
            python=platform.python_version(),
            requests=requests.__version__
        )

        requests_session.headers.update({'User-Agent': user_agent})
        username, password = util._user_setup(username=username,
                                        password=password,
                                        server=server)
        
        requests_session.auth = (username, password)

        # Gather info
        self.user, self.league, _ = util._login(requests_session)
        self.roster = Roster(leagueId=self.league.leagueId,
                            team=self.user.team,
                            teamId=self.user.teamId
                            )
        print('user ' + username)
        return requests_session

    def _set_logger(self, logger=None, level=None, debug=False):
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

            if level is not None:
                logger.setLevel(level)
            elif debug:
                logger.setLevel('DEBUG')
            else:
                logger.setLevel('WARNING')

    def bench_player(self, player):
        """ Move player to bench"""
        pass
        #TODO

    def activate_player(self, player):
        """ Move player to roster """
        pass
        # TODO


class FantraxBaseObject():

    def __init__(self, session=None):
        self._session = session
        self._uri = URL

    @property
    def session(self):
        return self._session
    
    @property
    def uri(self):
        return self._uri
    
    def _build_payload(self):
        payload = {'msgs': [],
                'ng2': True,
                'href':'',
                'dt':1,
                'at':0,
                'tz':'America/Indianapolis',
                'v': VERSION}
        return payload

    def _send_request(self, method, session, url=None,  payload=None,
                        params=None, headers=None):
        if not url:
            url = URL
        r = session.request(method, url, params=params,
                            headers=headers, json=payload)
        util._check_response(r.json())
        return r.json()


    