


import fantraxpy.fantraxUtils as util


class FantraxUser():

    def __init__(self, user=None, password=None, token=None, userId=None,
                        team=None, teamId=None, email=None):
        self._user, self._password = self.user_setup(user, password)
        self._token = token
        self._auth = (self._user, self._password)
        self._userId = userId
        self._team = team
        self._teamId = teamId
        self._email = email

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        self._user = user

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = password

    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, token):
        self._token = token

    @property
    def userId(self):
        return self._userId
    
    @userId.setter
    def userId(self, userId):
        self._userId = userId

    @property
    def team(self):
        return self._team
    
    @team.setter
    def team(self, team):
        self._team = team

    @property
    def teamId(self):
        return self._teamId
    
    @teamId.setter
    def teamId(self, teamId):
        self._teamId = teamId

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email

    @property
    def auth(self):
        return (self._user, self._password)
    
    @auth.setter
    def auth(self, user, password):
        self._auth = (user, password)

    