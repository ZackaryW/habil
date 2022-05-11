import typing
from habil.elements.daily import HabiDaily
from habil.elements.habit import HabiHabit
from habil.elements.reward import HabiReward
from habil.elements.todo import HabiTodo
from habil_base.habiToken import HabiTokenMeta
import habil_case
from habil_map.habiMapResponse import HabiMapResponse

class HabiTasking:
    @staticmethod
    def _get_type(data):
        

        if (is_dict := isinstance(data, dict)):
            real_type = data.get("type", None)
        elif isinstance(data, HabiMapResponse):
            real_type = data.json_data.get("type", None)
        else:
            real_type = None

        if real_type is None:
            raise ValueError("type is not defined")

        match real_type:
            case "daily":
                return HabiDaily, is_dict
            case "habit":
                return HabiHabit, is_dict
            case "reward":
                return HabiReward, is_dict
            case "todo":
                return HabiTodo, is_dict
            case "dailys":
                return HabiDaily, is_dict
            case "habits":
                return HabiHabit, is_dict
            case "rewards":
                return HabiReward, is_dict
            case "todos":
                return HabiTodo, is_dict

    @classmethod
    def _from_res(cls, data: HabiMapResponse, token=None) -> 'HabiTasking':
        type_, is_dict = cls._get_type(data)
        if is_dict:
            return type_.from_dict(**data)
        else:
            return type_.from_res(data)

    @classmethod
    @HabiTokenMeta.acquire_token()
    def get(cls, id : str, token=None) -> typing.Union[HabiDaily, HabiHabit, HabiReward, HabiTodo ,None]:
        task_res = habil_case.task.get_a_task(headers=token, taskId=id)
        if not task_res.success:
            return None
        return cls._from_res(task_res)

    @classmethod
    @HabiTokenMeta.acquire_token()
    def get_all(cls, token=None) -> typing.List[typing.Union[HabiDaily, HabiHabit, HabiReward, HabiTodo]]:
        tasks_res = habil_case.task.get_users_tasks(headers=token)
        if not tasks_res.success:
            return []

        tasks_raw = tasks_res.json_data
        if not isinstance(tasks_raw, list):
            raise TypeError("tasks_raw must be a list, but is {}".format(type(tasks_raw)))
        
        tasks = []
        for task_raw in tasks_raw:
            task = cls._from_res(task_raw, token=token)
            if task is not None:
                tasks.append(task)
        return tasks