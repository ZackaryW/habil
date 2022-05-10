from habil_map import Body, Path, Return, HabiMapCase

block_unblock_user_from_sending_pm = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/block/{uuid}"
)
