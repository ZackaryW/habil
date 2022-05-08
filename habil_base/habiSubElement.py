from dataclasses import dataclass
from habil_base.habiUItem import HabiUItem

@dataclass(frozen=True)
class HabiSubElement(HabiUItem):

    @classmethod
    def unpack(cls, data: dict) -> 'HabiSubElement':
        pass

    def pack(self) -> dict:
        pass
