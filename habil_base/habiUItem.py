
from abc import abstractmethod
from dataclasses import dataclass
import dataclasses

class HabiUMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}
        
        id = kwargs.get("id")
        if id is None:
            raise TypeError("id must be provided")

        if id in cls._instances[cls]:
            del cls._instances[cls][id]

        cls._instances[cls][id] = super().__call__(*args, **kwargs)
        return cls._instances[cls][id]

    def get(cls, id):
        if cls not in cls._instances:
            raise TypeError("No instances of {}".format(cls))
        if id not in cls._instances[cls]:
            raise TypeError("No instance of {} with id {}".format(cls, id))
        return cls._instances[cls][id]

    def exist(cls, id):
        if cls not in cls._instances:
            return False
        if id not in cls._instances[cls]:
            return False
        return True

@dataclass(frozen=True)
class HabiUItem(metaclass=HabiUMeta):
    id : str
    _raw : dict

    @abstractmethod
    def update(self, **kwargs):
        vals = {k:v for k,v in kwargs.items() if k in self.fields and k != "id"}
        return vals

    @abstractmethod
    def delete(self):
        pass

    # ANCHOR properties
    @property
    def fields(self):
        fields = dataclasses.fields(self)
        return [f.name for f in fields]

    @property
    def raw_init(self):
        return self._raw.copy()

    @property
    def expired(self) -> bool:
        return self.__class__.exist(self.id) == False

    # ANCHOR Classmethods
    @classmethod
    def from_dict(cls, data_dict: dict):
        if not isinstance(data_dict, dict):
            raise TypeError("data_dict must be a dict")
        if not data_dict:
            raise TypeError("data_dict must not be empty")
        
        data_dict = {k: v for k, v in data_dict.items() if k in cls.fields}
        data_dict["_raw"] = data_dict
        return cls(**data_dict)

    