from dataclasses import dataclass
import dataclasses
import typing
from habil.other.profile import HabiProfile, HabiStatBox
from habil.sub.tag import HabiTag, HabiTagMeta
from habil_base.exceptions import HabiMissingTokenException
from habil_base.habiToken import HabiToken
from habil.tasking import HabiTasking
from habil_utils import FrozenClass
from habil_map.habiMapMeta import HabiMapMeta

class HabiClient(FrozenClass):
    

    def __init__(self, token : typing.Union[HabiToken, dict] = None):
        if token is None:
            token = HabiToken.get_root()
        
        if token is None:
            raise HabiMissingTokenException("No token found")
            
        self.token : HabiToken = token
        self._freeze()

    TASK = 0
    TAG = 1
    REWARD = 2
    HABIT = 3
    DAILY = 4
    TODO = 5

    def get(self, category : int, id : str):
        match category:
            case self.TASK: return HabiTasking.get(token=self.token, taskId=id)
            case self.TAG: return HabiTag.get(token=self.token, tagId=id)
            case _: raise ValueError(f"Unknown category {category}")
    
    def make(self, category : int, **kwargs):
        match category:
            case self.TASK: raise ValueError("Tasks is a generic category, please use REWARD, HABIT, DAILY, 2DO")
            case self.TAG: return HabiTag.create(token=self.token, name=kwargs.get("name"))
            case _: raise ValueError(f"Unknown category {category}")

    
    # ANCHOR classmethods
    @classmethod
    def login(cls, username : str, password : str, appid : str=None, set_root : bool = False) -> 'HabiClient':
        token = HabiToken.login(username=username, password=password, appid=appid, set_root=set_root)
        return cls(token=token)

    @classmethod
    def create(cls, user_id : str =None, api_token : str =None, app_id : str =None, json_path: str =None) -> 'HabiClient':
        if json_path is not None:
            token = HabiToken.from_json(json_path)
        else:
            token = HabiToken(user_id=user_id, api_token=api_token, app_id=app_id)
        return cls(token=token)

    # ANCHOR dynamic properties
    @property
    def stats(self):
        return HabiStatBox.get(token=self.token)

    @property
    def tasks(self):
        HabiTag.get_all(token=self.token)
        return HabiTasking.get_all(token=self.token)
    
    @property
    def tags(self):
        return HabiTag.get_all(token=self.token)

    @property
    def profile(self):
        return HabiProfile.get(token=self.token)

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