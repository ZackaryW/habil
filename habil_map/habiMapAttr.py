
from dataclasses import dataclass
import typing

@dataclass(frozen=True)
class HabiMapAttr:
    name : str
    xtype : typing.Type = None
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HabiMapAttr):
            return False
        return self.name == __o.name

    def validate(self, value):
        if self.xtype is not None and not isinstance(value, self.xtype):
            value = self.xtype(value)

        return value

@dataclass(frozen=True)
class HabiMapSendParam(HabiMapAttr):
    optional : bool = False
    xrange : typing.Iterable = None
    xmin : int = None
    xmax : int = None
    default : typing.Any = None
    
    def validate(self, value):
        value = super().validate(value)
        if self.xrange is not None and value not in self.xrange:
            raise ValueError(f"{value} is not in {self.xrange}")

        if self.xmin is not None and value < self.xmin:
            raise ValueError(f"{value} is less than {self.xmin}")

        if self.xmax is not None and value > self.xmax:
            raise ValueError(f"{value} is greater than {self.xmax}")

        return value

@dataclass(frozen=True)
class HabiMapPathParam(HabiMapSendParam):
    pass

@dataclass(frozen=True)
class HabiMapBodyParam(HabiMapSendParam):
    pass

@dataclass(frozen=True)
class HabiMapReturnParam(HabiMapAttr):
    func : typing.Callable = None

    def validate(self, value):
        value = super().validate(value)
        if self.func is None:
            return value

        if not callable(self.func): 
            raise TypeError("func must be a callable")

        res = self.func(value)
        if isinstance(res, bool) and not res:
            raise ValueError(f"{value} is not valid")
        elif not isinstance(res, bool):
            return value

        return res

