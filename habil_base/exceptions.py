class HabiBaseException(Exception):
    pass

class HabiMissingTokenException(HabiBaseException):
    pass

class HabiRequestException(HabiBaseException):
    def __init__(self, res,*args) -> None:
        self.res = res
        super().__init__(res.status_code, res.reason,*args)

    @property
    def reason(self):
        return self.res.reason

    @property
    def code(self):
        return self.res.code

class HabiRequestRateLimited(HabiBaseException):
    pass

class HabiLocalNotFoundException(HabiBaseException):
    pass