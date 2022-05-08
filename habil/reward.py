from dataclasses import dataclass
from habil.__task__ import AHabiTask
from habil_base.habiToken import token_required
import habil_case

@dataclass(frozen=True)
class HabiReward(AHabiTask):
    _type = "reward"

    @token_required()
    def redeem(self,token=None):
        return self.score_task(score=True, token=token, caller_func="habil.reward.HabiReward.redeem")
