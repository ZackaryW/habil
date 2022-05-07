from dataclasses import dataclass
import json 

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
        pass
    
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

def token_required(func):
    def wrapper(*args, **kwargs):
        global _SINGLETON_INSTANCE
        if "token" not in kwargs and _SINGLETON_INSTANCE is None:
            raise ValueError("Token is required")
        if "token" not in kwargs:
            kwargs["token"] = _SINGLETON_INSTANCE.headers
        token = kwargs["token"]
        if isinstance(token, HabiToken):
            kwargs["token"] = token.headers
        return func(*args, **kwargs)
    return wrapper