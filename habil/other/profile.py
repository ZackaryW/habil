from dataclasses import dataclass
import logging
import uuid
from habil_base.habiToken import token_required
from habil_base.habiUItem import HabiUItem
import habil_case
from habil_base.exceptions import HabiRequestException
@dataclass(frozen=True)
class HabiStatBox(HabiUItem):
    job : str
    lvl : int
    exp : int
    hp : int
    mp : int
    gold : int
    str : int
    con : int
    per : int
    inte : int

    @classmethod
    @token_required(throw=True)
    def get(cls, token=None):
        res = habil_case.user.get_user_profile_stats(headers=token, caller_func="HabiStatBox.get")
        if res.fail:
            raise HabiRequestException(res)
        token : dict
        return cls.from_dict(**res.repo, id=token.get("x-api-user"))

    @token_required(throw=True)
    def update(self,
        lvl : int = None,
        exp : int = None,
        hp : int = None,
        mp : int = None,
        gold : int = None,
        str : int = None,
        con : int = None,
        per : int = None,
        inte : int = None,
        set :bool = False,
    token=None):
        skip = ("token", "self", "set", "skip","changed")
        changed = {k : v for k, v in locals().items() if (v is not None and k not in skip)}
        if len(changed) == 0:
            logging.warning("No stats to update for user %s", token.get("x-api-user"))
            return None
        if not set:
            changed = {f"stat_{k}" : v + getattr(self, k) for k, v in changed.items()}

        res = habil_case.user.update_user_profile(headers=token, **changed, caller_func="HabiStatBox.update")
        if res.fail:
            raise HabiRequestException(res)

        return self.from_dict(**res.repo.get("stats"), id=token.get("x-api-user"))


@dataclass(frozen=True)
class HabiProfile(HabiUItem):
    stats : HabiStatBox

    @classmethod
    @token_required()
    def get(cls, token=None):
        res = habil_case.user.get_user_profile(headers=token, caller_func="HabiProfile.get")
        if res.fail:
            raise HabiRequestException(res)
        stats = HabiStatBox.from_dict(**res.repo.get("stats"), id=token.get("x-api-user"))
        return cls.from_dict(id=token.get("x-api-user"), stats=stats)

    
