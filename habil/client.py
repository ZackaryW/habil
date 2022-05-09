from dataclasses import dataclass
import dataclasses
import typing
from habil.sub.tag import HabiTag, HabiTagMeta
from habil_base.exceptions import HabiMissingTokenException
from habil_base.habiToken import HabiToken
from habil.tasking import HabiTasking
from habil_utils import FrozenClass
from habil_map.habiMapMeta import HabiMapMeta

class HabiClient(FrozenClass):
    TASK = 0
    #TAG = 1

    def __init__(self, token : typing.Union[HabiToken, dict] = None):
        if token is None:
            token = HabiToken.get_global()
        
        if token is None:
            raise HabiMissingTokenException("No token found")

        self.token : HabiToken = token
        self._freeze()

    

    def get(self, category : int, id : str):
        if category == self.TASK:
            return HabiTasking.get(token=self.token, taskId=id)
    
    def create(self, category : int, **kwargs):
        raise NotImplementedError

    # ANCHOR classmethods
    @classmethod
    def login(cls, username : str, password : str, appid : str=None, set_global : bool = False) -> 'HabiClient':
        token = HabiToken.login(username=username, password=password, appid=appid, set_global=set_global)
        return cls(token=token)

    # ANCHOR dynamic properties
    @property
    def tasks(self):
        HabiTag.get_all(token=self.token)
        return HabiTasking.get_all(token=self.token)
    
    @property
    def tags(self):
        return HabiTag.get_all(token=self.token)

    @property
    def character(self):
        raise NotImplementedError

    # ANCHOR config properties
    @property
    def CONFIG_GLOBAL_TAGS_refresh_interval(self):
        return HabiTagMeta.PULL_INTERVAL
    
    @CONFIG_GLOBAL_TAGS_refresh_interval.setter
    def CONFIG_GLOBAL_TAGS_refresh_interval_setter(self, value):
        HabiTagMeta.PULL_INTERVAL = value

    # ANCHOR stats
    @property
    def STAT_rate_limit_remaining(self):
        return HabiMapMeta.RATE_LIMIT_REMAINING