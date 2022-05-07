from dataclasses import dataclass
from habil_base.habiUItem import HabiUItem


@dataclass(frozen=True)
class AHabiTask(HabiUItem):
    createdAt : str
    updatedAt : str
    text : str