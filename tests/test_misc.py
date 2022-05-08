from pprint import pp, pprint
import unittest
import requests
import json
from habil.habit import HabiHabit
from habil_base.exceptions import HabiRequestRateLimited
from habil_base.habiToken import HabiToken
from habil_base.habiUItem import HabiUItem
from habil_map import HabiMapMeta
import habil_case


class t_map_cases(unittest.TestCase):
    def setUp(self) -> None:
        HabiToken.from_json("config.json", set_global=True)

    def test_api_up(self):
        self.assertTrue(habil_case.get_api_status.request().status)

    def test_rate_limit(self):
        """
        do not use this test too often
        """
        self.assertTrue(habil_case.get_api_status.request().status)
        HabiMapMeta.MIN_TRIGGER_RATE_LIMIT = 28
        with self.assertRaises(HabiRequestRateLimited):
            self.assertTrue(habil_case.get_api_status.request().status)
            self.assertTrue(habil_case.get_api_status.request().status)
    
    def test_get_all_tasks(self):
        from habil import HabiTask

        try:
            tasks = HabiTask.get_all()
            pprint(tasks)
        except:
            pass
        

    def test_get_and_update_one_task(self):
        from habil import HabiTask
        from zxutil.bridge import Bridge
        bridge= Bridge("config.json")
        task = HabiTask.get(id=bridge.test_habit)
        print(repr(task))
        # create random string
        import random
        import string
        random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        task = task.update(text=random_str)
        print(repr(task))
        self.assertEqual(random_str, task.text)

    def test_change_habit_up_down(self):
        from zxutil.bridge import Bridge
        bridge= Bridge("config.json")
        habit = HabiHabit.get(id=bridge.test_habit)
        print(repr(habit))
        pprint(HabiHabit.get_raw(item=habit.id).json_data)

        if habit.up:
            habit = habit.good_habit(False)
        else:
            habit = habit.good_habit(True)

        print(repr(habit))
        pprint(HabiMapMeta.get_last_log())

    def test_score_task(self):
        from habil import HabiTask
        from zxutil.bridge import Bridge
        bridge= Bridge("config.json")
        habit = HabiTask.get(id=bridge.test_habit)
        pprint(HabiHabit.get_raw(item=habit.id).json_data)
        habit = habit.score_task(True)
        print("______________________________")
        pprint(HabiHabit.get_raw(item=habit.id).json_data)