import inspect
import typing
from habil_base.habiToken import token_required
from habil_utils import FrozenClass, get_simple_caller_name, get_caller_class
from habil import HabiDaily
import re

class CounterDaily(FrozenClass):
    def __init__(self, id: str, text: str, max:int, current: int=0) -> None:
        sig  =get_simple_caller_name()
        if sig != "overload":
            raise ValueError("CounterDaily must be called with overload")
        if get_caller_class() != CounterDaily:
            raise ValueError("CounterDaily must be called by a classmethod of CounterDaily")

        self.id = id
        self.text = text
        self.max = max
        self.current = current

    @token_required()
    def complete(self, count: int=1, token=None) -> None:
        self.current += count
        done = False
        if self.current >= self.max:
            self.current = self.max
            done = True
        
        daily : HabiDaily = self.daily()
        if done:
            daily = daily.update(text=self.text, token=token, caller_func="habil_ext.counterDaily.CounterDaily.complete")
            daily.score_task(score=True, token=token, caller_func="habil_ext.counterDaily.CounterDaily.complete")
            return

        daily = daily.update(text=f"{self.text} [{self.current}/{self.max}]", token=token, caller_func="habil_ext.counterDaily.CounterDaily.complete")
        return

    @token_required()
    def daily(self, token=None) -> HabiDaily:
        return HabiDaily.get(id=self.id, token=token)

    @classmethod
    @token_required()
    def overload(cls, daily: HabiDaily, reset:bool = False, max:int =None, current : int = 0, token= None) -> typing.Union["CounterDaily", HabiDaily]:
        if not isinstance(daily, HabiDaily):
            raise ValueError("daily must be a HabiDaily")

        if daily.expired:
            raise ValueError("daily must not be expired")

        # pattern <text> [<int>/<int>]
        pattern = r"(?P<text>.*?)\s*\[(?P<current>\d+)?/(?P<max>\d+)?\]\s*"
        regex = re.compile(pattern)
        match = regex.search(daily.text)
        if not match and not reset:
            return daily
        
        # making new
        if not match and reset:
            new_text = daily.text

            if daily.text.endswith("]"):
                # reverse iter
                new_text = ""
                for i in range(0, len(daily.text)):
                    if daily.text[i] == "[":
                        break
                    new_text = new_text + daily.text[i]

            daily.update(
                text=f"{new_text} [{current}/{max}]", 
                token=token, 
                caller_func="habil_ext.counterDaily.CounterDaily.overload"
            )
            return cls(
                id=daily.id,
                text=daily.text,
                max=max,
                current=current
            )

        text = match.group("text")
        max = int(match.group("max"))
        current = int(match.group("current"))

        return cls(
            id=daily.id,
            text=text,
            max=max,
            current=current
        )

