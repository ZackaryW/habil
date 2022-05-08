from dataclasses import dataclass
from habil_base.habiUItem import HabiUItem
import habil_case
from habil_base import token_required

@dataclass(frozen=True)
class AHabiTask(HabiUItem):
    createdAt : str
    updatedAt : str
    text : str

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.text)

    def __str__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id)

    @token_required
    def update(self, token=None,**kwargs)-> 'AHabiTask':
        res = habil_case.task.update_a_task(headers=token, taskId=self.id, **kwargs)
        if not res.success:
            raise Exception(res.x_raw)
        created_obj = self.from_dict(res.x_data)
        return created_obj
