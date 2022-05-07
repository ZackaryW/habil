from habil_map import Body, Path, Return, HabiMapCase

get_api_status = HabiMapCase.get_case(
    "https://habitica.com/api/v3/status",
    Return(name='status', func=lambda v:v == "up"),
    token_required=False
)

