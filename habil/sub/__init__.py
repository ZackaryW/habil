from abc import abstractmethod
from dataclasses import dataclass
from types import MappingProxyType
import typing
from habil_base.habiUItem import HabiUItem

@dataclass(frozen=True)
class HabiSubElement(HabiUItem):
    name : str

    @classmethod
    def unpack(cls, data: dict) -> 'HabiSubElement':
        parsed_data = {k:v for k, v in data.items() if k in cls.fields()}
        return cls(**parsed_data,_raw_=data)

    @abstractmethod
    def pack(self) -> dict:
        pass

    def _local_update(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.__class__.fields():
                object.__setattr__(self, k, v)

    @abstractmethod
    def update(self) -> 'HabiSubElement':
        pass

    @classmethod
    def get(cls, id: str) -> 'HabiSubElement':
        pass

    @classmethod
    def get_all(cls) -> typing.List['HabiSubElement']:
        if cls not in cls._instances:
            cls._instances[cls] = {}
        
        return MappingProxyType(cls._instances[cls])
