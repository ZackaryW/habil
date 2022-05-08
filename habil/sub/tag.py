from dataclasses import dataclass
from datetime import datetime
from habil_base.exceptions import HabiRequestException
from habil.sub import HabiSubElement
from habil_base.habiToken import token_required
import habil_case

class HabiTagMeta:
    LAST_PULL = None
    PULL_INTERVAL = 300

    @classmethod
    def set_timer(cls):
        cls.LAST_PULL = datetime.utcnow()

    @classmethod
    def is_time_to_pull(cls):
        if cls.LAST_PULL is None:
            return True
        return datetime.utcnow() - cls.LAST_PULL > datetime.timedelta(seconds=cls.PULL_INTERVAL)

@dataclass(frozen=True)
class HabiTag(HabiSubElement):

    @classmethod
    @token_required()
    def get(cls, id: str, token=None, force_pull : bool = False) -> 'HabiSubElement':
        if HabiTagMeta.is_time_to_pull():
            force_pull = True

        if cls not in cls._instances:
            cls._instances[cls] = {}
            
        if id in cls._instances[cls] and not force_pull:
            return cls._instances[cls][id]
        
        res = habil_case.tag.get_a_users_tags(
            headers=token,
            tagId=id
        )

        if not res.success:
            raise HabiRequestException(res)

        for element in res.data:
            eid = element.get("id")
            if eid not in cls._instances[cls]:
                cls._instances[cls][eid] = cls.unpack(element)
            else:
                instance : HabiSubElement = cls._instances[cls][eid]
                instance._local_update(**element)

        HabiTagMeta.set_timer()
        return cls._instances[cls][id]
