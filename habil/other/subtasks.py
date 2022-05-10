from dataclasses import dataclass
from habil_utils import FrozenClass
@dataclass(frozen=True)
class HabiSubTask:
    _id : str
    text : str
    id : str
    completed : bool

    def __repr__(self) -> str:
        return "({} - {})[{}]".format(self.__class__.__name__, self.text, self.completed)

    

@dataclass(init=False)
class HabiSubTasks(FrozenClass):
    def __init__(self, id : str, data : list) -> None:
        self._id = id
        subtasks =[]
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("SubTasks data is not a list of dicts")
            subtasks.append(HabiSubTask(**item, _id=self._id))
        
        self._subtasks = tuple(subtasks)

        self._freeze()

    def _gen_repr(self) -> str:
        return "\n".join([repr(t) for t in self._subtasks])

    def _freeze(self):
        self._repr = self._gen_repr()
        return super()._freeze()
    
    #ANCHOR overloads
    def __repr__(self) -> str:
        return self._repr

    def __iter__(self) -> iter:
        return iter(self._subtasks)

    def __len__(self) -> int:
        return len(self._subtasks)

    def __getitem__(self, key : int) -> HabiSubTask:
        for i, t in enumerate(self._subtasks):
            if i == key:
                return t
            if key == t.text:
                return t
        raise KeyError(key)
