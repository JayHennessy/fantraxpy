
import pandas as pd


class Player():

    POSITION_MAP = {206: 'C',
                    203: 'LW',
                    204: 'RW',
                    202: 'D',
                    'xx': 'G'
                    }

    STATUS_MAP = {1: 'active',
                2: 'bench',
                3: 'injured'
                }

    def __init__(self, name=None, team=None, teamId=None, rookie=False,
                    firstname=None, lastname=None, age=None, position=None, 
                    positionId=None, elig_positionIds=None, status=None,
                    statusId=None, elig_statusIds=None, scorerId=None,
                    fan_points=None, opponent=None, gameId=None, 
                    roster_json=None
                ):
        self._name = name
        self._team = team
        self._teamId = teamId
        self._rookie = rookie
        self._age = age
        self._position = POSITION_MAP[positionId]
        self._positionIds = positionId 
        self._elig_positionIds = elig_positionIds
        self._status = STATUS_MAP[statusId]
        self._statusId = statusId 
        self._elig_statusIds = elig_statusIds
        self._scorerId = scorerId
        self._fan_points = fan_points
        self._opponent = opponent
        self._gameID = gameId
        self._roster_json = roster_json

        self._season_stats = self._parse_player_stats()

    @property
    def name(self):
        return self._name

    @property
    def team(self):
        return self._team

    @property
    def teamId(self):
        return self._teamId
        
    @property
    def rookie(self):
        return self._rookie

    @property
    def age(self):
        return self._age

    @property
    def position(self):
        return self._position
    
    @property
    def elig_positionIds(self):
        return self._elig_positionIds
    
    @property
    def positionId(self):
        return self._positionId

    @property
    def status(self):
        return self._status
    
    @property
    def statusId(self):
        return self._statusId
    
    @property
    def elig_statusIds(self):
        return self._elig_statusIds
    
    @property
    def scorerId(self):
        return self._scorerId

    @property
    def fan_points(self):
        return self._fan_points
    
    @property
    def opponent(self):
        return self._opponent

    def drop(self):
        """ Remove player from roster."""
        pass
        #TODO

    def add(self):
        """ Add player to Roster."""
        pass
        #TODO
    
    def bench_player(self, player):
        """ Move player to bench"""
    pass
    #TODO

    def activate_player(self, player):
        """ Move player to roster """
        pass
        # TODO

    def _parse_player_stats(self):
        """ Parse the requests response to get season stats
        Note: the raw json should be from get_roster_info
        """
        if self.position == 'G':
            pos = 1
        else:
            pos = 0 
        
        player_idx = self._find_player_tabke_idx()
        stats = self._roster_json['tables'][pos]['rows'][player_idx]['cells'] 
        col = self._roster_json['tables'][pos]['headers']['cells']

        # get the stat header column names
        data = {}
        for idx in len(col):
            if idx == 0:
                continue # this is the opponent not stats
            data[col[idx]['shortName']] = stats[idx]['content']

        return data

    def _find_player_tabke_idx(self):
        if self.position == 'G':
            pos = 1
        else:
            pos = 0 
        
        player_cells = self._roster_json['tables'][pos]['rows']
        for idx in player_cells:
            if player_cells[idx]['scorer']['name'] == self.name:
                return idx
        return None