from dataclasses import dataclass
import typing
import requests
from habil_map.habiMapAttr import HabiMapReturnParam
from habil_utils import FrozenClass

@dataclass(init=False)
class HabiMapResponse(FrozenClass):
    url : str
    is_json : bool
    json_data : typing.Optional[dict]
    is_dict : bool
    has_data : bool = False
    success : bool = False
    status_code : int = None
    
    def __init__(self, 
        raw : requests.Response,
        ret_params : typing.Dict[str, HabiMapReturnParam] = None,
        only_in_model : bool = True,
        extract_data : bool = True,
    ) -> None:
        self.raw = raw
        self.reason = raw.reason
        self.status_code = raw.status_code
        self.success = False
        self.is_dict = None
        self.is_json = False
        self.has_data = False

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

        if only_in_model:
            data_params = {k: v for k, v in self.json_data.items() if k in ret_params}
                
        for key, val in data_params.items():
            ret : HabiMapReturnParam = ret_params[key]
            val = ret.validate(val)
            object.__setattr__(self, key, val)

        return self._freeze()

    @property
    def is_list(self):
        return not self.is_dict

    @property
    def fail(self):
        return not self.success

    @property
    def data(self):
        return self.json_data

    @classmethod
    def parse(cls, raw_response : requests.Response,ret_params : dict,  extract_data : bool = True, only_in_model : bool = True) -> 'HabiMapResponse':
        return cls(raw_response, ret_params, extract_data, only_in_model)