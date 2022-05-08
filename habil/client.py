from dataclasses import dataclass
import dataclasses
import typing
from habil_base.exceptions import HabiMissingTokenException
from habil_base.habiToken import HabiToken
from habil.tasking import HabiTask
from habil_utils import FrozenClass

class Client(FrozenClass):
    TASK = 0
    #TAG = 1

    def __init__(self, token : typing.Union[HabiToken, dict] = None):
        if token is None:
            token = HabiToken.get_global()
        
        if token is None:
            raise HabiMissingTokenException("No token found")

        self.token : HabiToken = token
        self._freeze()

    @property
    def tasks(self):
        return HabiTask.get_all(token=self.token)
    
    @property
    def character(self):
        raise NotImplementedError

    def get(self, category : int, id : str):
        if category == self.TASK:
            return HabiTask.get(token=self.token, taskId=id)

    
    def create(self, category : int, **kwargs):
        raise NotImplementedError