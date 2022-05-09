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
    Return(name="stats.class", xtype=str, rename_to="stat_class", to_repo="job"),
    Return(name="stats.lvl", xtype=int, rename_to="stat_lvl", to_repo="lvl"),
    Return(name="stats.exp", xtype=int, rename_to="stat_exp", to_repo="exp"),
    Return(name="stats.hp", xtype=int, rename_to="stat_hp", to_repo="hp"),
    Return(name="stats.gp", xtype=int, rename_to="stat_gold", to_repo="gold"),
    Return(name="stats.str", xtype=int, rename_to="stat_str", to_repo="str"),
    Return(name="stats.int", xtype=int, rename_to="stat_int", to_repo="int"),
    Return(name="stats.con", xtype=int, rename_to="stat_con", to_repo="con"),
    Return(name="stats.per", xtype=int, rename_to="stat_per", to_repo="per"),
    Return(name="stats.mp", xtype=int, rename_to="stat_mp", to_repo="mp"),
)