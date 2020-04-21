
class FantraxAPIKeyMissingError(Exception):
    pass

class FantraxRequestError(Exception):
    def __init__(self, data=None, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = 'An error occured with FantraxAPI'
        super(FantraxRequestError, self).__init__(msg)
        self.data = data


class FantraxConnectionError(Exception):
    """ Failed trying to connect to fantrax.com"""
    pass

class FantraxRosterError(Exception):
    """ Failed trying to connect to fantrax.com"""
    pass