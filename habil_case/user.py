from habil_map import Body, Path, Return, HabiMapCase

login = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/auth/local/login",
    Body(name="username", xtype=str),
    Body(name="password", xtype=str),
    Return(name="id", xtype=str),
    Return(name="apiToken", xtype=str),
    token_required=False
)

get_user_profile = HabiMapCase.get_case(
    "https://habitica.com/api/v3/user",
    Path(name="userFields", xtype=str, optional=True),
)

get_user_profile_stats = HabiMapCase.get_case(
    "https://habitica.com/api/v3/user?userFields=stats",
    Return(name="stats.class", xtype=str, rename_to="job", to_repo=True),
    Return(name="stats.lvl", xtype=int, rename_to="lvl", to_repo=True),
    Return(name="stats.exp", xtype=int, rename_to="exp", to_repo=True),
    Return(name="stats.hp", xtype=int, rename_to="hp", to_repo=True),
    Return(name="stats.gp", xtype=int, rename_to="gold", to_repo=True),
    Return(name="stats.str", xtype=int, rename_to="str", to_repo=True),
    Return(name="stats.int", xtype=int, rename_to="int", to_repo=True),
    Return(name="stats.con", xtype=int, rename_to="con", to_repo=True),
    Return(name="stats.per", xtype=int, rename_to="per", to_repo=True),
    Return(name="stats.mp", xtype=int, rename_to="mp", to_repo=True),
)