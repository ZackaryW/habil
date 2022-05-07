
from dataclasses import dataclass
from habil_map.habiMapAttr import HabiMapAttr, HabiMapPathParam, HabiMapBodyParam, HabiMapReturnParam
import typing
import requests
from string import Formatter
from habil_map.habiMapResponse import HabiMapResponse

@dataclass(frozen=True, init=False)
class HabiMapCase:
    url : str
    
    path_params : typing.Dict[str, HabiMapAttr]
    body_params : typing.Dict[str,HabiMapAttr]
    ret_params : typing.Dict[str,HabiMapAttr]

    token_required : bool = True
    request_method : typing.Callable = requests.get

    def __init__(self, url, request_method, *args, token_required: bool = True) -> None:
        
        if not isinstance(token_required, bool):
            raise TypeError("token_required must be a boolean")
        object.__setattr__(self, "token_required", token_required)

        if not isinstance(url, str):
            raise TypeError("url must be a string")
        object.__setattr__(self, "url", url)

        if not isinstance(request_method, typing.Callable):
            raise TypeError("request_method must be a callable")
        object.__setattr__(self, "request_method", request_method)


        object.__setattr__(self, "path_params", {})
        object.__setattr__(self, "body_params", {})
        object.__setattr__(self, "ret_params", {})
        
        # parse
        for arg in args:
            if not isinstance(arg, HabiMapAttr):
                raise TypeError("args must be a HabiMapAttr")

                raise ValueError("arg name is not unique")

            if isinstance(arg, HabiMapPathParam):
                self.path_params[arg.name] = arg
            
            elif isinstance(arg, HabiMapBodyParam):
                self.body_params[arg.name] = arg

            elif isinstance(arg, HabiMapReturnParam):
                self.ret_params[arg.name] = arg


    def _parse_url(self, **kwargs):
        # read url and get str {}
        url = self.url
        url_vars = [i[1] for i in Formatter().parse(url) if i[1] is not None]
        kwargs = {k:v for k,v in kwargs.items() if k in url_vars}
        url = url.format(**kwargs)
        return url

    def _parse_vars(self,
        **kwargs
    ):
        # init checks
        if len(kwargs) == 0:
            return None, None

        path = {}
        body = {}
        
        # parse
        for k, v in kwargs.items():
            if k in self.path_params:
                path[k] = self.path_params[k].validate(v)
        
            if k in self.body_params:
                body[k] = self.body_params[k].validate(v)

        # check missing
        for k, v in self.path_params.items():
            v : HabiMapPathParam
            if v.optional:
                continue
            if k not in path and v.default is None:
                raise ValueError(f"{k} is required")

            path[k] = v.default

        for k, v in self.body_params.items():
            v : HabiMapBodyParam
            if v.optional:
                continue
            if k not in body and v.default is None:
                raise ValueError(f"{k} is required")
            
            body[k] = v.default

        return path, body

    def request(
        self,
        headers: typing.Dict[str, str] = None,
        extract_data : bool = True,
        only_in_model: bool = True,
        **kwargs
    ):
        path, body = self._parse_vars(**kwargs)
        url = self._parse_url(**kwargs)

        if self.token_required and headers is None:
            raise ValueError("token is required")

        kwargs = {
            "url" : url,
            "params" : path,
            "json" : body,
        }

        if self.token_required:
            kwargs["headers"] = headers


        res = self.request_method(**kwargs)
        return HabiMapResponse.parse(res, self.ret_params, extract_data, only_in_model)
    

    @classmethod
    def get_case(cls, url, *args, token_required: bool = True) -> 'HabiMapCase':
        return cls(url, requests.get, *args, token_required=token_required)
    
    @classmethod
    def post_case(cls, url, *args, token_required: bool = True) -> 'HabiMapCase':
        return cls(url, requests.post, *args, token_required=token_required)

    @classmethod
    def put_case(cls, url, *args, token_required: bool = True) -> 'HabiMapCase':
        return cls(url, requests.put, *args, token_required=token_required)

    @classmethod
    def delete_case(cls, url, *args, token_required: bool = True) -> 'HabiMapCase':
        return cls(url, requests.delete, *args, token_required=token_required)