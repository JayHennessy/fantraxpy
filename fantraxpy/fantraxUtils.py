import json
import requests
import netrc
import getpass
from pprint import pprint

from .league import League
from .player import Player
from .roster import Roster
from .user import FantraxUser as User
from .exceptions import FantraxRequestError
from .constants import URL, VERSION, FANTRAX_TOKEN

URL = 'https://www.fantrax.com/fxpa/req'

## TODO
# DONE: 1) Deal with token (get it from the env variable)
# 2) return response and json
# 3) deal with errors
# 4) create a cache to pull info from so I don't keep redownloading


BASE_PAYLOAD = {'msgs': [],
                'ng2': True,
                'href':'',
                'dt':1,
                'at':0,
                'tz':'America/Indianapolis',
                'v': VERSION}

def _build_payload():
    payload = {'msgs': [],
                'ng2': True,
                'href':'',
                'dt': 0,
                'at': 0,
                'tz':'America/Indianapolis',
                'v': VERSION}
    return payload

def _login_payload(user, password, token):
    payload = BASE_PAYLOAD
    payload['msgs'] =[{'method':'login',
                        'data':
                            {'u': user,
                            'p':password,
                            't': token,
                            'v':3
                            }
                        }]
    payload['href'] = 'https://www.fantrax.com'
    return payload

def _fantasy_league_info_payload(leagueId):
    payload = BASE_PAYLOAD
    payload['href'] = 'https://www.fantrax.com/fantasy/{}/home'.format(leagueId)
    payload['msgs'] = [{'method':'getFantasyLeagueInfo',
                    'data': {}
                    }]
    return payload

def _league_home_info_payload(leagueId):
    payload = BASE_PAYLOAD
    payload['href'] = 'https://www.fantrax.com/fantasy/{}/home'.format(leagueId)
    payload['msgs'] = [{'method':'getLeagueHomeInfo',
                    'data': {}
                    }]
    return payload

def _team_roster_info_payload(leagueId, teamId):
    payload = BASE_PAYLOAD
    payload['msgs'] = [{'method':'getTeamRosterInfo',
                    'data': {'leagueId': leagueId,
                            'teamId': teamId}
                    }]
    payload['href'] = 'https://www.fantrax.com/fantasy/league/{}/home'.format(
                        leagueId)
    return payload

def _execute_team_roster_change_payload(teamId, roster_limit_period, fieldMap):
    payload = BASE_PAYLOAD
    payload['msgs'] = [{'method':'confirmOrExecuteTeamRosterChanges',
                    'data': {'rosterLimitPeriod': roster_limit_period,
                            'fantasyTeamId': teamId,
                            'daily': 'false',
                            'adminMode': 'false',
                            'confirm': 'true',
                            'applyToFuturePeriods': 'true',
                            'fieldMap': fieldMap}
                    }]
    return payload

def _parse_login(response, session):
    
    # create league
    pprint(response)
    leagues = response['responses'][0]['data']['leagues']
    fantrax_league = League(session=session,
                            leagueId=leagues[0]['leaguesTeams'][0]['leagueId'],
                            sport=leagues[0]['sport'],
                            sportId=leagues[0]['sportId'],
                            name=leagues[0]['leaguesTeams'][0]['league'],
                            season=leagues[0]['season']
                            )

    # create a user
    user_info = response['responses'][0]['data']['userInfo']
    fantrax_user = User(username=user_info['username'],
                        token=FANTRAX_TOKEN,
                        userId=user_info['userId'],
                        team=leagues[0]['leaguesTeams'][0]['team'],
                        teamId=leagues[0]['leaguesTeams'][0]['teamId'],
                        email=leagues[0]['leaguesTeams'][0]['email'])

    return fantrax_user, fantrax_league

def _login(session):
    payload = _login_payload(*session.auth, FANTRAX_TOKEN)
    response = session.post(URL, json=payload).json()
    _check_response(response)
    user, league = _parse_login(response, session)
    return user, league, response

def _check_response(response):
        if 'pageError' in response.keys():
            raise FantraxRequestError()
        for x in  response['responses']:
            if 'errors' in x.keys():
                pprint(response['responses'])
                raise FantraxRequestError(x['errors'][0]['text'])


def _get_league_home_info(session, leagueId):         
    payload = _league_home_info_payload(leagueId)
    response = session.post(URL, json=payload).json()
    _check_response(response)
    return response['responses'][0]['data']

def _get_team_roster_info(session, leagueId, teamId):  
    payload = _team_roster_info_payload(leagueId, teamId)
    response = session.post(URL, json=payload).json()
    _check_response(response)
    return response['responses'][0]['data']

def get_teams(leagueId):
    data = _get_league_home_info(leagueId)
    teams = {}
    for team in data['fantasyTeams']:
        teams[team['name']] = team['id']
    return teams

def get_roster(leagueId, team):
    data = _get_league_home_info(leagueId)

    # roster = Roster()
    players = {}
    for player in data['players']['myTeams']:
        players[player['scorerFantasy']['name']] = player['scorerFantasy']
    return players

def get_roster(leagueId, team):
    data = _get_team_roster_info(leagueId)

    # roster = Roster()
    players = {}
    for player in data['players']['myTeams']:
        players[player['scorerFantasy']['name']] = player['scorerFantasy']
    return players

def _get_player_map(player, team):
    """ stid is to say if the palyer is in or not. 
        1 = in game
        2 = on bench
        3 = goalie spot
    """
    # changeMap = {'id1': {'posId': '206', 'stId': '1'},
    #         'id2': {'posId': '206', 'stId': '1'}}
    roster = get_roster(team)
    #ToDo
    
def get_roster_limit_period():
    pass

def write_json(json_data, json_file):
    with open(json_file, 'w') as f:
        json.dump(json_data, f) 

def team_name_from_id(teamId):
    """convert teamId to team name"""
    pass

def league_name_from_id(teamId):
    """convert leagueId to league name"""
    pass

def query_netrc(server):
    netrc = netrc.netrc()
    authTokens = netrc.authenticators(server)
    return authTokens[0], authTokens[2]

def _user_setup(username=None, password=None, server=None):
        if not server:
            server = URL
        if username is None and password is None:
            username, password = query_netrc(server)

        if username is not None and password is None:
            password = getpass.getpass(prompt=str(
                    "Please enter the password for user '{}':".format(username)
                                        )        )
        return username, password