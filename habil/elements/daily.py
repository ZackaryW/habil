from dataclasses import dataclass
from habil.task import CompletableTask

@dataclass(frozen=True)
class HabiDaily(CompletableTask):
    _type = "daily"
