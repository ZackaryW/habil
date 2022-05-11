from dataclasses import dataclass
from habil.other.subtasks import HabiSubTask
from habil.sub.tag import HabiTag
from habil_base.exceptions import HabiRequestException
from habil_base.habiUItem import HabiUItem
import habil_case
from habil_base import HabiTokenMeta
import typing
from habil.other.profile import HabiStatBox

@dataclass(frozen=True)
class AHabiTask(HabiUItem):
    userId : str
    createdAt : str
    updatedAt : str
    text : str
    tags : typing.Tuple[str]
    _type = "task"

    def __post_init__(self):
        tag_objs = []
        for tag in self.tags:
            atag = HabiTag.get(id=tag)
            tag_objs.append(atag)
        object.__setattr__(self, "tags", tuple(tag_objs)) # make immutable

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.text)

    def __str__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.id)


    @classmethod
    @HabiTokenMeta.acquire_token()
    def get(cls, id : str, token=None, **kwargs):
        res = habil_case.task.get_a_task(headers=token, taskId=id, **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        if res.type == cls._type:
            return cls.from_res(res)
        return None

    @HabiTokenMeta.acquire_token()
    def update(self, token=None,**kwargs)-> 'AHabiTask':
        res = habil_case.task.update_a_task(headers=token, taskId=self.id, **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        created_obj = self.from_res(res)
        return created_obj

    @HabiTokenMeta.acquire_token()
    def delete(self, token=None, **kwargs) -> bool:
        res = habil_case.task.delete_a_task(headers=token, taskId=self.id, **kwargs)
        if not res.success:
            raise HabiRequestException(res)

        self.__class__.deleteins(self.id)
        return True

    @HabiTokenMeta.acquire_token()
    def score_task(self,score: bool = True, token=None, **kwargs):
        res = habil_case.task.score_a_task(headers=token, taskId=self.id, direction="up" if score else "down", **kwargs)
        if not res.success:
            raise HabiRequestException(res)
        return self.get(id=self.id, token=token)

    # ANCHOR tag operations
    def has_tag(self,name: str=None, id: str=None) -> bool:
        for tag in self.tags:
            tag : HabiTag
            if tag.name == name or tag.id == id:
                return True
        return False

    @HabiTokenMeta.acquire_token()
    def add_tag(self, tag: HabiTag, token=None) -> 'AHabiTask':
        res = habil_case.task.add_a_tag_to_a_task(headers=token, taskId=self.id, tagId=tag.id)
        if res.fail:
            raise HabiRequestException(res)
        return self.from_res(res)

    @HabiTokenMeta.acquire_token()
    def remove_tag(self, tag: HabiTag, token=None) -> 'AHabiTask':
        res = habil_case.task.delete_a_tag_from_a_task(headers=token, taskId=self.id, tagId=tag.id)
        if res.fail:
            raise HabiRequestException(res)
        return self.from_res(res)


@dataclass(frozen=True)
class CompletableTask(AHabiTask):
    completed : bool
    checklist : typing.Tuple[HabiSubTask]

    def __post_init__(self):
        super().__post_init__()
        checklists = []
        for checklist in self.checklist:
            checklists.append(HabiSubTask(**checklist, userId=self.userId, taskId=self.id))

        object.__setattr__(self, "checklist", tuple(checklists))

    @HabiTokenMeta.acquire_token()
    def complete(self, revert: bool = False, token=None) -> 'CompletableTask':
        if not isinstance(revert, bool):
            raise TypeError("revert must be bool")

        res = habil_case.task.score_a_task(taskId=self.id, direction="up" if not revert else "down")
        if not res.success:
            raise HabiRequestException(res)
        
        statbox = HabiStatBox.from_res(res)
        task = self.__class__.get(id=self.id)
        return task, statbox

    # ANCHOR checklist
    @HabiTokenMeta.acquire_token()
    def add_checklist_item(self, text: str, completed : bool = False, token=None) -> 'CompletableTask':
        res = habil_case.task.add_a_checklist_item_to_task(headers=token, taskId=self.id, text=text, completed=completed)
        if not res.success:
            raise HabiRequestException(res)

        return self.from_res(res)
