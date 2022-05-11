from dataclasses import dataclass
from datetime import datetime, timedelta
import typing
from habil.elements.daily import HabiDaily
from habil.elements.habit import HabiHabit
from habil.elements.reward import HabiReward
from habil.elements.todo import HabiTodo
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
        
        self._last_fetch_timestamp = None

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

    
    # ANCHOR internals
    def _set_timestamp(self):
        object.__setattr__(self, "_last_fetch_timestamp", datetime.utcnow())

    def _need_to_fetch(self):
        if self._last_fetch_timestamp is None:
            return True
        return (datetime.utcnow() - timedelta(seconds=self.CONFIG_TASKS_cache_expire_seconds)) > self._last_fetch_timestamp

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
        if not self._need_to_fetch():
            return self.tasks_cached

        HabiTag.get_all(token=self.token)
        ret = HabiTasking.get_all(token=self.token)
        self._set_timestamp()
        return ret
    
    @property
    def tasks_cached(self):
        all_lists =[]
        all_lists.extend(HabiDaily.get_by_userid(userid=self.token.user_id))
        all_lists.extend(HabiHabit.get_by_userid(userid=self.token.user_id))
        all_lists.extend(HabiTodo.get_by_userid(userid=self.token.user_id))
        all_lists.extend(HabiReward.get_by_userid(userid=self.token.user_id))
        return all_lists

    @property
    def tags(self):
        if not self._need_to_fetch():
            return self.tags_cached
        return HabiTag.get_all(token=self.token)

    @property
    def tags_cached(self):
        return HabiTag.get_by_userid(userid=self.token.user_id)

    @property
    def profile(self):
        return HabiProfile.get(token=self.token)

    @property
    def profile_cached(self):
        res = HabiProfile.get_by_userid(userid=self.token.user_id)
        if len(res) == 0:
            return None
        return res[0]

    @property
    def dailys(self):
        if not self._need_to_fetch():
            return self.dailys_cached
        tasks = self.tasks
        return [t for t in tasks if isinstance(t, HabiDaily)]

    @property
    def dailys_cached(self):
        return HabiDaily.get_by_userid(userid=self.token.user_id)

    @property
    def habits(self):
        if not self._need_to_fetch():
            return self.habits_cached

        tasks = self.tasks
        return [t for t in tasks if isinstance(t, HabiHabit)]
    
    @property
    def habits_cached(self):
        return HabiHabit.get_by_userid(userid=self.token.user_id)

    @property
    def rewards(self):
        if not self._need_to_fetch():
            return self.rewards_cached
        tasks = self.tasks
        return [t for t in tasks if isinstance(t, HabiReward)]

    @property
    def rewards_cached(self):
        return HabiReward.get_by_userid(userid=self.token.user_id)

    @property
    def todos(self):
        if not self._need_to_fetch():
            return self.todos_cached
        tasks = self.tasks
        return [t for t in tasks if isinstance(t, HabiTodo)]
    
    @property
    def todos_cached(self):
        return HabiTodo.get_by_userid(userid=self.token.user_id)

    # ANCHOR config properties
    @property
    def CONFIG_GLOBAL_TAGS_refresh_interval(self):
        return HabiTagMeta.PULL_INTERVAL
    
    @CONFIG_GLOBAL_TAGS_refresh_interval.setter
    def CONFIG_GLOBAL_TAGS_refresh_interval(self, value):
        HabiTagMeta.PULL_INTERVAL = value

    @property
    def CONFIG_TASKS_cache_expire_seconds(self):
        """
        this property sets the time in seconds that the cache will be called instead of remote\n
        default is 0, meaning that the client by default will fetch from api every time\n
        is only valid for tasks
        """
        if not hasattr(self, "_CONFIG_TASKS_cache_expire_seconds"):
            object.__setattr__(self, "_CONFIG_TASKS_cache_expire_seconds", 0)
        
        return self._CONFIG_TASKS_cache_expire_seconds

    @CONFIG_TASKS_cache_expire_seconds.setter
    def CONFIG_TASKS_cache_expire_seconds(self, value):
        if not isinstance(value, int):
            raise ValueError("CONFIG_TASKS_cache_expire_seconds must be an integer")
        object.__setattr__(self, "_CONFIG_TASKS_cache_expire_seconds", value)


    # ANCHOR stats
    @property
    def STAT_rate_limit_remaining(self):
        return HabiMapMeta.RATE_LIMIT_REMAINING