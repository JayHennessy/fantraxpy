import fantraxpy.fantraxUtils as util
from .constants import URL

class League():
    def __init__(self, leagueId=None, session=None, name=None, teams=None,
                    sport=None, sportId=None, season=None):
        self.session = session
        self._name = name
        self._teams = teams
        self._leagueId = leagueId
        self._teams = teams
        self._sport = sport
        self._sportId = sportId
        self._season = season
        self._get_fantasy_league_home_info()

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def teams(self):
        return self._teams
    
    @teams.setter
    def teams(self, team):
        self._team = team
    
    @property
    def sport(self):
        return self._sport
    
    @sport.setter
    def sport(self, sport):
        self._sport = sport
    
    @property
    def sportId(self):
        return self._sportId
    
    @sportId.setter
    def sportId(self, sportId):
        self._sportId = sportId
    
    @property
    def leagueId(self):
        return self._leagueId
    
    @leagueId.setter
    def leagueId(self, leagueId):
        self._leagueId = leagueId

    @property
    def season(self):
        return self._season
    
    @season.setter
    def season(self, season):
        self._season = season

    
    def _get_league_home_info(self):         
        payload = util._league_home_info_payload(self.leagueId)
        response = self.session.post(URL, json=payload).json()
        util._check_response(response)
        return response['responses'][0]['data']