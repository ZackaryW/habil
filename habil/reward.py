from dataclasses import dataclass
from habil.__task__ import AHabiTask

@dataclass(frozen=True)
class HabiReward(AHabiTask):
    _type = "reward"