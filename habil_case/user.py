from habil_map import Body, Path, Return, HabiMapCase

login = HabiMapCase.post_case(
    "https://habitica.com/api/v3/user/auth/local/login",
    Body(name="username", xtype=str),
    Body(name="password", xtype=str),
    Return(name="_id", xtype=str),
    Return(name="apiToken", xtype=str),
)