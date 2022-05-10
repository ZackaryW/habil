
from abc import abstractmethod
from dataclasses import dataclass
import dataclasses
from datetime import datetime
import typing

class HabiUMeta(type):
    _instances = {}
    _raw = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}

        if cls not in cls._raw:
            cls._raw[cls] = {}

        id = kwargs.get("id", None)
        raw = kwargs.pop("_raw_", None)
        if id is None:
            raise TypeError("id must be provided")

        if raw is None:
            raise TypeError("_raw_ must be provided")

        cls._instances[cls][id] = super().__call__(*args, **kwargs)
        cls._raw[cls][id] = datetime.now(), raw

        return cls._instances[cls][id]

    def gets(cls, id):
        if cls not in cls._instances:
            raise TypeError("No instances of {}".format(cls))
        if id not in cls._instances[cls]:
            raise TypeError("No instance of {} with id {}".format(cls, id))
        return cls._instances[cls][id]

    def get_raw(cls, item : typing.Union[str, 'HabiUItem'], only_raw=True):
        if cls not in cls._raw:
            raise TypeError("No raw of {}".format(cls))
        if not isinstance(item,str) and hasattr(item, "id"):
            item = item.id

        if item not in cls._raw[cls]:
            raise TypeError("No raw of {} with id {}".format(cls, item))

        if only_raw:
            return cls._raw[cls][item][1]

        return cls._raw[cls][item]

    def exist(cls, id):
        if cls not in cls._instances:
            return False
        if id not in cls._instances[cls]:
            return False
        return True

    def fields(cls):
        fs = dataclasses.fields(cls)
        return [f.name for f in fs]

@dataclass(frozen=True)
class HabiUItem(metaclass=HabiUMeta):
    id : str

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id)

    def __str__(self) -> str:
        return self.__repr__()

    @abstractmethod
    def update(self, **kwargs):
        pass

    # ANCHOR properties

    @property
    def expired(self) -> bool:
        return self.__class__._instances[self.__class__][self.id] is not self

    # ANCHOR Classmethods
    @classmethod
    def from_dict(cls, **data_dict):
        if not isinstance(data_dict, dict):
            raise TypeError("data_dict must be a dict")
        if not data_dict:
            raise TypeError("data_dict must not be empty")
        
        passed_dict = {k: v for k, v in data_dict.items() if k in cls.fields()}
        return cls(**passed_dict, _raw_=data_dict)

    @classmethod
    def from_res(cls, res, **kwargs):
        if not isinstance(res.data, dict):
            raise TypeError("data must be a dict")
        if not res.data:
            raise TypeError("data must not be empty")
        
        kwargs.update(res.data)

        passed_dict = {k: v for k, v in kwargs.items() if k in cls.fields()}
        return cls(**passed_dict, _raw_=res)

    def __eq__(self, other):
        if not isinstance(other, HabiUItem):
            return False
        
        return self is other