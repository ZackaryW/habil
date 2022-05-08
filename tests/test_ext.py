from pprint import pp, pprint
from time import sleep
import unittest
from habil.elements.daily import HabiDaily
from habil.elements.habit import HabiHabit
from habil_base.exceptions import HabiRequestRateLimited
from habil_base.habiToken import HabiToken
from habil_base.habiUItem import HabiUItem
from habil_ext.counterDaily import CounterDaily
from habil_map import HabiMapMeta
import habil_case
import sys
import logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class t_map_cases(unittest.TestCase):
    def setUp(self) -> None:
        HabiToken.from_json("config.json", set_global=True)
        from zxutil.bridge import Bridge
        bridge= Bridge("config.json")
        self.test_daily = bridge.test_daily
    
    def test_counter_daily_1(self):
        daily = HabiDaily.get(id=self.test_daily)
        print(repr(daily))
        daily =daily.update(text="10/10]")
        daily = CounterDaily.overload(daily)
        self.assertIsInstance(daily, HabiDaily)
        
        sleep(3)

        daily = daily.update(text="something something")
        print(repr(daily))
        daily = CounterDaily.overload(daily)
        self.assertIsInstance(daily, HabiDaily)
        
        sleep(3)

        daily = daily.update(text="something [3/10]")
        daily = CounterDaily.overload(daily)
        
        pprint(daily.__dict__)
        self.assertIsInstance(daily, CounterDaily)
        self.assertEqual(daily.current, 3)
        self.assertEqual(daily.max, 10)
        self.assertEqual(daily.text, "something")
        pprint(HabiMapMeta.get_last_log())
        daily.complete()
        pprint(daily.__dict__)
        daily = HabiDaily.get(id=self.test_daily)
        
        pprint(HabiMapMeta.get_last_log())

        self.assertEqual(daily.text, "something [4/10]")