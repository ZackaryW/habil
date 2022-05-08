import typing
from habil.daily import HabiDaily
from habil.habit import HabiHabit
from habil.reward import HabiReward
from habil.todo import HabiTodo
from habil_base.habiToken import token_required
import habil_case
from habil_map.habiMapResponse import HabiMapResponse

class HabiTask:
    @classmethod
    def _from_res(cls, data: HabiMapResponse) -> 'HabiTask':
        if isinstance(data, HabiMapResponse):
            method = "from_res"
            xtype = data.data.get("type",None)
        elif isinstance(data, dict):
            method = "from_dict"
            xtype = data.get("type",None)
        else:
            raise TypeError("data must be HabiMapResponse or dict")

        if xtype is None:
            raise ValueError("type is missing")
        if xtype == "daily":
            return getattr(HabiDaily, method)(data)
        elif xtype == "habit":
            return getattr(HabiHabit, method)(data)
        elif xtype == "reward":
            return getattr(HabiReward, method)(data)
        elif xtype == "todo":
            return getattr(HabiTodo, method)(data)
        else:
            raise ValueError(f"unknown type: {xtype}")

    @classmethod
    @token_required()
    def get(cls, id : str, token=None) -> typing.Union[HabiDaily, HabiHabit, HabiReward, HabiTodo ,None]:
        task_res = habil_case.task.get_a_task(headers=token, taskId=id)
        if not task_res.success:
            return None
        return cls._from_res(task_res)

    @classmethod
    @token_required()
    def get_all(cls, token=None) -> typing.List[typing.Union[HabiDaily, HabiHabit, HabiReward, HabiTodo]]:
        tasks_res = habil_case.task.get_users_tasks(headers=token)
        if not tasks_res.success:
            return []

        tasks_raw = tasks_res.json_data
        if not isinstance(tasks_raw, list):
            raise TypeError("tasks_raw must be a list, but is {}".format(type(tasks_raw)))
        
        tasks = []
        for task_raw in tasks_raw:
            task = cls._from_res(task_raw)
            if task is not None:
                tasks.append(task)
        return tasks