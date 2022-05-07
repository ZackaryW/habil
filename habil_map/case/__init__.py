from habil_map.habiMapCase import HabiMapCase
from habil_map.habiMapAttr import HabiMapPathParam as Path
from habil_map.habiMapAttr import HabiMapBodyParam as Body
from habil_map.habiMapAttr import HabiMapReturnParam as Return

get_api_status = HabiMapCase.get_case(
    "https://habitica.com/api/v3/status",
    Return(name='status', func=lambda v:v == "up"),
    token_required=False
)

