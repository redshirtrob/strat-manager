class InvalidYearException(Exception):
    def __init__(self, message):
        super(InvalidYearException, self).__init__(message)

class InvalidPlayerException(Exception):
    def __init__(self, message):
        super(InvalidPlayerException, self).__init__(message)

class InvalidLeagueException(Exception):
    def __init__(self, message):
        super(InvalidPlayerException, self).__init__(message)
        
