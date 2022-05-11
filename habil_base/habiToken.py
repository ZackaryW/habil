from dataclasses import dataclass
import json 
import functools
import logging
import habil_case
from habil_utils import caller_getattr
from habil_base.exceptions import HabiMissingTokenException, HabiRequestException

class HabiTokenMeta:
    ROOT =None
    INSTANCES = {}
    
    @staticmethod
    def get(id):
        if id not in HabiTokenMeta.INSTANCES:
            return None
        return HabiTokenMeta.INSTANCES[id]
    
    @staticmethod   
    def set(id, token):
        HabiTokenMeta.INSTANCES[id] = token
    
    @staticmethod
    def set_root(token):
        HabiTokenMeta.ROOT = token
    
    @staticmethod
    def get_root() -> 'HabiToken':
        return HabiTokenMeta.ROOT

    @staticmethod
    def acquire_token(use_root : bool = False, dig_var :bool = False, throw_on_missing : bool = False, dig_deep:bool = False) -> 'HabiToken':
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                token = None
                
                if use_root and HabiTokenMeta.ROOT is not None:
                    token = HabiTokenMeta.ROOT

                # check if token is already set
                elif token is None and "token" in kwargs and kwargs["token"] is not None:
                    token = kwargs.pop("token", None)

                elif (
                    token is None 
                    and (userId := caller_getattr("userId")) is not None
                    and (token := HabiTokenMeta.get(userId)) is not None
                ):
                    pass
                elif (token:=caller_getattr("token", default=None, deep=dig_deep)) is not None:
                    pass
                
                # finally
                if token is None:
                    logging.warning("No token found")
                if token is None and throw_on_missing:
                    raise HabiMissingTokenException("No token found")

                # parse token
                if isinstance(token,dict):
                    pass
                elif hasattr(token, "headers"):
                    token = token.headers
                
                return func(*args, token=token, **kwargs)

            return wrapper
        return decorator



               



@dataclass(frozen=True)
class HabiToken:
    user_id : str
    api_token : str
    app_id : str = None 

    def __post_init__(self):
        if self.app_id is None:
            object.__setattr__(self, "app_id", self.user_id + "_habil")

    @staticmethod
    def get_root() -> 'HabiToken':
        return HabiTokenMeta.ROOT

    def set_root(self) -> None:
        HabiTokenMeta.set_root(self)

    @property
    def headers(self) -> dict:
        return {
            'x-api-user': self.user_id,
            'x-api-key': self.api_token,
            'x-client': self.app_id
        }

    @classmethod
    def login(cls, username : str, password : str, appid : str=None, set_root : bool = False) -> 'HabiToken':
        res = habil_case.user.login(username=username, password=password, appid=appid)
        if res.fail:
            raise HabiRequestException(res)
        token = HabiToken.create(
            user_id=res.id,
            api_token=res.apiToken,
            app_id=appid,
            set_root=set_root
        )
        return token
    
    @classmethod
    def create(cls, user_id : str, api_token : str, app_id : str=None, set_root : bool = False) -> 'HabiToken':
        token = cls(user_id=user_id, api_token=api_token, app_id=app_id)
        if set_root:
            token.set_root()
        return token

    @classmethod
    def from_dict(cls, data : dict, set_root : bool = False) -> 'HabiToken':
        return cls.create(
            user_id=data.get('user_id', None),
            api_token=data.get('api_token', None),
            app_id=data.get('app_id', None),
            set_root=set_root
        )

    @classmethod
    def from_json(cls, jsonpath : str, set_root : bool = False) -> 'HabiToken':
        data = {}
        with open(jsonpath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data=data, set_root=set_root)


def acquire_(glob :bool = True, dig:bool = True, dig_deep:bool = False, throw : bool = False) -> callable:
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
                raise HabiMissingTokenException("token is required [HabiTokenMeta]")

            return func(*args, **kwargs)
                
        return wrapper
    return decorator
