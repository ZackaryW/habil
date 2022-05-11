from dataclasses import dataclass
from typing import FrozenSet
from habil_utils import FrozenClass
@dataclass(frozen=True)
class HabiSubTask:
    userId : str
    text : str
    id : str
    completed : bool

    def __repr__(self) -> str:
        return "{} [{}]".format(self.text, self.completed)
