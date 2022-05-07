from habil_map import Body, Path, Return, HabiMapCase

create_new_tag = HabiMapCase.post_case(
    "https://habitica.com/api/v3/tags",
    Body(name="name", xtype=str),
    Return(name="id", xtype=str),
    Return(name="name", xtype=str)
)

delete_a_user_tag = HabiMapCase.delete_case(
    "https://habitica.com/api/v3/tags/{tagId}"
)

get_a_users_tags = HabiMapCase.get_case(
    "https://habitica.com/api/v3/tags"
)

reorder_a_tag = HabiMapCase.post_case(
    "https://habitica.com/api/v3/reorder-tags",
    Body(name="tagId", xtype=str),
    Body(name="to", xtype=int),
)

update_a_tag = HabiMapCase.put_case(
    "https://habitica.com/api/v3/tags/{tagId}",
    Body(name="name", xtype=str),
)