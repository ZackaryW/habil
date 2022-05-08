from dataclasses import dataclass
import typing
import requests
from habil_map.habiMapAttr import HabiMapReturnParam

@dataclass(frozen=True, init=False)
class HabiMapResponse:
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
        object.__setattr__(self, "raw", raw)
        object.__setattr__(self, "reason", raw.reason)
        object.__setattr__(self, "text", raw.text)
        object.__setattr__(self, "is_dict", False)
        object.__setattr__(self, "has_data", False)
        object.__setattr__(self, "success", False)
        # status code
        object.__setattr__(self, "status_code", raw.status_code)

        try:
            json_data = raw.json()
            object.__setattr__(self, "json_data", json_data.get("data", None))
            object.__setattr__(self, "is_json", True)
            if self.json_data is None:
                return
            object.__setattr__(self, "has_data", True)
            
        except:
            object.__setattr__(self, "json_data", None)
            object.__setattr__(self, "is_json", False)
            return

        if not self.is_json:
            return
        
        # check success
        if "success" in json_data and isinstance(json_data["success"], bool) and json_data["success"]:
            object.__setattr__(self, "success", True)

        # check type
        if isinstance(self.json_data, dict):
            object.__setattr__(self, "is_dict", True)

        if ret_params is None or not self.is_dict or len(ret_params) == 0:
            return

        if not extract_data:
            return

        if only_in_model:
            data_params = {k: v for k, v in self.json_data.items() if k in ret_params}
                
        for key, val in data_params.items():
            ret : HabiMapReturnParam = ret_params[key]
            val = ret.validate(val)
            object.__setattr__(self, key, val)

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