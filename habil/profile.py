from dataclasses import dataclass
from habil_base.habiToken import token_required
import habil_case
from habil_base.exceptions import HabiRequestException
@dataclass(frozen=True)
class HabiStatBox:
    job : str
    lvl : int
    exp : int
    hp : int
    mp : int
    gold : int
    str : int
    int : int
    con : int
    per : int

    @classmethod
    @token_required()
    def get(cls, token=None):
        res = habil_case.user.get_user_profile_stats(headers=token)
        if res.fail:
            raise HabiRequestException(res)
        return cls(**res.repo)

class HabiProfile:
    @classmethod
    @token_required()
    def get(cls, token=None):
        raise NotImplementedError