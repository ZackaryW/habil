from habil_map import Body as _Body
from habil_map import Path as _Path
from habil_map import Return as _Return
from habil_map import HabiMapCase as _HabiMapCase

import habil_case.tag as tag
import habil_case.task as task


get_api_status = _HabiMapCase.get_case(
    "https://habitica.com/api/v3/status",
    _Return(name='status', func=lambda v:v == "up"),
    token_required=False
)

