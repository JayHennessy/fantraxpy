#!/home/jay/anaconda3/envs/insta-env

import requests
from pprint import pprint

class FantraxAPIError(Exception):
    def __init__(self, data=None, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = 'An error occured with FantraxAPI'
        super(FantraxAPIError, self).__init__(msg)
        self.data = data

class FantraxAPI():
    def __init__(self, user='jayhen', password='iD#6VHCT7h2cRwe'):
        self.user = user
        self.password = password
        self.token = None
        self.token = '03AOLTBLQ1iUTuFTsKAI6-QDbvRijnNN-jTGdk8Cbfnl6YJdb8lwe_lMwVdyT1m3XDydSwj0lM5P5cZJudXr47D6vVdcDCzvhWkNfdnOTbw7KRzPu3GoGsaahcMpXdHnyizH5QeoYIVPzAmLqPbh9h_XFHNS4_NoiGRjNq5AfX6fqqNqm4G1gcDwb9l19qsnz9FpWS5uOrd1N_5PDgsp9p41XH4ftSeFUvav7sfYtFnFe-supP1EqONWO2RG6_lSBNq10xz6OByKg4P_haieqfuoITfMU2ILy1J5yQ97LC_58k6CT_nKRcz5HrRO0auqjdihooxFojZ-GYXtspQz1fFaRThIBHCB_hzQ1F1lWVDz-2-dQZqv_U3c7rKd89EbKfL1D3f1YF-FdOusAU8WiQgELLMPLasfHcKLFggQPfj-ansO54L_yPmT5ELa_rNTzGcpeobT79ynxlSG9n3EJRpMCCCIh1zCLJMjpzZry_StRcsKWXqt-LCDMZ4oDPFvy4fjNRL9daeQdM'
        self.url = 'https://www.fantrax.com/fxpa/req'
        self.version = '9.3.2'
        self.session = self.connect()
        self.role = []
        self.userId = ''
        self.payload = {'msgs':
                    [{'method':'login',
                    'data':
                        {'u': self.user,
                        'p': self.password,
                        't': self.token,
                        'v':3
                        }
                    }],
                'ng2': True,
                'href':'https://www.fantrax.com/login',
                'dt':1,
                'at':0,
                'tz':'America/Indianapolis',
                'v': self.version}
    
    def login(self):
        payload = self.payload
        payload['href'] = 'https://www.fantrax.com/login'
        payload['msgs'] = [{'method':'login',
                            'data': {'u': self.user,
                                    'p': self.password,
                                    't': self.token,
                                    'v':3
                                    }
                            }]       
 
        response = requests.post(self.url, json=payload)
        resp_dict = response.json()
        if 'pageError' in resp_dict.keys():
            pprint(resp_dict)
            raise FantraxAPIError(msg='Problem Logging In')
        leagues = resp_dict['responses'][0]['data']['leagues']
        self.sport = leagues[0]['sport']
        self.sportId = leagues[0]['sportId']
        self.league = leagues[0]['leaguesTeams'][0]['league']
        self.leagueId = leagues[0]['leaguesTeams'][0]['leagueId']
        self.team = leagues[0]['leaguesTeams'][0]['team']
        self.teamId = leagues[0]['leaguesTeams'][0]['teamId']

        user_info = resp_dict['responses'][0]['data']['userInfo']
        self.userId = user_info['userId']
        self.username = user_info['username']
        self.roles = resp_dict['roles']
    
    def create_payload(self):
        pass

    def logout(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_league(self):
        return self.league

    def set_league(self, league):
        self.league = league
        

    def get_team(self):
        pass

    def set_team(self):
        pass

    def _get_fantasy_league_info(self):
               
        params = {'leagueId': self.leagueId}
        payload = self.payload
        payload['href'] = 'https://www.fantrax.com/fantasy/{}/home'.format(self.leagueId)
        payload['msgs'] = [{'method':'getFantasyLeagueInfo',
                            'data': {}
                            }]
        response = requests.post(self.url, params=params, json=payload)
        resp_dict = response.json()
        if 'pageError' in resp_dict.keys():
            pprint(resp_dict)
            return {}
        data = resp_dict['responses'][0]['data']
        return resp_dict

    def get_all_teams(self):
        data = self._get_fantasy_league_info()
        teams = {}
        for team in data['fantasyTeams']:
            teams[team['name']] = team['id']
        return teams
        
    def get_all_teamIds(self):
        data = self._get_fantasy_league_info()
   

def main():
    pass

if __name__ == '__main__':
    main()