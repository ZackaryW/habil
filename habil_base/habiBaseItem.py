from dataclasses import dataclass
import dataclasses
import uuid


@dataclass(frozen=True, init=False)
class HabiBaseItem:
    """
    generic class for all habil items
    """
    _inherit_key : str

    def __init__(self, _inherit_key : str =None) -> None:
        if _inherit_key is None:
            _inherit_key = str(uuid.uuid4())
        object.__setattr__(self, "_inherit_key", _inherit_key)

    