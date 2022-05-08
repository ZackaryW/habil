from dataclasses import dataclass
from habil.elements import CompletableTask

@dataclass(frozen=True)
class HabiTodo(CompletableTask): 
    _type = "todo"