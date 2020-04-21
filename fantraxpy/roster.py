#
#
#
import fantraxpy.fantraxUtils as util
from .player import Player
from .exceptions import FantraxRosterError

class Roster():

    def __init__(self, leagueId=None, teamId=None, team=None, players=None):
        self._players = players
        self._leagueId = leagueId
        self._teamId = teamId
        self._team = team
        self.raw_json = util._get_team_roster_info(leagueId, teamId)
        self._get_roster_skaters(self, leagueId, teamId)

    @property
    def leagueId(self):
        return self._leagueId

    @property
    def team(self):
        return self._team

    @property
    def teamId(self):
        return self._teamId

    @property
    def players(self):
        return self._players
    
    @players.setter
    def players(self, players):
        """ Append players dict to existing players dict"""
        try:
            self.players.update(players)
        except ValueError as e:
            print("Failed to add players to roster")
            raise FantraxRosterError

    def add_player(self):
        """ Add a player by name to the roster"""

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
    
    def _get_roster_skaters(self, leagueId, teamId):
        """Add all the skaters to the roster."""
        for skater in self.raw_json['tables'][0]['rows']:
            # this loops through the table rows, home of which are headers so it
            # needs to do this check
            if ('scorer' in skater) and ('posId' in skater):
                player = Player(name=skater['scorer']['name'],
                                positionId=skater['posId'],
                                elig_statusIds=skater['eligibleStatusIds'],
                                statusId=skater['statusId'],
                                elig_positionIds=skater['eligiblePosIds'],
                                team=skater['scorer']['teamName'],
                                scorerId=skater['scorer']['scorerId'],
                                rookie=skater['scorer']['rookie'],
                                teamId=skater['scorer']['teamId'],
                                opponent=skater['cells'][0]['content'],
                                gameId=skater['cells'][0]['gameId'],
                                roster_json=self.raw_json)
                self.players({player.name: player})
        