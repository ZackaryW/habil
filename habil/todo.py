from dataclasses import dataclass
from habil.__task__ import CompletableTask

@dataclass(frozen=True)
class HabiTodo(CompletableTask): 
    _type = "todo"