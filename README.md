# habil

## Notes
1. currently challenges, clans and all communitiy features are not supported
2. all objects are immutable by default

## requirements
requests

## Example usage
```py

from habil import HabiClient

client = HabiClient.login(
    username="xxxxxxxxxxxxx",
    password="`xxxxxxxxxxxxxx"
)

#1
for task in client.tasks:
    print(task)

#2
for id, tag in client.tags:
    print(tag.name)

```

### Output
```md
# displaying client.tasks
HabiHabit(a2e4ab47-6eb0-44f9-90f2-e9fecfb93d8d)
HabiHabit(9e3f908c-5c66-45b0-8a56-9873356f13e2)
HabiDaily(336ba8f2-948e-4d14-ab8d-87b61c7034be)
HabiDaily(ed1d2801-2676-440a-b967-7c6284d9d117)
HabiDaily(a428340d-a035-4008-b8d1-5f5c246a9b82)
HabiTodo(d98ca9fb-c8a4-4b79-a9bc-2c08aecede61)
HabiTodo(8735fc9e-803c-480e-8ddb-351b74fe56bf)
HabiReward(cea84120-a3a4-4da8-a8a7-fbf0438fe37e)

# displaying tags
Work
Exercise
Health + Wellness
School
Teams
Chores
Creativity
```

## Project Structure
1. (lowest level) habil_map
2. habil_case
3. habil_base
4. habil

### habil_map
used to abstract api calls. 
```py
get_a_task = HabiMapCase.get_case( # creates a get method api call object
    "https://habitica.com/api/v3/tasks/{taskId}", # specifies url
    Return(name="type", xtype=str), # extracted variable
)

get_a_task(taskId="xxxxx")
"""
this is the same as:
1. handling the url, url = url.format(vars)
2. preparing json bodies and param bodies
"""
url : str
body : dict
path : dict

requests.get(url=url, headers=headers, json=json, params=path)
```

### habil_case
is an index of all possible api calls, please refer to https://habitica.com/apidoc

### habil_base
contains generic classes for habil
> HabiToken - token

> HabiUItem - uuid abstract class

### habil
the primary wrapper implementation

### habil_utils
this project is trying to stay independent from other libraries.
all misc functions and classes are stored in habil_util