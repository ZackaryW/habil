from dataclasses import dataclass
import json 
import functools
import logging
import habil_case
from habil_utils import caller_getattr
from habil_base.exceptions import HabiMissingTokenException, HabiRequestException
@dataclass(frozen=True)
class HabiToken:
    user_id : str
    api_token : str
    app_id : str = None 

    def __post_init__(self):
        if self.app_id is None:
            object.__setattr__(self, "app_id", self.user_id + "_habil")

    @staticmethod
    def get_global() -> 'HabiToken':
        return _SINGLETON_INSTANCE

    def set_global(self) -> None:
        global _SINGLETON_INSTANCE
        _SINGLETON_INSTANCE = self

    @property
    def headers(self) -> dict:
        return {
            'x-api-user': self.user_id,
            'x-api-key': self.api_token,
            'x-client': self.app_id
        }

    @classmethod
    def getlast(cls) -> 'HabiToken':
        if len(cls._instances) == 0:
            return None
        return cls._instances[-1]

    @classmethod
    def login(cls, username : str, password : str, appid : str=None, set_global : bool = False) -> 'HabiToken':
        res = habil_case.user.login(username=username, password=password, appid=appid)
        if res.fail:
            raise HabiRequestException(res)
        token = HabiToken.create(
            user_id=res.id,
            api_token=res.apiToken,
            app_id=appid,
            set_global=set_global
        )
        return token
    
    @classmethod
    def create(cls, user_id : str, api_token : str, app_id : str=None, set_global : bool = False) -> 'HabiToken':
        token = cls(user_id=user_id, api_token=api_token, app_id=app_id)
        if set_global:
            token.set_global()
        return token

    @classmethod
    def from_dict(cls, data : dict, set_global : bool = False) -> 'HabiToken':
        return cls.create(
            user_id=data.get('user_id', None),
            api_token=data.get('api_token', None),
            app_id=data.get('app_id', None),
            set_global=set_global
        )

    @classmethod
    def from_json(cls, jsonpath : str, set_global : bool = False) -> 'HabiToken':
        data = {}
        with open(jsonpath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data=data, set_global=set_global)


# ANCHOR global token 
_SINGLETON_INSTANCE = None

def token_required(glob :bool = True, dig:bool = True, dig_deep:bool = False, throw : bool = False) -> callable:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if "token" in kwargs and isinstance(kwargs["token"], HabiToken):
                kwargs["token"] = kwargs["token"].headers
                return func(*args, **kwargs)
            elif "token" in kwargs and isinstance(kwargs["token"], dict):
                return func(*args, **kwargs)
            elif not glob and not dig:
                raise ValueError("token is required")

            if dig and (token:=caller_getattr("token", default=None, deep=dig_deep)) is not None:
                if isinstance(token, HabiToken):
                    token = token.headers
                kwargs["token"] = token
                return func(*args, **kwargs)

            if glob:
                global _SINGLETON_INSTANCE
                if _SINGLETON_INSTANCE is not None:
                    kwargs["token"] = _SINGLETON_INSTANCE.headers
                    return func(*args, **kwargs)
            
            logging.debug("missing token")
            if throw:
                raise HabiMissingTokenException("token is required [token_required]")

            return func(*args, **kwargs)
                
        return wrapper
    return decorator
