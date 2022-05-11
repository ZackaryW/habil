from dataclasses import dataclass
from typing import FrozenSet
import habil.tasking as tasking
from habil_base.exceptions import HabiRequestException
from habil_base.habiToken import HabiTokenMeta
import habil_case

@dataclass(frozen=True)
class HabiSubTask:
    userId : str
    taskId : str
    text : str
    id : str
    completed : bool

    def __repr__(self) -> str:
        return "{} [{}]".format(self.text, self.completed)

    @HabiTokenMeta.acquire_token()
    def complete(self, token=None) -> 'HabiSubTask':
        """
        complete checklist item\n

        Return: \n
        `AHabiTask <habil.elements.AHabiTask>`
        """
        res = habil_case.task.score_a_checklist_item(headers=token, taskId=self.taskId, checklistId=self.id)
        if res.fail:
            raise HabiRequestException(res)
        return tasking.HabiTasking._from_res(res, token=token)

    @HabiTokenMeta.acquire_token()
    def remove(self, token=None) -> 'HabiSubTask':
        """
        remove checklist item\n

        Return: \n
        `AHabiTask <habil.elements.AHabiTask>`
        """
        
        res = habil_case.task.delete_a_checklist_item_from_task(headers=token, taskId=self.taskId, checklistId=self.id)
        if res.fail:
            raise HabiRequestException(res)
        return tasking.HabiTasking._from_res(res, token=token)

    @HabiTokenMeta.acquire_token()
    def update(self, text: str = None,completed :bool=None, token=None) -> 'HabiSubTask':
        """
        update checklist item\n

        Return: \n
        `AHabiTask <habil.elements.AHabiTask>`
        """
        
        params = {}
        if text is not None and isinstance(text, str):
            params["text"] = text
        if completed is not None and isinstance(completed, bool):
            params["completed"] = completed

        res = habil_case.task.update_a_checklist_item(
            headers=token, 
            taskId=self.taskId, 
            itemId=self.id, 
            **params
        )

        if res.fail:
            raise HabiRequestException(res)

        return tasking.HabiTasking._from_res(res, token=token)