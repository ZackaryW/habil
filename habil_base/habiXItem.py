from dataclasses import dataclass
import uuid
from habil_base.habiUItem import HabiUItem

@dataclass(frozen=True)
class HabiXItem(HabiUItem):
    uid : str

    @classmethod
    def from_dict(cls, **data_dict):
        uid = uuid.uuid4()
        return super().from_dict(**data_dict, uid=uid)

    @classmethod
    def from_res(cls, res):
        uid = uuid.uuid4()
        return super().from_res(res, uid=uid)

    def __eq__(self, other):
        if not isinstance(other, HabiXItem):
            return False

        return self.uid == other.uid