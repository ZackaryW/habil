from dataclasses import dataclass
import datetime
import typing
import requests
from habil_map.habiMapAttr import HabiMapReturnParam
from habil_utils import FrozenClass

@dataclass(init=False)
class HabiMapResponse(FrozenClass):
    """
    a simple wrapper for requests.Response

    Dataclass Vars:\n
        raw : requests.Response\n
        url : str - called url\n
        reason : str\n
        status_code : int\n
        success : bool\n
        is_dict : bool\n
        is_json : bool\n
        has_data : bool\n
        timestamp : datetime.datetime\n
        request_time : float\n
        raw_data : typing.Any\n
        json_data : typing.Any\n
        repo : typing.Dict[str, typing.Any]\n

    """
    url : str
    is_json : bool
    json_data : typing.Optional[dict]
    is_dict : bool
    timestamp : datetime.datetime
    request_time : float
    has_data : bool = False
    success : bool = False
    status_code : int = None
    
    def __init__(self, 
        caller_func : str,
        raw : requests.Response,
        ret_params : typing.Dict[str, HabiMapReturnParam] = None,
        extract_data : bool = True,
    ) -> None:
        self.caller_func = caller_func
        self.raw = raw
        self.url = raw.url
        self.reason = raw.reason
        self.status_code = raw.status_code
        self.success = False
        self.is_dict = None
        self.is_json = False
        self.has_data = False
        self.timestamp = datetime.datetime.now()
        self.request_time = raw.elapsed.total_seconds()

        try:
            self.raw_data = raw.json()
            self.is_json = True
            self.json_data = self.raw_data.get("data", None)
            if self.json_data is not None:
                self.has_data = True
        except:
            self.raw_data = raw.text
            self.is_json = False
            self.json_data = None
        
        if not self.has_data:
            return self._freeze()

        if "success" in self.raw_data:
            self.success = self.raw_data["success"]

        # check type
        if isinstance(self.json_data, dict):
            self.is_dict = True
        elif isinstance(self.json_data, list):
            self.is_dict = False
        
        if self.is_dict is None:
            return self._freeze()

        if ret_params is None or not self.is_dict or len(ret_params) == 0:
            return self._freeze()

        if not extract_data:
            return self._freeze()
        
        for key, ret in ret_params.items():
            key : str
            ret : HabiMapReturnParam
            val = self._dig(key, self.json_data)
            if val is None:
                continue
            val = ret.validate(val)
            if ret.rename_to is not None:
                key = ret.rename_to

            if not ret.to_repo:
                object.__setattr__(self, key, val)
                continue
            
            self._bury(key, val)

        return self._freeze()
        
    def _freeze(self):
        self._repr = self._gen_repr()
        super()._freeze()

    def _gen_repr(self):
        ret_dict = {k:v for k,v in self.__dict__.items() if not k.startswith("_")}
        ret_dict.pop("raw_data", None)
        ret_dict.pop("raw", None)
        ret_dict.pop("json_data", None)
        ret_dict = "\n".join(f"{k}={v}" for k,v in ret_dict.items())
        return f"{self.__class__.__name__}({ret_dict})"

    def _bury(self, key :str, val):
        if not hasattr(self, "repo"):
                self.repo = {}

        keys = key.split(".")

        if len(keys) == 1:
            self.repo[key] = val
            return

        focus = self.repo

        for k in keys[:-1]:
            if k not in focus:
                focus[k] = {}
            focus = focus[k]

        focus[keys[-1]] = val
            

    def _dig(self, key : str, val) -> typing.Any:
        keys = key.split(".")
        
        for k in keys:
            if isinstance(val, dict):
                xval = val.get(k, None)
            elif isinstance(val, typing.Iterable):
                xval = val[int(k)]
            else:
                xval = getattr(val, k, None)
            
            if xval is None:
                return None
            
            val = xval

        return val

    def __repr__(self):
        return self._repr

    def __str__(self):
        return f"{self.__class__.__name__}({self.url} @ {self.timestamp})"

    @property
    def is_list(self):
        return not self.is_dict

    @property
    def fail(self):
        return not self.success

    @property
    def data(self):
        return self.json_data

    @property
    def unix_timestamp(self):
        return int(self.timestamp.timestamp()*1000)

    @classmethod
    def parse(cls,caller_func:str, raw_response : requests.Response,ret_params : dict,  extract_data : bool = True) -> 'HabiMapResponse':
        return cls(
            caller_func=caller_func,
            raw=raw_response,
            ret_params=ret_params, 
            extract_data=extract_data,
        )