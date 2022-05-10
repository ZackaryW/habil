from habil_map import Body, Path, Return, HabiMapCase

allocate_a_single_stat_point = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/allocate",
    Path(name="stat", xtype=str, xrange=["str", "con", "int", "per"])
)

allocate_all_stat_auto = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/allocate-now"
)

# * Skip Allocate multiple Stat Points


buy_healthy_potion = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy-health-potion"
)

buy_mystery_item_set = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy-mystery-set/{key}"
)

buy_a_piece_of_gear = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy-gear/{key}"
)

buy_a_quest_with_gold = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy-quest/{key}"
)

buy_an_enchanted_armoire_item = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy-armoire"
)

buy_item = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy/{key}"
)

buy_special_item =HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/buy-special-spell/{key}"
)



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
    Return(name="stats.class", xtype=str, rename_to="stats.job", to_repo=True),
    Return(name="stats.lvl", xtype=int, rename_to="stats.lvl", to_repo=True),
    Return(name="stats.exp", xtype=int, rename_to="stats.exp", to_repo=True),
    Return(name="stats.hp", xtype=int, rename_to="stats.hp", to_repo=True),
    Return(name="stats.gp", xtype=int, rename_to="stats.gold", to_repo=True),
    Return(name="stats.str", xtype=int, rename_to="stats.str", to_repo=True),
    Return(name="stats.int", xtype=int, rename_to="stats.inte", to_repo=True),
    Return(name="stats.con", xtype=int, rename_to="stats.con", to_repo=True),
    Return(name="stats.per", xtype=int, rename_to="stats.per", to_repo=True),
    Return(name="stats.mp", xtype=int, rename_to="stats.mp", to_repo=True),
)

get_user_profile_stats = HabiMapCase.get_case(
    "https://habitica.com/api/v3/user?userFields=stats",
    Return(name="stats.class", xtype=str, rename_to="job", to_repo=True),
    Return(name="stats.lvl", xtype=int, rename_to="lvl", to_repo=True),
    Return(name="stats.exp", xtype=int, rename_to="exp", to_repo=True),
    Return(name="stats.hp", xtype=int, rename_to="hp", to_repo=True),
    Return(name="stats.gp", xtype=int, rename_to="gold", to_repo=True),
    Return(name="stats.str", xtype=int, rename_to="str", to_repo=True),
    Return(name="stats.int", xtype=int, rename_to="inte", to_repo=True),
    Return(name="stats.con", xtype=int, rename_to="con", to_repo=True),
    Return(name="stats.per", xtype=int, rename_to="per", to_repo=True),
    Return(name="stats.mp", xtype=int, rename_to="mp", to_repo=True),
)

update_user_profile = HabiMapCase.put_case(
    "https://habitica.com/api/v3/user",
    Body(name="stat_lvl", xtype=int, rename_to="stats.lvl", optional=True),
    Body(name="stat_exp", xtype=int, rename_to="stats.exp", optional=True),
    Body(name="stat_hp", xtype=int, rename_to="stats.hp", optional=True),
    Body(name="stat_gold", xtype=int, rename_to="stats.gp", optional=True),
    Body(name="stat_str", xtype=int, rename_to="stats.str", optional=True),
    Body(name="stat_inte", xtype=int, rename_to="stats.int", optional=True),
    Body(name="stat_con", xtype=int, rename_to="stats.con", optional=True),
    Body(name="stat_per", xtype=int, rename_to="stats.per", optional=True),
    Body(name="stat_mp", xtype=int, rename_to="stats.mp", optional=True),
    # return 
    Return(name="stats.class", xtype=str, rename_to="stats.job", to_repo=True),
    Return(name="stats.lvl", xtype=int, rename_to="stats.lvl", to_repo=True),
    Return(name="stats.exp", xtype=int, rename_to="stats.exp", to_repo=True),
    Return(name="stats.hp", xtype=int, rename_to="stats.hp", to_repo=True),
    Return(name="stats.gp", xtype=int, rename_to="stats.gold", to_repo=True),
    Return(name="stats.str", xtype=int, rename_to="stats.str", to_repo=True),
    Return(name="stats.int", xtype=int, rename_to="stats.inte", to_repo=True),
    Return(name="stats.con", xtype=int, rename_to="stats.con", to_repo=True),
    Return(name="stats.per", xtype=int, rename_to="stats.per", to_repo=True),
    Return(name="stats.mp", xtype=int, rename_to="stats.mp", to_repo=True),
)