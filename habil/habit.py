from dataclasses import dataclass
from habil.__task__ import AHabiTask
from habil_base.habiToken import token_required

@dataclass(frozen=True)
class HabiHabit(AHabiTask):
    up : bool
    down : bool
    _type = "habit"

    @token_required()
    def good_habit(self,flag:bool = True, token=None):
        return self.update(token=token,up=flag)

    @token_required()
    def bad_habit(self,flag:bool = True, token=None):
        return self.update(token=token,up=flag)

    @token_required()
    def score_good(self,token=None):
        return self.score_task(score=True, token=token)

    @token_required()
    def score_bad(self,token=None):
        return self.score_task(score=False, token=token)
