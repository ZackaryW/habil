from dataclasses import dataclass
import typing
import requests
from habil_map.habiMapAttr import HabiMapReturnParam

@dataclass(frozen=True, init=False)
class HabiMapResponse:
    x_raw : requests.Response
    x_is_json : bool
    x_has_data : bool
    x_data : typing.Dict = None
    x_is_list : bool = False
    x_success : bool = None

    def __init__(self, 
        x_raw : typing.Union[requests.Response, dict],
        x_is_json : bool = False,
        x_has_data : bool = False, 
        **kwargs

    ) -> None:
        object.__setattr__(self, "x_raw", x_raw)
        object.__setattr__(self, "x_is_json", x_is_json)
        object.__setattr__(self, "x_has_data", x_has_data)
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)

    @property
    def success(self) -> bool:
        return self.x_success

    @classmethod
    def parse(cls, raw_response : requests.Response,ret_params : dict,  extract_data : bool = True, only_in_model : bool = True) -> 'HabiMapResponse':
        #
        if not isinstance(raw_response, requests.Response):
            raise TypeError("raw_response must be a requests.Response")
        #
        try:
            json_data = raw_response.json()
            is_json = True
        except:
            return HabiMapResponse(x_raw=raw_response)
        #
        if "data" not in json_data:
            return HabiMapResponse(
                x_raw=raw_response,
                x_is_json=True,
            )
        #
        if not isinstance(ret_params, dict):
            ret_params = {}

        # 
        if not extract_data:
            return HabiMapResponse(
                x_raw=raw_response,
                x_is_json=True,
                x_has_data=True,
                x_success=json_data.get("success", None),
            )
    
        #
        data_params : dict = json_data["data"]

        if isinstance(data_params, list):
            return HabiMapResponse(
                x_raw=raw_response,
                x_is_json=True,
                x_has_data=True,
                x_is_list=True,
                x_data=data_params,
                x_success=json_data.get("success", None),
            )


        if only_in_model:
            data_params = {k: v for k, v in data_params.items() if k in ret_params}
                
        kwargs = {}
        for key, val in data_params.items():
            ret : HabiMapReturnParam = ret_params[key]
            val = ret.validate(val)
            kwargs[key] = val       
            
        return cls(
            x_raw = raw_response,
            x_data = json_data.get("data", None),
            x_is_json = is_json,
            x_success=json_data.get("success", None),
            **kwargs
        )