from dataclasses import dataclass
from habil.elements import CompletableTask

@dataclass(frozen=True)
class HabiDaily(CompletableTask):
    _type = "daily"
