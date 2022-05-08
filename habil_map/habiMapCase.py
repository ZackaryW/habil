
from dataclasses import dataclass
import datetime
from habil_base.exceptions import HabiRequestRateLimited
from habil_map.habiMapAttr import HabiMapAttr, HabiMapPathParam, HabiMapBodyParam, HabiMapReturnParam
import typing
import requests
from string import Formatter
from habil_map.habiMapResponse import HabiMapResponse

class HabiMapMeta:
    RATE_LIMIT = None
    MIN_TRIGGER_RATE_LIMIT = 1
    RATE_LIMIT_REMAINING = None
    LOGS = {}
    MAX_HOLD_LOGS = 10

    @classmethod
    def parse_rate_limit_state(cls, res: requests.Response):
        chances_remain = res.headers.get("X-RateLimit-Remaining", None)
        if chances_remain is None:
            return
        chances_remain = int(chances_remain)
        cls.RATE_LIMIT_REMAINING = chances_remain

        reset_time = res.headers.get("X-RateLimit-Reset", None)
        # parse string into datetime object
        if reset_time is not None:
            # Sat May 07 2022 23:29:36 GMT+0000 to strftime format
            try:
                reset_time = datetime.datetime.strptime(reset_time, "%a %b %d %Y %H:%M:%S %Z")
            except ValueError as v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    reset_time = reset_time[:-(len(v.args[0]) - 26)]
                    reset_time = datetime.datetime.strptime(reset_time, "%a %b %d %Y %H:%M:%S %Z")
                else:
                    raise v
        if chances_remain <= cls.MIN_TRIGGER_RATE_LIMIT:
            cls.RATE_LIMIT = reset_time

    @classmethod
    def check_rate_limit(cls):
        if cls.RATE_LIMIT is None:
            return
        gmt_now = datetime.datetime.utcnow()
        if gmt_now < cls.RATE_LIMIT:
            raise HabiRequestRateLimited("Rate Limited, wait until {}".format(cls.RATE_LIMIT))
        
    @classmethod
    def _log(cls, text, url: str):
        cls.LOGS[url] = text
        while len(cls.LOGS) > cls.MAX_HOLD_LOGS:
            cls.LOGS.popitem(last=False)

    @classmethod
    def get_log(cls, url: str):
        return cls.LOGS.get(url, None)
    
    @classmethod
    def get_last_log(cls):
        if len(cls.LOGS) == 0:
            return None
        # get last log
        return cls.LOGS.get(cls.LOGS.keys()[-1], None)

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
        if len(path) == 0:
            path = None
        if len(body) == 0:
            body = None

        return path, body

    def __call__(self, headers: typing.Dict[str, str] = None,
        extract_data : bool = True,
        only_in_model: bool = True,
        **kwargs) -> HabiMapResponse:
        return self.request(headers, extract_data, only_in_model, **kwargs)

    def request(
        self,
        headers: typing.Dict[str, str] = None,
        extract_data : bool = True,
        only_in_model: bool = True,
        **kwargs
    ) -> HabiMapResponse:
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

        HabiMapMeta.check_rate_limit()
        res : requests.Response = self.request_method(**kwargs)
        HabiMapMeta.parse_rate_limit_state(res)
        try:
            res.json()
        except:
            # if not jsonable, a log is written
            HabiMapMeta._log(res.text, url)

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