from dataclasses import dataclass
import datetime
import requests
from habil_base.exceptions import HabiRequestRateLimited
from habil_map.habiMapResponse import HabiMapResponse

class HabiMapMeta:
    RATE_LIMIT = None
    MIN_TRIGGER_RATE_LIMIT = 1
    RATE_LIMIT_REMAINING = None
    LOGS = {}
    MAX_HOLD_LOGS = 50

    @classmethod
    def parse_rate_limit_state(cls, res: requests.Response):
        chances_remain = res.headers.get("X-RateLimit-Remaining", None)
        if chances_remain is None:
            return
        chances_remain = int(chances_remain)
        cls.RATE_LIMIT_REMAINING = chances_remain

        reset_time = res.headers.get("X-RateLimit-Reset", None)
        # parse string into datetime object
        if reset_time is not None:
            # Sat May 07 2022 23:29:36 GMT+0000 to strftime format
            try:
                reset_time = datetime.datetime.strptime(reset_time, "%a %b %d %Y %H:%M:%S %Z")
            except ValueError as v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    reset_time = reset_time[:-(len(v.args[0]) - 26)]
                    reset_time = datetime.datetime.strptime(reset_time, "%a %b %d %Y %H:%M:%S %Z")
                else:
                    raise v
        if chances_remain <= cls.MIN_TRIGGER_RATE_LIMIT:
            cls.RATE_LIMIT = reset_time

    @classmethod
    def check_rate_limit(cls):
        if cls.RATE_LIMIT is None:
            return
        gmt_now = datetime.datetime.utcnow()
        if gmt_now < cls.RATE_LIMIT:
            raise HabiRequestRateLimited("Rate Limited, wait until {}".format(cls.RATE_LIMIT))
        
    @classmethod
    def _log(cls, res : HabiMapResponse, caller_func ):
        cls.LOGS[str(caller_func).lower()] = res
        while len(cls.LOGS) > cls.MAX_HOLD_LOGS:
            cls.LOGS.popitem(last=False)

    @classmethod
    def logs(cls):
        return cls.LOGS

    @classmethod
    def get_log(cls, caller:str =None,**kwargs):
        if caller is None:
            return None
        if caller in cls.LOGS:
            return cls.LOGS[caller]
        for key, val in cls.LOGS.items():
            if caller is not None and isinstance(caller, str) and str(caller).lower() in key:
                return val
            if any(getattr(val, k, None) == v for k, v in kwargs.items()):
                return val
    
    @classmethod
    def get_last_log(cls):
        if len(cls.LOGS) == 0:
            return None
        # get last log
        return cls.LOGS.get(list(cls.LOGS.keys())[-1], None)