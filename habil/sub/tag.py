from dataclasses import dataclass
from datetime import datetime, timedelta
from types import MappingProxyType
from habil_base.exceptions import HabiLocalNotFoundException, HabiRequestException
from habil.sub import HabiSubElement
from habil_base.habiToken import HabiTokenMeta
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
        return datetime.utcnow() - cls.LAST_PULL > timedelta(seconds=cls.PULL_INTERVAL)

@dataclass(frozen=True)
class HabiTag(HabiSubElement):
    def delete(self) -> None:
        res = habil_case.tag.delete_a_user_tag(self.id)
        if res.fail:
            raise HabiRequestException(res)

        self.__class__.deleteins(self.id)


    @classmethod
    @HabiTokenMeta.acquire_token()
    def create(cls, name:str, token=None):
        res = habil_case.tag.create_new_tag(name=name, headers=token)
        if res.fail:
            raise HabiRequestException(res)
        return cls(
            id=res.id,
            name=res.name
        )

    @classmethod
    @HabiTokenMeta.acquire_token()
    def get(cls, id: str, token=None, force_pull : bool = False) -> 'HabiSubElement':
        if HabiTagMeta.is_time_to_pull():
            force_pull = True

        if force_pull:
            cls.get_all(token=token)
        
        if id not in cls._instances[cls]:
            raise HabiLocalNotFoundException(
                f"Tag with id {id} not found in local cache."
            )
        
        return cls._instances[cls][id]
    

    @classmethod
    @HabiTokenMeta.acquire_token()
    def get_all(cls, token=None, force_pull : bool = True) -> list:
        if HabiTagMeta.is_time_to_pull():
            force_pull = True
        
        if cls not in cls._instances:
            cls._instances[cls] = {}
        
        if not(len(cls._instances[cls]) == 0 or force_pull):
            return MappingProxyType(cls._instances[cls])

        res = habil_case.tag.get_a_users_tags(
            headers=token,
            caller_func="HabiTag.get_all"
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
        return MappingProxyType(cls._instances[cls])