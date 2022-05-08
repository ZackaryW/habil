class HabiBaseException(Exception):
    pass

class HabiMissingTokenException(HabiBaseException):
    pass

class HabiRequestException(HabiBaseException):
    def __init__(self, res,*args) -> None:
        super().__init__(res.status_code, res.reason,*args)

class HabiRequestRateLimited(HabiBaseException):
    pass

