from dataclasses import dataclass
from habil.task import CompletableTask

@dataclass(frozen=True)
class HabiTodo(CompletableTask): 
    _type = "todo"