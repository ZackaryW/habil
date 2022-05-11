from dataclasses import dataclass
from habil.elements import AHabiTask
from habil_base.habiToken import HabiTokenMeta

@dataclass(frozen=True)
class HabiHabit(AHabiTask):
    up : bool
    down : bool
    _type = "habit"

    @HabiTokenMeta.acquire_token()
    def good_habit(self,flag:bool = True, token=None):
        return self.update(token=token,up=flag, caller_func="habil.habit.HabiHabit.good_habit")

    @HabiTokenMeta.acquire_token()
    def bad_habit(self,flag:bool = True, token=None):
        return self.update(token=token,up=flag, caller_func="habil.habit.HabiHabit.bad_habit")

    @HabiTokenMeta.acquire_token()
    def score_good(self,token=None):
        return self.score_task(score=True, token=token, caller_func="habil.habit.HabiHabit.score_good")

    @HabiTokenMeta.acquire_token()
    def score_bad(self,token=None):
        return self.score_task(score=False, token=token, caller_func="habil.habit.HabiHabit.score_bad")
