from dataclasses import dataclass
from habil.elements import AHabiTask
from habil_base.habiToken import HabiTokenMeta

@dataclass(frozen=True)
class HabiReward(AHabiTask):
    _type = "reward"

    @HabiTokenMeta.acquire_token()
    def redeem(self,token=None):
        return self.score_task(score=True, token=token, caller_func="habil.reward.HabiReward.redeem")
