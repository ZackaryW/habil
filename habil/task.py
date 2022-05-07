import typing
from habil.daily import HabiDaily
from habil.habit import HabiHabit
from habil.reward import HabiReward
from habil.todo import HabiTodo
from habil_base.habiToken import token_required
class HabiTask:
    @token_required
    @classmethod
    def get(cls, id : str, token=None) -> typing.Union[HabiDaily, HabiHabit, HabiReward, HabiTodo ,None]:
        pass