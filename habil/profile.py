from dataclasses import dataclass
import uuid
from habil_base.habiToken import token_required
from habil_base.habiXItem import HabiXItem
import habil_case
from habil_base.exceptions import HabiRequestException
@dataclass(frozen=True)
class HabiStatBox(HabiXItem):
    job : str
    lvl : int
    exp : int
    hp : int
    mp : int
    gold : int
    str : int
    con : int
    per : int
    int : int

    @classmethod
    @token_required()
    def get(cls, token=None):
        res = habil_case.user.get_user_profile_stats(headers=token)
        if res.fail:
            raise HabiRequestException(res)
        token : dict
        return cls.from_dict(**res.repo, _raw_=res, id=token.get("x-api-user"))

@dataclass(frozen=True)
class HabiProfile(HabiXItem):
    stats : HabiStatBox

    @classmethod
    @token_required()
    def get(cls, token=None):
        res = habil_case.user.get_user_profile(headers=token)
        if res.fail:
            raise HabiRequestException(res)
        stats = HabiStatBox.from_dict(**res.repo.get("stats"), _raw_=res, id=token.get("x-api-user"))
        return cls.from_dict(_raw_=res, id=token.get("x-api-user"), stats=stats)

    
