# habil
a lite wrapper for habitica api

currently, it does not support any community features

## requirements
requests
## examples
### setting up a client
>method 1: using username and password
```py
from habil import HabiClient

client = HabiClient.login(
    username="xxxxxxxxxxxxx",
    password="`xxxxxxxxxxxxxx"
)
```

### get tasks
> method 1
```py
for task in client.tasks:
    print(task)

"""
HabiHabit(a2e4ab47-6eb0-44f9-90f2-e9fecfb93d8d)
HabiHabit(9e3f908c-5c66-45b0-8a56-9873356f13e2)
HabiDaily(336ba8f2-948e-4d14-ab8d-87b61c7034be)
HabiDaily(ed1d2801-2676-440a-b967-7c6284d9d117)
HabiDaily(a428340d-a035-4008-b8d1-5f5c246a9b82)
HabiTodo(d98ca9fb-c8a4-4b79-a9bc-2c08aecede61)
HabiTodo(8735fc9e-803c-480e-8ddb-351b74fe56bf)
HabiReward(cea84120-a3a4-4da8-a8a7-fbf0438fe37e)
"""
```

### update stats
> -1 hp in exchange for 1 gold
```py
# assuming current hp 50 and gold 0
stats = client.stats.update(gold=1, hp=-1)
# expected hp 49 and gold 1
```

### get tags
```py
for tag in client.tags:
    print(tag.name)

"""
Work
Exercise
Health + Wellness
School
Teams
Chores
Creativity
```

