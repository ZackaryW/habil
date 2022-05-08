from datetime import datetime
from habil_map import Body, Path, Return, HabiMapCase
add_a_tag_to_a_task = HabiMapCase.post_case(
    "https://habitica.com/api/v3/tasks/{taskId}/tags/{tagId}",
)

delete_a_task = HabiMapCase.delete_case(
    "https://habitica.com/api/v3/tasks/{taskId}",
)

get_a_task = HabiMapCase.get_case(
    "https://habitica.com/api/v3/tasks/{taskId}",
)

get_users_tasks = HabiMapCase.get_case(
    "https://habitica.com/api/v3/tasks/user",
    Path(name="type", xtype=str, xrange=("habits", "dailys", "todos", "rewards", "completedTodos")),
)

score_a_checklist_item = HabiMapCase.post_case(
    "https://habitica.com/api/v3/tasks/{taskId}/checklist/{checklistId}/score",
)

score_a_task = HabiMapCase.post_case(
    "https://habitica.com/api/v3/tasks/{taskId}/score/{direction}",
)

update_a_checklist_item = HabiMapCase.put_case(
    "https://habitica.com/api/v3/tasks/{taskId}/checklist/{itemId}",
    Body(name="text", xtype=str),
    Body(name="completed", xtype=bool, default=False),
)


update_a_task = HabiMapCase.put_case(
    "https://habitica.com/api/v3/tasks/{taskId}",
    Body(name="text", xtype=str, optional=True),
    Body(name="attribute", xrange=["str", "int", "per", "con"], optional=True),
    Body(name="collapseChecklist", xtype=bool, optional=True, default=False),
    Body(name="notes", xtype=str, optional=True),
    Body(name="date	", xtype=datetime, optional=True),
    Body(name="priority", xtype=int, optional=True, default=1),
    # ... skipping some
    Body(name="up", xtype=bool, optional=True),
    Body(name="down", xtype=bool, optional=True),
    Body(name="value", xtype=int, optional=True),

)

